import numpy as np
import pickle

class ManualLinearSVM:
    """
    Logika SVM Biner (2 Kelas) dari Nol.
    Menggunakan rumus: w = w - learning_rate * (2 * lambda * w - x * y)
    """
    def __init__(self, learning_rate=0.001, lambda_param=0.01, n_iters=1000):
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.w = None
        self.b = None

    def fit(self, X, y):
        # Ubah label 0/1 menjadi -1/1 (Format wajib SVM)
        y_ = np.where(y <= 0, -1, 1)
        n_samples, n_features = X.shape
        
        self.w = np.zeros(n_features)
        self.b = 0

        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                # Cek kondisi margin
                condition = y_[idx] * (np.dot(x_i, self.w) - self.b) >= 1
                if condition:
                    self.w -= self.lr * (2 * self.lambda_param * self.w)
                else:
                    self.w -= self.lr * (2 * self.lambda_param * self.w - np.dot(x_i, y_[idx]))
                    self.b -= self.lr * y_[idx]

    def predict(self, X):
        approx = np.dot(X, self.w) - self.b
        return np.sign(approx)

class ManualMulticlassSVM:
    """
    Wrapper untuk 4 Kelas (Glioma, Meningioma, dll).
    Menggunakan strategi One-vs-Rest (1 lawan Sisanya).
    """
    def __init__(self, n_classes=4, n_iters=1000):
        self.models = []
        self.n_classes = n_classes
        self.n_iters = n_iters

    def fit(self, X, y):
        self.models = []
        print(f"   [MANUAL] Melatih {self.n_classes} model sub-SVM...")
        for i in range(self.n_classes):
            # Buat label biner: Kelas 'i' jadi 1, sisanya -1
            y_binary = np.where(y == i, 1, -1)
            svm = ManualLinearSVM(n_iters=self.n_iters)
            svm.fit(X, y_binary)
            self.models.append(svm)

    def predict(self, X):
        # Ambil skor tertinggi dari 4 model
        pred_scores = self.decision_function(X)
        return np.argmax(pred_scores, axis=1)

    def decision_function(self, X):
        """
        Mengembalikan skor mentah (jarak ke hyperplane) untuk setiap kelas.
        Penting untuk ROC-AUC.
        """
        pred_scores = np.zeros((X.shape[0], self.n_classes))
        for idx, model in enumerate(self.models):
            pred_scores[:, idx] = np.dot(X, model.w) - model.b
        return pred_scores

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)