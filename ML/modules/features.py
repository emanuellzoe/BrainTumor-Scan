import numpy as np
import math

class ManualFeatures:
    def __init__(self):
        pass

    # ==========================================
    # BAGIAN 1: GLCM (Gray Level Co-occurrence Matrix)
    # ==========================================
    
    def quantize_image(self, image, levels=8):
        """
        [MANUAL GLCM 1] Menyederhanakan warna.
        Dari 0-255 (256 warna) menjadi 0-7 (8 warna) agar matriks GLCM tidak kegedean.
        Rumus: pixel_baru = floor(pixel_lama / (256 / levels))
        """
        ratio = 256 / levels
        quantized = (image / ratio).astype(int)
        return quantized, levels

    def compute_glcm_matrix(self, image, distance=1, angle=0):
        """
        [MANUAL GLCM 2] Membuat matriks frekuensi ketetanggaan pixel.
        Angle 0 derajat = Cek piksel sebelah kanannya (dx=1, dy=0).
        """
        # Kuantisasi dulu ke 8 level
        img_quant, levels = self.quantize_image(image, levels=8)
        h, w = img_quant.shape
        
        # Buat matriks kosong 8x8
        glcm = np.zeros((levels, levels), dtype=int)
        
        # Tentukan arah offset (sekarang kita set fix 0 derajat/horizontal)
        dx, dy = 1, 0  
        
        # Loop manual (mengisi matriks)
        for y in range(h - dy):
            for x in range(w - dx):
                i = img_quant[y, x]       # Nilai pixel saat ini
                j = img_quant[y+dy, x+dx] # Nilai pixel tetangga
                glcm[i, j] += 1
                
        # Normalisasi (agar jadi probabilitas, total = 1.0)
        glcm_sum = np.sum(glcm)
        if glcm_sum == 0:
            return glcm
        return glcm / glcm_sum

    def extract_glcm_features(self, image):
        """
        [MANUAL GLCM 3] Menghitung 4 statistik dasar dari matriks GLCM.
        Rumus diambil dari buku teks Haralick.
        """
        P = self.compute_glcm_matrix(image)
        levels = P.shape[0]
        
        contrast = 0.0
        energy = 0.0
        homogeneity = 0.0
        correlation = 0.0
        
        # Hitung mean & standar deviasi untuk korelasi
        i_indices = np.arange(levels).reshape(-1, 1)
        j_indices = np.arange(levels).reshape(1, -1)
        mean = np.sum(i_indices * P) # Asumsi mean_i ~ mean_j
        std = np.sqrt(np.sum((i_indices - mean)**2 * P))
        
        # Loop hitung fitur
        for i in range(levels):
            for j in range(levels):
                val = P[i, j]
                
                # 1. Contrast: (i-j)^2 * P[i,j]
                contrast += ((i - j) ** 2) * val
                
                # 2. Energy: Sum(P[i,j]^2)
                energy += val ** 2
                
                # 3. Homogeneity: P[i,j] / (1 + |i-j|)
                homogeneity += val / (1 + abs(i - j))
                
                # 4. Correlation: ((i-mean)*(j-mean)*P[i,j]) / std^2
                if std > 0:
                    correlation += ((i - mean) * (j - mean) * val) / (std ** 2)
                    
        return [contrast, energy, homogeneity, correlation]

    # ==========================================
    # BAGIAN 2: HOG (Histogram of Oriented Gradients)
    # ==========================================

    def compute_gradients_manual(self, image):
        """
        [MANUAL HOG 1] Menghitung Gradien (Gx, Gy), Magnitude, dan Angle.
        Tanpa sobel, pakai selisih biasa: I(x+1) - I(x-1).
        """
        image = image.astype(float)
        h, w = image.shape
        
        # Matriks kosong
        gx = np.zeros_like(image)
        gy = np.zeros_like(image)
        
        # Hitung selisih (Gradient)
        # Gx = kanan - kiri
        gx[:, 1:-1] = image[:, 2:] - image[:, :-2]
        # Gy = bawah - atas
        gy[1:-1, :] = image[2:, :] - image[:-2, :]
        
        # Magnitude (Kekuatan tepi) = sqrt(gx^2 + gy^2)
        magnitude = np.sqrt(gx**2 + gy**2)
        
        # Angle (Arah tepi) dalam derajat (0-180)
        angle = np.arctan2(gy, gx) * (180 / np.pi)
        angle[angle < 0] += 180 # Pastikan positif
        
        return magnitude, angle

    def extract_hog_features(self, image, cell_size=16, bin_count=9):
        """
        [MANUAL HOG 2] Membuat Histogram 9-bin dari Magnitude & Angle.
        Gambar dibagi jadi sel-sel kecil (misal 16x16 pixel).
        """
        mag, ang = self.compute_gradients_manual(image)
        h, w = image.shape
        
        # Hitung jumlah sel
        n_cell_y = h // cell_size
        n_cell_x = w // cell_size
        
        hog_features = []
        
        # Loop setiap sel (kotak kecil)
        for y in range(n_cell_y):
            for x in range(n_cell_x):
                # Ambil potongan magnitude & angle untuk sel ini
                cell_mag = mag[y*cell_size:(y+1)*cell_size, x*cell_size:(x+1)*cell_size]
                cell_ang = ang[y*cell_size:(y+1)*cell_size, x*cell_size:(x+1)*cell_size]
                
                # Buat histogram 9 bin (0, 20, 40 ... 160 derajat)
                hist = np.zeros(bin_count)
                
                # Isi bin (Voting)
                # Cara manual flattening loop
                for i in range(cell_size):
                    for j in range(cell_size):
                        m = cell_mag[i, j]
                        a = cell_ang[i, j]
                        
                        # Tentukan masuk bin mana
                        bin_idx = int(a // (180 / bin_count))
                        if bin_idx >= bin_count: bin_idx = bin_count - 1
                        
                        hist[bin_idx] += m
                
                # Normalisasi L2 per cell (agar terang/gelap tidak ngaruh)
                hist_norm = hist / (np.linalg.norm(hist) + 1e-5)
                hog_features.extend(hist_norm)
                
        return np.array(hog_features)

    # ==========================================
    # BAGIAN 3: SPATIAL GRIDDING (Penggabungan)
    # ==========================================
    
    def extract_full_features(self, image):
        """
        Fungsi Utama: Menggabungkan Global + Lokal (3x3 Grid)
        Sesuai Proposal:
        1. Fitur Global (1 gambar utuh) -> GLCM & HOG
        2. Fitur Lokal (Gambar dipotong 3x3) -> GLCM & HOG per potongan
        """
        feature_vector = []
        
        # --- A. Fitur Global ---
        # Untuk global HOG, kita resize kecil dulu biar tidak meledak fiturnya
        img_small = cv2.resize(image, (64, 64)) # Resize sementara untuk HOG global
        
        feat_glcm_global = self.extract_glcm_features(image)
        feat_hog_global = self.extract_hog_features(img_small, cell_size=16) # 16 histogram
        
        feature_vector.extend(feat_glcm_global)
        feature_vector.extend(feat_hog_global)
        
        # --- B. Fitur Lokal (Spatial Grid 3x3) ---
        h, w = image.shape
        step_h = h // 3
        step_w = w // 3
        
        for r in range(3):
            for c in range(3):
                # Potong grid
                y1, y2 = r*step_h, (r+1)*step_h
                x1, x2 = c*step_w, (c+1)*step_w
                sub_img = image[y1:y2, x1:x2]
                
                # Ekstraksi fitur sub-grid
                # Gunakan parameter lebih 'kasar' biar cepat
                f_glcm = self.extract_glcm_features(sub_img)
                
                # HOG lokal: resize sub-img jadi kecil agar ringan
                sub_img_small = cv2.resize(sub_img, (32, 32)) 
                f_hog = self.extract_hog_features(sub_img_small, cell_size=16)
                
                feature_vector.extend(f_glcm)
                feature_vector.extend(f_hog)
                
        return np.array(feature_vector)

# Perlu import cv2 di dalam method extract_full_features untuk resize utilitas
import cv2