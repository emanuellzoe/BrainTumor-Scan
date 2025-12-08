import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from modules.preprocessing import ManualPreprocessor
from modules.features import ManualFeatures

# --- 1. SETUP ---
preprocessor = ManualPreprocessor()
extractor = ManualFeatures()

sample_path = "dataset/Training/glioma/Tr-gl_0010.jpg"

if not os.path.exists(sample_path):
    print("ERROR: Gambar tidak ditemukan! Cek path.")
else:
    # --- 2. PREPROCESSING ---
    print(">> [1/2] Menjalankan Preprocessing...")
    img = cv2.imread(sample_path)
    gray = preprocessor.to_grayscale_manual(img)
    blurred = preprocessor.convolution_manual(gray, preprocessor.gaussian_kernel_manual())
    cropped = preprocessor.crop_roi_manual(blurred)
    # Kita resize ke 128x128 saja agar ekstraksi fitur saat testing cepat
    final_img = preprocessor.resize_padding_manual(cropped, target_size=128)
    
    # --- 3. EKSTRAKSI FITUR ---
    print(">> [2/2] Menjalankan Ekstraksi Fitur Manual...")
    
    # Test GLCM
    glcm_feats = extractor.extract_glcm_features(final_img)
    print(f"   [GLCM] Contrast: {glcm_feats[0]:.4f}, Energy: {glcm_feats[1]:.4f}")
    
    # Test HOG
    hog_feats = extractor.extract_hog_features(final_img, cell_size=16)
    print(f"   [HOG] Jumlah fitur HOG (Global): {len(hog_feats)}")
    
    # Test FULL (Grid 3x3 + Global)
    full_feats = extractor.extract_full_features(final_img)
    print(f"   [FULL] Total Dimensi Vektor Fitur (Global + 3x3 Grid): {len(full_feats)}")
    
    print("\nSUKSES! Kode manual berjalan tanpa error.")
    
    # Visualisasi HOG Gradient
    mag, ang = extractor.compute_gradients_manual(final_img)
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(final_img, cmap='gray')
    plt.title("Input Image")
    
    plt.subplot(1, 2, 2)
    plt.imshow(mag, cmap='gray') # Visualisasi kekuatan tepi
    plt.title("Visualisasi Gradient Magnitude (HOG Base)")
    
    plt.show()