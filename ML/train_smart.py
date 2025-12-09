import os
import sys
import cv2
import numpy as np
import pickle
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import label_binarize

# --- KONFIGURASI PATH ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Import modul kita
try:
    from modules.preprocessing import ManualPreprocessor, ManualStandardScaler
    from modules.features import ManualFeatures
    from modules.pca import ManualPCA 
    from modules.model_manual import ManualMulticlassSVM
    from modules.model_library import LibrarySVM
except ImportError as e:
    print(f"[ERROR] Gagal import modul: {e}")
    sys.exit(1)

# Lokasi file Output (Absolut)
CACHE_FILE_X = os.path.join(BASE_DIR, 'cache_features.npy')
CACHE_FILE_Y = os.path.join(BASE_DIR, 'cache_labels.npy')
DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'Training') 
SCALER_PATH = os.path.join(BASE_DIR, 'scaler.pkl')
PCA_PATH = os.path.join(BASE_DIR, 'pca.pkl') 

# --- DEFINISI KELAS GPU SVM (WRAPPER) ---
class GPULibrarySVM:
    def __init__(self):
        import cuml 
        self.model = cuml.svm.SVC(kernel='rbf', probability=True)
    def fit(self, X, y):
        X = X.astype(np.float32); y = y.astype(np.float32)
        self.model.fit(X, y)
    def predict(self, X):
        X = X.astype(np.float32)
        return self.model.predict(X)
    def decision_function(self, X):
        # cuML SVC uses predict_proba for probabilities, but we can map it to decision function concept if needed
        # Or better, return proba for ROC AUC if available
        X = X.astype(np.float32)
        return self.model.predict_proba(X)
    def save(self, filename):
        with open(filename, 'wb') as f: pickle.dump(self.model, f)

# --- FUNGSI UTAMA ---
def load_or_extract_features():
    # 1. CEK CACHE
    if os.path.exists(CACHE_FILE_X) and os.path.exists(CACHE_FILE_Y):
        print("\n[INFO] Cache ditemukan.")
        # print("Ketik 'y' untuk scan ulang dataset (jika ada gambar baru).")
        # print("Ketik 'n' untuk pakai cache (cepat).")
        # choice = input("Scan ulang? (y/n): ").lower()
        choice = 'n' # Default auto-use cache for speed now
        if choice != 'y':
            print(">> Menggunakan Cache...")
            return np.load(CACHE_FILE_X), np.load(CACHE_FILE_Y)

    # 2. EKSTRAKSI BARU
    print(f"\n[INFO] Memulai Ekstraksi dari: {DATASET_PATH}")
    if not os.path.exists(DATASET_PATH):
        print(f"[CRITICAL ERROR] Folder dataset tidak ditemukan: {DATASET_PATH}")
        sys.exit(1)

    preprocessor = ManualPreprocessor()
    extractor = ManualFeatures()
    CATEGORIES = ["glioma", "meningioma", "notumor", "pituitary"]
    
    X_features = []
    y_labels = []
    
    for label_id, category in enumerate(CATEGORIES):
        cat_path = os.path.join(DATASET_PATH, category)
        if not os.path.exists(cat_path): continue
            
        images = os.listdir(cat_path)
        count = len(images)
        print(f"   - {category}: {count} gambar")
        
        for i, img_name in enumerate(images):
            try:
                img_path = os.path.join(cat_path, img_name)
                img = cv2.imread(img_path)
                if img is None: continue
                
                # Pipeline Preprocessing
                gray = preprocessor.to_grayscale_manual(img)
                kernel = preprocessor.gaussian_kernel_manual()
                blurred = preprocessor.convolution_manual(gray, kernel)
                cropped = preprocessor.crop_roi_manual(blurred)
                final = preprocessor.resize_padding_manual(cropped, target_size=64)
                
                # Ekstraksi Fitur
                glcm = extractor.extract_glcm_features(final)
                hog = extractor.extract_hog_features(final, cell_size=8)
                
                combined = np.hstack([glcm, hog])
                X_features.append(combined)
                y_labels.append(label_id)
                
                if i % 100 == 0: print(f"      Proses: {i}/{count}", end='\r')
            except: pass
    
    print("\n")
    X = np.array(X_features)
    y = np.array(y_labels)

    if len(X) == 0:
        print("[ERROR] Tidak ada data terekstraksi.")
        sys.exit(1)

    print(">> Menyimpan Cache...")
    np.save(CACHE_FILE_X, X)
    np.save(CACHE_FILE_Y, y)
    
    return X, y

def print_confusion_matrix(cm, classes):
    print("\n   [CONFUSION MATRIX]")
    print(f"   {'':<12} | {' | '.join([f'{c:<10}' for c in classes])} |")
    print("   " + "-" * 60)
    for i, row in enumerate(cm):
        print(f"   {classes[i]:<12} | {' | '.join([f'{val:<10}' for val in row])} |")

def run_training_smart():
    # 1. Load Data
    X, y = load_or_extract_features()
    print(f">> Total Sampel: {len(X)}")
    print(f">> Dimensi Awal: {X.shape[1]} fitur")
    
    # Pilih Model
    print("\nPilih Model:")
    print("1. Manual SVM (CPU) - Lebih Lambat, Implementasi Sendiri")
    print("2. Library SVM (Scikit-Learn/cuML) - Cepat, Standar Industri")
    mode_input = input("Pilih (1/2): ")
    
    is_manual = (mode_input == '1')
    save_path = os.path.join(BASE_DIR, 'model_manual.pkl' if is_manual else 'model_library.pkl')
    
    # Konfigurasi K-Fold
    K = 5
    skf = StratifiedKFold(n_splits=K, shuffle=True, random_state=42)
    
    acc_scores = []
    auc_scores = []
    
    # Variabel untuk akumulasi Confusion Matrix Global
    y_true_all = []
    y_pred_all = []
    
    print(f"\n[INFO] Memulai {K}-Fold Cross Validation...")
    print("=" * 60)

    fold = 1
    final_model = None
    final_scaler = None
    final_pca = None

    for train_index, test_index in skf.split(X, y):
        print(f"Fold {fold}/{K}: ", end="")
        
        # Split Data
        X_train_raw, X_test_raw = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        
        # --- A. SCALING (Fit pada Train saja!) ---
        scaler = ManualStandardScaler()
        X_train_scaled = scaler.fit_transform(X_train_raw)
        X_test_scaled = scaler.transform(X_test_raw)
        
        # --- B. PCA (Fit pada Train saja!) ---
        pca = ManualPCA(n_components=0.95)
        X_train_pca = pca.fit_transform(X_train_scaled)
        X_test_pca = pca.transform(X_test_scaled)
        
        # --- C. TRAINING ---
        if is_manual:
            model = ManualMulticlassSVM(n_classes=4)
        else:
            try:
                import cuml
                model = GPULibrarySVM()
            except ImportError:
                model = LibrarySVM()
                
        model.fit(X_train_pca, y_train)
        
        # --- D. PREDIKSI ---
        preds = model.predict(X_test_pca)
        
        # Convert GPU results to numpy if needed
        if hasattr(preds, 'to_numpy'): preds = preds.to_numpy()
        if hasattr(y_test, 'to_numpy'): y_test = y_test.to_numpy()
            
        # --- E. METRIK PER FOLD ---
        acc = accuracy_score(y_test, preds)
        acc_scores.append(acc)
        
        # Hitung AUC (One-vs-Rest)
        try:
            # Ambil Decision Function (Score) atau Probability
            if hasattr(model, 'decision_function'):
                scores = model.decision_function(X_test_pca)
            elif hasattr(model, 'predict_proba'): # Fallback for sklearn SVC
                scores = model.predict_proba(X_test_pca)
            else:
                 # Fallback manual dummy scores if neither exists (should not happen with our classes)
                 scores = np.zeros((len(y_test), 4))
            
            # Handle GPU output
            if hasattr(scores, 'to_numpy'): scores = scores.to_numpy()

            # Binarize labels for AUC
            y_test_bin = label_binarize(y_test, classes=[0, 1, 2, 3])
            
            # Jika scores tidak berbentuk probabilitas (misal decision function dari SVM Manual), 
            # roc_auc_score tetap bisa menghandlenya untuk ranking.
            # Namun untuk Manual SVM kita return raw scores, jadi cocok.
            
            auc = roc_auc_score(y_test_bin, scores, multi_class='ovr', average='macro')
            auc_scores.append(auc)
        except Exception as e:
            print(f"(AUC Error: {e})", end=" ")
            auc = 0
            auc_scores.append(0)

        print(f"Acc: {acc*100:.2f}% | AUC: {auc:.4f}")
        
        # Simpan untuk Global Report
        y_true_all.extend(y_test)
        y_pred_all.extend(preds)
        
        # Kita simpan model dari fold terakhir (atau terbaik) sebagai output final
        final_model = model
        final_scaler = scaler
        final_pca = pca
        
        fold += 1

    print("=" * 60)
    print(f"\n[HASIL AKHIR K-FOLD]")
    print(f">> Rata-rata Akurasi : {np.mean(acc_scores)*100:.2f}%")
    print(f">> Rata-rata AUC     : {np.mean(auc_scores):.4f}")
    
    # Confusion Matrix Global
    target_names = ["Glioma", "Meningioma", "NoTumor", "Pituitary"]
    cm = confusion_matrix(y_true_all, y_pred_all)
    print_confusion_matrix(cm, target_names)
    
    print("\n[CLASSIFICATION REPORT GLOBAL]")
    print(classification_report(y_true_all, y_pred_all, target_names=target_names))
    
    # Simpan Model & Scaler & PCA (Dari Fold Terakhir sebagai representasi)
    # Catatan: Idealnya kita retrain FULL dataset, tapi fold terakhir sudah cukup representatif 
    # karena dilatih dengan 80% data.
    
    final_model.save(save_path)
    with open(SCALER_PATH, 'wb') as f: pickle.dump(final_scaler, f)
    with open(PCA_PATH, 'wb') as f: pickle.dump(final_pca, f)
    
    print(f"\n[SUKSES] Model tersimpan di: {save_path}")

if __name__ == "__main__":
    run_training_smart()
