from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import pickle
import os
import sys

# --- KONFIGURASI PATH DINAMIS (PENTING) ---
# Agar Python tahu posisi file ini ada di folder "ML"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR) # Pastikan folder ML terbaca sebagai modul

# Import modul dari folder yang sama
from modules.preprocessing import ManualPreprocessor
from modules.features import ManualFeatures
from modules.model_manual import ManualMulticlassSVM 

app = Flask(__name__)
CORS(app)

preprocessor = ManualPreprocessor()
extractor = ManualFeatures()

# --- DIAGNOSIS PATH ---
print("\n" + "="*40)
print("       API DIAGNOSTIC (NEW STRUCTURE)")
print("="*40)
print(f"[INFO] Lokasi Script: {BASE_DIR}")

# Tentukan lokasi file Model & Scaler secara Absolut
# Jadi mau terminalnya di BRAIN-SCAN atau di ML, dia tetap ketemu
file_manual = os.path.join(BASE_DIR, 'model_manual.pkl')
file_library = os.path.join(BASE_DIR, 'model_library.pkl')
file_scaler = os.path.join(BASE_DIR, 'scaler.pkl')

has_manual = os.path.exists(file_manual)
has_library = os.path.exists(file_library)
has_scaler = os.path.exists(file_scaler)

print(f"[CHECK] {os.path.basename(file_library)} : {'ADA' if has_library else 'TIDAK ADA'}")
print(f"[CHECK] {os.path.basename(file_scaler)}          : {'ADA' if has_scaler else 'TIDAK ADA'}")

svm_model = None
scaler = None
CATEGORIES = ["Glioma", "Meningioma", "No Tumor", "Pituitary"]

# Logika Load Model
if has_manual:
    print(f">> [SUCCESS] Memuat MODEL MANUAL...")
    with open(file_manual, 'rb') as f:
        svm_model = pickle.load(f)
elif has_library:
    print(f">> [SUCCESS] Memuat MODEL LIBRARY...")
    with open(file_library, 'rb') as f:
        svm_model = pickle.load(f)
else:
    print(">> [CRITICAL] TIDAK ADA MODEL! Jalankan 'python ML/train_smart.py' dulu.")

# Logika Load Scaler
if has_scaler:
    print(f">> [SUCCESS] Memuat SCALER...")
    with open(file_scaler, 'rb') as f:
        scaler = pickle.load(f)
else:
    print(">> [WARNING] Scaler tidak ditemukan.")

print("="*40 + "\n")

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    in_memory_file = file.read()
    nparr = np.frombuffer(in_memory_file, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None: return jsonify({'error': 'Bad image'}), 400

    try:
        # Preprocessing
        gray = preprocessor.to_grayscale_manual(img)
        kernel = preprocessor.gaussian_kernel_manual()
        blurred = preprocessor.convolution_manual(gray, kernel)
        cropped = preprocessor.crop_roi_manual(blurred)
        final_img = preprocessor.resize_padding_manual(cropped, target_size=64)

        # Ekstraksi
        glcm = extractor.extract_glcm_features(final_img)
        hog_feats = extractor.extract_hog_features(final_img, cell_size=8)
        
        prediction_text = "Model belum dilatih"
        
        # Prediksi
        if svm_model is not None:
            features_vector = np.hstack([glcm, hog_feats]).reshape(1, -1)
            
            if scaler:
                features_vector = scaler.transform(features_vector)
            
            pred_idx = svm_model.predict(features_vector)[0]
            pred_idx = int(pred_idx)
            
            if 0 <= pred_idx < len(CATEGORIES):
                prediction_text = CATEGORIES[pred_idx]
                if hasattr(svm_model, "predict_proba"):
                    probs = svm_model.predict_proba(features_vector)[0]
                    confidence = probs[pred_idx] * 100
                    prediction_text += f" ({confidence:.1f}%)"
            else:
                prediction_text = "Unknown"

        return jsonify({
            'status': 'success',
            'features': {
                'glcm': {
                    'contrast': float(glcm[0]),
                    'energy': float(glcm[1]),
                    'homogeneity': float(glcm[2]),
                    'correlation': float(glcm[3])
                },
                'hog': {
                    'total_features': len(hog_feats),
                    'sample_values': [float(x) for x in hog_feats[:5]]
                }
            },
            'prediction': prediction_text
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)