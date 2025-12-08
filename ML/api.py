import os
import sys
import pickle
import numpy as np
import cv2
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- SETUP PATH ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from modules.preprocessing import ManualPreprocessor
from modules.features import ManualFeatures
from modules.pca import ManualPCA

app = Flask(__name__)
CORS(app)

preprocessor = ManualPreprocessor()
extractor = ManualFeatures()

# --- KONFIGURASI FILE ---
FILE_LIBRARY = os.path.join(BASE_DIR, 'model_library.pkl')
FILE_MANUAL = os.path.join(BASE_DIR, 'model_manual.pkl')
FILE_SCALER = os.path.join(BASE_DIR, 'scaler.pkl')
FILE_PCA = os.path.join(BASE_DIR, 'pca.pkl')

CATEGORIES = ["Glioma", "Meningioma", "No Tumor", "Pituitary"]
svm_model = None
scaler = None
pca = None

# --- LOAD MODEL SAAT STARTUP ---
print(f"[INFO] Backend Start di: {BASE_DIR}")

# 1. Cek Model
if os.path.exists(FILE_LIBRARY):
    print(f">> Load Model Library: {FILE_LIBRARY}")
    with open(FILE_LIBRARY, 'rb') as f:
        svm_model = pickle.load(f)
elif os.path.exists(FILE_MANUAL):
    print(f">> Load Model Manual: {FILE_MANUAL}")
    with open(FILE_MANUAL, 'rb') as f:
        svm_model = pickle.load(f)
else:
    print("[WARN] Belum ada model! Jalankan 'python ML/train_smart.py' dulu.")

# 2. Cek Scaler
if os.path.exists(FILE_SCALER):
    print(f">> Load Scaler: {FILE_SCALER}")
    with open(FILE_SCALER, 'rb') as f:
        scaler = pickle.load(f)
else:
    print("[WARN] Scaler tidak ditemukan.")

# 3. Cek PCA
if os.path.exists(FILE_PCA):
    print(f">> Load PCA: {FILE_PCA}")
    with open(FILE_PCA, 'rb') as f:
        pca = pickle.load(f)
else:
    print("[WARN] PCA tidak ditemukan.")

# --- ROUTES ---
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    try:
        # 1. Baca Gambar
        file = request.files['file']
        np_img = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'error': 'Invalid image format'}), 400

        # 2. Preprocessing & Ekstraksi
        gray = preprocessor.to_grayscale_manual(img)
        kernel = preprocessor.gaussian_kernel_manual()
        blurred = preprocessor.convolution_manual(gray, kernel)
        cropped = preprocessor.crop_roi_manual(blurred)
        final_img = preprocessor.resize_padding_manual(cropped, target_size=64)

        glcm = extractor.extract_glcm_features(final_img)
        hog = extractor.extract_hog_features(final_img, cell_size=8)
        
        # 3. Prediksi
        label = "Unknown"
        confidence = 0.0
        
        if svm_model and scaler:
            # A. Gabung fitur
            features = np.hstack([glcm, hog]).reshape(1, -1)
            
            # B. Scaling (CUKUP SATU KALI!)
            features = scaler.transform(features)
            
            # C. PCA Transform (Jika ada)
            if pca:
                features = pca.transform(features)

            # D. Prediksi
            pred_idx = int(svm_model.predict(features)[0])
            
            # E. Confidence
            if hasattr(svm_model, "predict_proba"):
                probs = svm_model.predict_proba(features)[0]
                confidence = float(probs[pred_idx])
            else:
                confidence = 1.0 
            
            if 0 <= pred_idx < len(CATEGORIES):
                label = CATEGORIES[pred_idx]

        # 4. Kirim Respon JSON
        return jsonify({
            'status': 'success',
            'label': label,
            'confidence': confidence,
            'features': {
                'glcm_contrast': float(glcm[0]),
                'hog_len': len(hog)
            }
        })

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)