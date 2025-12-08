import numpy as np
import cv2  # Hanya dipakai untuk I/O (baca/tulis gambar), bukan untuk algoritma
import math

class ManualPreprocessor:
    def __init__(self):
        pass

    def to_grayscale_manual(self, image):
        """
        [MANUAL 1] Konversi RGB ke Grayscale.
        Menggunakan rumus Luminosity: Gray = 0.299*R + 0.587*G + 0.114*B
        Dosen: "Kenapa tidak rata-rata biasa?"
        Jawab: "Karena mata manusia lebih sensitif terhadap warna hijau, Pak."
        """
        # Pisahkan channel warna
        B = image[:, :, 0].astype(float)
        G = image[:, :, 1].astype(float)
        R = image[:, :, 2].astype(float)
        
        # Hitung manual dot product
        gray = 0.299 * R + 0.587 * G + 0.114 * B
        
        return gray.astype(np.uint8)

    def gaussian_kernel_manual(self, size=5, sigma=1.0):
        """
        [MANUAL 2A] Membuat kernel Gaussian (Filter Penghalus) secara matematis.
        Ini menggantikan cv2.getGaussianKernel.
        """
        kernel = np.zeros((size, size))
        center = size // 2
        sum_val = 0

        for x in range(size):
            for y in range(size):
                diff = (x - center)**2 + (y - center)**2
                # Rumus Distribusi Normal (Gaussian)
                exponent = -(diff) / (2 * sigma**2)
                val = (1 / (2 * math.pi * sigma**2)) * math.exp(exponent)
                kernel[x, y] = val
                sum_val += val
        
        return kernel / sum_val # Normalisasi

    def convolution_manual(self, image, kernel):
        """
        [MANUAL 2B] Operasi Konvolusi Manual.
        Menggeser kernel di atas gambar pixel demi pixel.
        Ini menggantikan cv2.GaussianBlur atau cv2.filter2D.
        """
        h_img, w_img = image.shape
        k_h, k_w = kernel.shape
        
        pad_h = k_h // 2
        pad_w = k_w // 2
        
        # Padding manual (Zero Padding)
        padded_img = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
        output = np.zeros_like(image)
        
        # Loop manual (Algoritma inti Image Processing)
        for i in range(h_img):
            for j in range(w_img):
                region = padded_img[i:i+k_h, j:j+k_w]
                output[i, j] = np.sum(region * kernel)
                
        return output.astype(np.uint8)

    def crop_roi_manual(self, image_gray, threshold_value=45):
        """
        [MANUAL 3] Cropping Otak (ROI) tanpa cv2.findContours.
        Teknik: Projection Profile (Scan Baris & Kolom).
        Cara kerja: Cari baris/kolom pertama dan terakhir yang ada pixel putihnya.
        """
        # Binarisasi manual (Thresholding)
        binary_map = (image_gray > threshold_value).astype(int)
        
        # Scan horizontal & vertikal
        row_sum = np.sum(binary_map, axis=1)
        col_sum = np.sum(binary_map, axis=0)
        
        rows_with_data = np.where(row_sum > 0)[0]
        cols_with_data = np.where(col_sum > 0)[0]
        
        # Jika gambar gelap total, kembalikan apa adanya
        if len(rows_with_data) == 0:
            return image_gray 
            
        y_min, y_max = rows_with_data[0], rows_with_data[-1]
        x_min, x_max = cols_with_data[0], cols_with_data[-1]
        
        # Slicing Array (Potong)
        cropped = image_gray[y_min:y_max+1, x_min:x_max+1]
        
        return cropped

    def resize_padding_manual(self, image, target_size=224):
        """
        [MANUAL 4] Resize dengan Nearest Neighbor Interpolation + Padding.
        Ini menggantikan cv2.resize.
        Penting agar gambar tidak gepeng (sesuai proposal: Aspect Ratio Preserving).
        """
        h_src, w_src = image.shape
        target_h, target_w = target_size, target_size
        
        # Hitung skala agar muat di kotak 224x224
        scale = min(target_w / w_src, target_h / h_src)
        new_w = int(w_src * scale)
        new_h = int(h_src * scale)
        
        # Buat canvas kosong untuk gambar hasil resize
        resized_img = np.zeros((new_h, new_w), dtype=np.uint8)
        
        # Nearest Neighbor Algorithm
        x_ratio = w_src / new_w
        y_ratio = h_src / new_h
        
        for i in range(new_h):
            for j in range(new_w):
                src_y = int(i * y_ratio)
                src_x = int(j * x_ratio)
                # Kunci koordinat agar tidak error index out of bound
                src_y = min(src_y, h_src - 1)
                src_x = min(src_x, w_src - 1)
                resized_img[i, j] = image[src_y, src_x]
        
        # Padding (Menempelkan hasil resize ke tengah canvas hitam)
        final_image = np.zeros((target_h, target_w), dtype=np.uint8)
        y_offset = (target_h - new_h) // 2
        x_offset = (target_w - new_w) // 2
        
        final_image[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_img
        
        return final_image

    def normalize_manual(self, image):
        """
        [MANUAL 5] Normalisasi piksel ke range 0-1.
        """
        return image.astype(float) / 255.0
    

class ManualStandardScaler:
    """
    [MANUAL 6] Standard Scaler.
    Rumus: z = (x - mean) / std
    Fungsi: Menyamakan skala semua fitur agar SVM tidak bingung antara
    nilai GLCM (kecil) dan HOG (besar).
    """
    def __init__(self):
        self.mean = None
        self.std = None

    def fit(self, X):
        # Hitung rata-rata dan standar deviasi per kolom fitur
        self.mean = np.mean(X, axis=0)
        self.std = np.std(X, axis=0)
        # Hindari pembagian dengan nol
        self.std[self.std == 0] = 1.0

    def transform(self, X):
        if self.mean is None:
            raise Exception("Scaler belum di-fit!")
        return (X - self.mean) / self.std

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)