import os
import sys
import pickle
import numpy as np
import cv2
import base64
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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

if os.path.exists(FILE_SCALER):
    print(f">> Load Scaler: {FILE_SCALER}")
    with open(FILE_SCALER, 'rb') as f:
        scaler = pickle.load(f)
else:
    print("[WARN] Scaler tidak ditemukan.")

if os.path.exists(FILE_PCA):
    print(f">> Load PCA: {FILE_PCA}")
    with open(FILE_PCA, 'rb') as f:
        pca = pickle.load(f)
else:
    print("[WARN] PCA tidak ditemukan.")

# --- HELPER VISUALISASI ---
def to_base64_image(data):
    """
    Mengubah numpy array (gambar) atau figure matplotlib menjadi base64 string.
    """
    if isinstance(data, np.ndarray):
        # Jika numpy array (gambar CV2)
        _, buffer = cv2.imencode('.png', data)
        return base64.b64encode(buffer).decode('utf-8')
    elif isinstance(data, plt.Figure):
        # Jika figure Matplotlib
        buf = io.BytesIO()
        data.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close(data) # Tutup figure untuk bebaskan memori
        return base64.b64encode(buf.read()).decode('utf-8')
    return None

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

        original_h, original_w, _ = img.shape # Capture original dimensions

        # --- TAHAP 1: PREPROCESSING ---
        gray = preprocessor.to_grayscale_manual(img)
        kernel = preprocessor.gaussian_kernel_manual()
        blurred = preprocessor.convolution_manual(gray, kernel)
        cropped = preprocessor.crop_roi_manual(blurred)
        final_img = preprocessor.resize_padding_manual(cropped, target_size=64)
        
        final_h, final_w = final_img.shape # Capture preprocessed dimensions

        # --- TAHAP 2: EKSTRAKSI FITUR ---
        glcm_feats, glcm_matrix = extractor.extract_glcm_features(final_img)
        hog_feats, hog_mag = extractor.extract_hog_features(final_img, cell_size=8)
        
        # --- TAHAP 3: PREDIKSI ---
        label = "Unknown"
        confidence = 0.0
        features_pca = None
        
        if svm_model and scaler:
            # A. Gabung fitur
            features = np.hstack([glcm_feats, hog_feats]).reshape(1, -1)
            
            # B. Scaling
            features_scaled = scaler.transform(features)
            
            # C. PCA Transform (Jika ada)
            if pca:
                features_pca = pca.transform(features_scaled)
                pred_features = features_pca
            else:
                pred_features = features_scaled

            # D. Prediksi
            pred_idx = int(svm_model.predict(pred_features)[0])
            
            # E. Confidence
            if hasattr(svm_model, "predict_proba"):
                probs = svm_model.predict_proba(pred_features)[0]
                confidence = float(probs[pred_idx])
            else:
                confidence = 1.0 
            
            if 0 <= pred_idx < len(CATEGORIES):
                label = CATEGORIES[pred_idx]

        # --- TAHAP 4: MEMBUAT VISUALISASI ---
        
        # Visualisasi GLCM
        fig_glcm = plt.figure(figsize=(4, 4))
        plt.imshow(glcm_matrix, cmap='viridis', interpolation='nearest')
        plt.title('GLCM Matrix')
        plt.colorbar()
        glcm_base64 = to_base64_image(fig_glcm)

        # Visualisasi PCA
        pca_base64 = None
        if features_pca is not None:
            fig_pca = plt.figure(figsize=(6, 3))
            plt.bar(range(len(features_pca[0])), features_pca[0])
            plt.title('PCA-transformed Features')
            plt.xlabel('Principal Component')
            plt.ylabel('Value')
            pca_base64 = to_base64_image(fig_pca)

        # --- TAHAP 5: KIRIM RESPON JSON ---
        return jsonify({
            'status': 'success',
            'label': label,
            'confidence': f"{confidence:.2f}",
            'metadata': {
                'original_dimensions': {'width': original_w, 'height': original_h},
                'preprocessed_dimensions': {'width': final_w, 'height': final_h}
            },
            'visualizations': {
                'preprocessed': to_base64_image(final_img),
                'hog': to_base64_image(hog_mag),
                'glcm': glcm_base64,
                'pca': pca_base64
            }
        })

    except Exception as e:
        import traceback
        print(f"[ERROR] {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)