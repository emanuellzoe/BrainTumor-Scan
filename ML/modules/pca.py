import numpy as np
import pickle

class ManualPCA:
    """
    Implementasi PCA Manual menggunakan Eigen Decomposition.
    Tujuan: Mereduksi dimensi data tapi tetap mempertahankan informasi (variance).
    """
    def __init__(self, n_components=0.95):
        # Jika n_components float (0.0 - 1.0), berarti % varians yang dijaga.
        # Jika int (> 1), berarti jumlah fitur pasti yang diambil.
        self.n_components = n_components
        self.components = None
        self.mean = None
        self.explained_variance_ratio_ = None

    def fit(self, X):
        # 1. Hitung Rata-rata (Mean Centering)
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean

        # 2. Hitung Covariance Matrix
        # Rumus: (X^T * X) / (n - 1)
        n_samples = X.shape[0]
        cov_matrix = np.dot(X_centered.T, X_centered) / (n_samples - 1)

        # 3. Hitung Eigenvalues dan Eigenvectors
        # Ini adalah inti matematika PCA
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

        # 4. Urutkan dari yang terbesar (Desc)
        sorted_index = np.argsort(eigenvalues)[::-1]
        sorted_eigenvalues = eigenvalues[sorted_index]
        sorted_eigenvectors = eigenvectors[:, sorted_index]

        # 5. Tentukan berapa komponen yang diambil
        if isinstance(self.n_components, float):
            # Hitung kumulatif varians (Total info)
            total_eigenvalues = np.sum(sorted_eigenvalues)
            var_explained = sorted_eigenvalues / total_eigenvalues
            cum_var_explained = np.cumsum(var_explained)
            
            # Cari indeks di mana varians >= n_components (misal 0.95)
            # np.argmax akan berhenti di True pertama
            num_components = np.argmax(cum_var_explained >= self.n_components) + 1
            print(f"   [PCA Auto] Memilih {num_components} komponen untuk cover {self.n_components*100}% varians.")
        else:
            num_components = self.n_components

        # 6. Simpan Komponen Utama (W)
        self.components = sorted_eigenvectors[:, :num_components]
        self.explained_variance_ratio_ = sorted_eigenvalues[:num_components] / np.sum(sorted_eigenvalues)

    def transform(self, X):
        # Proyeksikan data ke ruang fitur baru
        # Rumus: X_new = (X - mean) dot Components
        X_centered = X - self.mean
        return np.dot(X_centered, self.components)

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)