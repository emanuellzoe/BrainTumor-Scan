import os
import cv2
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Import modul kita
from modules.preprocessing import ManualPreprocessor, ManualStandardScaler
from modules.features import ManualFeatures
from modules.model_manual import ManualMulticlassSVM
from modules.model_library import LibrarySVM

# --- PATH DINAMIS ---
# Mendapatkan lokasi file train_smart.py ini berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Menentukan lokasi Cache & Dataset relatif terhadap file ini
CACHE_FILE_X = os.path.join(BASE_DIR, 'cache_features.npy')
CACHE_FILE_Y = os.path.join(BASE_DIR, 'cache_labels.npy')
DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'Training') # Pastikan folder Training ada di dalam dataset
SCALER_PATH = os.path.join(BASE_DIR, 'scaler.pkl')

def load_or_extract_features():
    """
    Fungsi Pintar V2: Interaktif menanyakan user.
    """
    # 1. CEK APAKAH CACHE ADA?
    if os.path.exists(CACHE_FILE_X) and os.path.exists(CACHE_FILE_Y):
        print("\n[INFO] Ditemukan Data Fitur Tersimpan (Cache).")
        print("Apakah Anda baru saja mengubah/menambah dataset gambar?")
        print("   y = Ya, Scan Ulang Dataset (Lama - Pilih ini jika nambah gambar)")
        print("   n = Tidak, Pakai Cache Saja (Cepat - Pilih ini jika cuma ganti model)")
        
        jawaban = input("Jawab (y/n): ").lower()
        
        if jawaban == 'n':
            print("\n>> Menggunakan Data Cache (Skip Ekstraksi)...")
            X = np.load(CACHE_FILE_X)
            y = np.load(CACHE_FILE_Y)
            return X, y
        else:
            print("\n>> Oke, menghapus cache lama dan scan ulang...")
            # Lanjut ke proses ekstraksi di bawah

    # 2. EKSTRAKSI MANUAL DARI FOLDER
    print("\n[INFO] Memulai Ekstraksi Fitur dari 0...")
    
    preprocessor = ManualPreprocessor()
    extractor = ManualFeatures()
    
    DATASET_PATH = "dataset/Training"
    CATEGORIES = ["glioma", "meningioma", "notumor", "pituitary"]
    
    X_features = []
    y_labels = []
    
    for label_id, category in enumerate(CATEGORIES):
        path = os.path.join(DATASET_PATH, category)
        if not os.path.exists(path): continue
        
        images = os.listdir(path)
        print(f"   - Memproses {category} ({len(images)} gambar)...")
        
        for idx, img_name in enumerate(images):
            # Tampilkan progress bar sederhana
            if idx % 50 == 0: 
                print(f"     Progress: {idx}/{len(images)}", end='\r')
            
            try:
                img_path = os.path.join(path, img_name)
                img = cv2.imread(img_path)
                if img is None: continue
                
                # Preprocessing
                gray = preprocessor.to_grayscale_manual(img)
                kernel = preprocessor.gaussian_kernel_manual()
                blurred = preprocessor.convolution_manual(gray, kernel)
                cropped = preprocessor.crop_roi_manual(blurred)
                final = preprocessor.resize_padding_manual(cropped, target_size=64)
                
                # Ekstraksi
                glcm = extractor.extract_glcm_features(final)
                hog = extractor.extract_hog_features(final, cell_size=8)
                
                combined = np.hstack([glcm, hog])
                X_features.append(combined)
                y_labels.append(label_id)
                
            except Exception:
                pass
    
    X = np.array(X_features)
    y = np.array(y_labels)
    
    # 3. SIMPAN HASILNYA (OVERWRITE CACHE LAMA)
    print(f"\n\n>> Menyimpan hasil baru ke '{CACHE_FILE_X}'...")
    np.save(CACHE_FILE_X, X)
    np.save(CACHE_FILE_Y, y)
    
    return X, y

def run_training_smart():
    # --- LANGKAH 1: DAPATKAN DATA ---
    X, y = load_or_extract_features()
    
    print(f"\n>> Total Data Siap: {len(X)} sampel.")
    
    # Inisialisasi Scaler
    scaler = ManualStandardScaler()
    
    # --- LANGKAH 2: SPLIT DATA ---
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # --- LANGKAH 3: SCALING ---
    print(">> Melakukan Scaling Data...")
    X_train = scaler.fit_transform(X_train_raw)
    X_test = scaler.transform(X_test_raw)
    
    # Simpan Scaler (Penting diupdate jika data berubah)
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
        
    # --- LANGKAH 4: PILIH MODEL ---
    print("\nPilih Mode Training:")
    print("1. Manual SVM")
    print("2. Library SVM (Recommended)")
    choice = input("Pilih (1/2): ")
    
    if choice == '1':
        print("\n>> Melatih SVM MANUAL...")
        model = ManualMulticlassSVM(n_classes=4, n_iters=1000)
        save_name = 'model_manual.pkl'
    else:
        print("\n>> Melatih SVM LIBRARY...")
        model = LibrarySVM()
        save_name = 'model_library.pkl'
        
    model.fit(X_train, y_train)
    
    # --- LANGKAH 5: EVALUASI ---
    print("\n>> Evaluasi Model...")
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"   AKURASI: {acc*100:.2f}%")
    
    target_names = ["glioma", "meningioma", "notumor", "pituitary"]
    print(classification_report(y_test, preds, target_names=target_names))
    
    # Ubah cara save model biar masuk ke folder ML
    if choice == '1':
        save_name = os.path.join(BASE_DIR, 'model_manual.pkl')
    else:
        save_name = os.path.join(BASE_DIR, 'model_library.pkl')
        
    model.save(save_name)
    print(f"\n[SUKSES] Model disimpan di: {save_name}")

if __name__ == "__main__":
    run_training_smart()