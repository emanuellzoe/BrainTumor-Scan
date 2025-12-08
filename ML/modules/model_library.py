from sklearn.svm import SVC
import pickle

class LibrarySVM:
    """
    Wrapper sederhana untuk Scikit-Learn SVM.
    Menggunakan Kernel RBF (Non-linear) yang lebih canggih.
    """
    def __init__(self):
        self.model = SVC(kernel='rbf', C=1.0, probability=True, random_state=42)

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)
    
    def predict_proba(self, X):
        return self.model.predict_proba(X)

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.model, f)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)