import os
import sys
import cv2
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# --- KONFIGURASI PATH ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Import modul kita
try:
    from modules.preprocessing import ManualPreprocessor, ManualStandardScaler
    from modules.features import ManualFeatures
    from modules.pca import ManualPCA  # <--- IMPORT PCA (Pastikan file modules/pca.py sudah dibuat)
    from modules.model_manual import ManualMulticlassSVM
    from modules.model_library import LibrarySVM
except ImportError as e:
    print(f"[ERROR] Gagal import modul: {e}")
    print("Pastikan file 'modules/pca.py' sudah dibuat sesuai instruksi sebelumnya.")
    sys.exit(1)

# Lokasi file Output (Absolut)
CACHE_FILE_X = os.path.join(BASE_DIR, 'cache_features.npy')
CACHE_FILE_Y = os.path.join(BASE_DIR, 'cache_labels.npy')
DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'Training') 
SCALER_PATH = os.path.join(BASE_DIR, 'scaler.pkl')
PCA_PATH = os.path.join(BASE_DIR, 'pca.pkl') # <--- File Output PCA

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
    def save(self, filename):
        with open(filename, 'wb') as f: pickle.dump(self.model, f)

# --- FUNGSI UTAMA ---
def load_or_extract_features():
    # 1. CEK CACHE
    if os.path.exists(CACHE_FILE_X) and os.path.exists(CACHE_FILE_Y):
        print("\n[INFO] Cache ditemukan.")
        print("Ketik 'y' untuk scan ulang dataset (jika ada gambar baru).")
        print("Ketik 'n' untuk pakai cache (cepat).")
        choice = input("Scan ulang? (y/n): ").lower()
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

def run_training_smart():
    # 1. Load Data
    X, y = load_or_extract_features()
    print(f">> Total Sampel: {len(X)}")
    print(f">> Dimensi Awal: {X.shape[1]} fitur")
    
    # 2. Split Data
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Scaling (Wajib sebelum PCA)
    print(">> Melakukan Scaling Manual...")
    scaler = ManualStandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_raw)
    X_test_scaled = scaler.transform(X_test_raw)
    
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)
        
    # 4. PCA (Reduksi Dimensi) - BAGIAN BARU
    print(">> Melakukan PCA (Manual)...")
    # Mempertahankan 95% informasi
    pca = ManualPCA(n_components=0.95)
    
    X_train = pca.fit_transform(X_train_scaled)
    X_test = pca.transform(X_test_scaled)
    
    print(f">> Dimensi Setelah PCA: {X_train.shape[1]} fitur utama")
    
    with open(PCA_PATH, 'wb') as f:
        pickle.dump(pca, f)
        
    # 5. Pilih Model
    print("\nPilih Model:")
    print("1. Manual SVM (CPU)")
    print("2. Library SVM (Auto GPU/CPU)")
    mode = input("Pilih (1/2): ")
    
    model = None
    save_path = ""

    if mode == '1':
        print(">> [MODE] Manual SVM...")
        model = ManualMulticlassSVM(n_classes=4)
        save_path = os.path.join(BASE_DIR, 'model_manual.pkl')
    else:
        try:
            import cuml
            print(">> [GPU] Menggunakan RAPIDS cuML...")
            model = GPULibrarySVM()
        except ImportError:
            print(">> [CPU] Menggunakan Scikit-Learn...")
            model = LibrarySVM()
        save_path = os.path.join(BASE_DIR, 'model_library.pkl')
        
    # 6. Training & Evaluasi
    print(">> Mulai Training...")
    model.fit(X_train, y_train)
    
    print("\n>> Evaluasi...")
    preds = model.predict(X_test)
    
    # Handle output format dari GPU (jika ada)
    if hasattr(preds, 'to_numpy'): preds = preds.to_numpy()
    if hasattr(y_test, 'to_numpy'): y_test = y_test.to_numpy()

    acc = accuracy_score(y_test, preds)
    print(f"   Akurasi: {acc*100:.2f}%")
    print(classification_report(y_test, preds, target_names=["Glioma", "Meningioma", "NoTumor", "Pituitary"]))
    
    model.save(save_path)
    print(f"[SUKSES] Model tersimpan di: {save_path}")

if __name__ == "__main__":
    run_training_smart()