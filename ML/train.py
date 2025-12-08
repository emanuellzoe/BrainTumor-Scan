# import os
# import cv2
# import numpy as np
# import pickle
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score, classification_report

# # Import modul
# from modules.preprocessing import ManualPreprocessor, ManualStandardScaler # <--- Import baru
# from modules.features import ManualFeatures
# from modules.model_manual import ManualMulticlassSVM
# from modules.model_library import LibrarySVM

# def run_training():
#     preprocessor = ManualPreprocessor()
#     extractor = ManualFeatures()
#     scaler = ManualStandardScaler() # <--- Inisialisasi Scaler
    
#     DATASET_PATH = "dataset/Training"
#     CATEGORIES = ["glioma", "meningioma", "notumor", "pituitary"]
    
#     X_features = []
#     y_labels = []
    
#     print("=== MULAI TRAINING (FULL DATASET) ===")
#     print(">> [1/4] Ekstraksi Fitur (Ini akan memakan waktu lama, sabar ya!)...")
    
#     for label_id, category in enumerate(CATEGORIES):
#         path = os.path.join(DATASET_PATH, category)
#         if not os.path.exists(path): continue
        
#         # --- PERUBAHAN PENTING DI SINI ---
#         # Kita pakai SEMUA data (hapus [:50])
#         images = os.listdir(path) 
#         print(f"   - Memproses kelas {category}: {len(images)} gambar...")
        
#         for img_name in images:
#             try:
#                 img_path = os.path.join(path, img_name)
#                 img = cv2.imread(img_path)
#                 if img is None: continue
                
#                 # A. Preprocessing
#                 gray = preprocessor.to_grayscale_manual(img)
#                 # Resize 64x64 cukup untuk pola tumor, tapi jauh lebih ringan
#                 blurred = preprocessor.convolution_manual(gray, preprocessor.gaussian_kernel_manual())
#                 cropped = preprocessor.crop_roi_manual(blurred)
#                 final = preprocessor.resize_padding_manual(cropped, target_size=64)
                
#                 # B. Ekstraksi Fitur
#                 glcm = extractor.extract_glcm_features(final)
#                 hog = extractor.extract_hog_features(final, cell_size=8)
                
#                 combined = np.hstack([glcm, hog])
#                 X_features.append(combined)
#                 y_labels.append(label_id)
                
#             except Exception as e:
#                 pass

#     X = np.array(X_features)
#     y = np.array(y_labels)
    
#     # --- SPLIT DATA ---
#     X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
#     # --- SCALING (PENYETARAAN) ---
#     print(f"\n>> [2/4] Melakukan Scaling Fitur Manual...")
#     # Pelajari pola data latih
#     X_train = scaler.fit_transform(X_train_raw)
#     # Terapkan pola yang sama ke data tes
#     X_test = scaler.transform(X_test_raw)
    
#     # Simpan Scaler (PENTING: Agar API tahu cara scaling gambar baru)
#     with open('scaler.pkl', 'wb') as f:
#         pickle.dump(scaler, f)
#     print("   Scaler disimpan ke 'scaler.pkl'")

#     print(f"\n>> Total Data: {len(X)} | Fitur per Citra: {X.shape[1]}")
    
#     # --- TRAINING ---
#     print("\nPilih Mode:")
#     print("1. Manual SVM (Lama - Bisa 10-30 menit)")
#     print("2. Library SVM (Cepat & Akurat - Disarankan untuk hasil terbaik)")
#     choice = input("Pilih (1/2): ")
    
#     if choice == '1':
#         print("\n>> [3/4] Melatih SVM MANUAL...")
#         model = ManualMulticlassSVM(n_classes=4, n_iters=1000)
#         save_name = 'model_manual.pkl'
#     else:
#         print("\n>> [3/4] Melatih SVM LIBRARY...")
#         model = LibrarySVM()
#         save_name = 'model_library.pkl'
        
#     model.fit(X_train, y_train)
    
#     # --- EVALUASI ---
#     print("\n>> [4/4] Evaluasi Akurasi...")
#     preds = model.predict(X_test)
#     acc = accuracy_score(y_test, preds)
#     print(f"   AKURASI AKHIR: {acc*100:.2f}%")
    
#     target_names = ["glioma", "meningioma", "notumor", "pituitary"]
#     print(classification_report(y_test, preds, target_names=target_names))
    
#     model.save(save_name)
#     print(f"\n[SUKSES] Model disimpan sebagai '{save_name}'")

# if __name__ == "__main__":
#     run_training()