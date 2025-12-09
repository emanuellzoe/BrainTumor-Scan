// app/components/TumorDetector.tsx
"use client";

import React, { useState, useEffect, useMemo } from "react";

// Tipe data untuk hasil lengkap dari API
type AnalysisResult = {
  label: string;
  confidence: string;
  metadata: {
    original_dimensions: { width: number; height: number };
    preprocessed_dimensions: { width: number; height: number };
  };
  visualizations: {
    preprocessed: string;
    hog: string;
    glcm: string;
    pca: string | null;
  };
};

type Tab = "upload" | "preprocessing" | "features" | "pca" | "result";

const TABS: { id: Tab; title: string }[] = [
  { id: "upload", title: "1. Unggah Gambar" },
  { id: "preprocessing", title: "2. Pra-pemrosesan" },
  { id: "features", title: "3. Ekstraksi Fitur" },
  { id: "pca", title: "4. Reduksi Dimensi (PCA)" },
  { id: "result", title: "5. Hasil Prediksi" },
];

const TumorDetector = () => {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>("upload");

  const updateFile = (newFile: File | null) => {
    setFile(newFile);
    setAnalysisResult(null);
    setError(null);
    setActiveTab("upload");

    if (newFile) {
      const url = URL.createObjectURL(newFile);
      setPreview(url);
    } else {
      setPreview(null);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0] || null;
    updateFile(f);
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("Silakan pilih gambar MRI otak terlebih dahulu.");
      return;
    }

    setError(null);
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Ganti URL ini jika backend Anda berjalan di port yang berbeda
      const res = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || "Gagal memproses gambar di backend.");
      }

      const data = (await res.json()) as AnalysisResult;
      setAnalysisResult(data);
      setActiveTab("preprocessing"); // Langsung pindah ke tab pertama hasil
    } catch (err: any) {
      setError(err.message || "Terjadi kesalahan saat menghubungi API.");
    } finally {
      setLoading(false);
    }
  };
  
  const isTabDisabled = (tabId: Tab): boolean => {
    if (tabId === "upload") return false;
    return !analysisResult;
  };

  // Effect untuk paste gambar
  useEffect(() => {
    const handlePaste = (event: ClipboardEvent) => {
      const items = event.clipboardData?.items;
      if (items) {
        for (let i = 0; i < items.length; i++) {
          if (items[i].type.indexOf("image") !== -1) {
            const blob = items[i].getAsFile();
            if (blob) {
              const pastedFile = new File([blob], "pasted_image.png", { type: blob.type });
              updateFile(pastedFile);
              event.preventDefault(); // Mencegah default paste
              return;
            }
          }
        }
      }
    };

    document.addEventListener("paste", handlePaste);
    return () => {
      document.removeEventListener("paste", handlePaste);
    };
  }, []); // Hanya dijalankan sekali saat komponen dimuat

  const renderTabContent = () => {
    switch (activeTab) {
      case "upload":
        return (
          <div className="upload-container">
            <label className="upload-box">
              <input type="file" accept=".png,.jpg,.jpeg" onChange={handleFileChange} className="upload-input" />
              <div className="upload-inner">
                <div className="upload-icon">🧠</div>
                <p className="upload-title">Upload MRI Otak</p>
                <p className="upload-text">Klik di sini atau seret & jatuhkan gambar</p>
                <p className="upload-text-alt">Atau paste gambar dari clipboard!</p>
                {file && <p className="upload-file-name">File terpilih: <strong>{file.name}</strong></p>}
              </div>
            </label>
            {preview && (
              <div className="preview-card-small">
                 <h3 className="section-title-small">Preview</h3>
                <img src={preview} alt="MRI Preview" className="preview-image" />
              </div>
            )}
            <button onClick={handleAnalyze} className="primary-button" disabled={loading || !file}>
              {loading ? "Menganalisis..." : "Analisis Gambar"}
            </button>
          </div>
        );

      case "preprocessing":
        return (
          <div className="grid-container">
            <div className="visualization-card">
              <h3 className="section-title-small">Gambar Asli</h3>
              <img src={preview!} alt="Original MRI" className="preview-image" />
              {analysisResult?.metadata.original_dimensions && (
                <p className="desc-text">Dimensi: {analysisResult.metadata.original_dimensions.width}x{analysisResult.metadata.original_dimensions.height} px</p>
              )}
            </div>
            <div className="visualization-card">
              <h3 className="section-title-small">Hasil Pra-pemrosesan</h3>
              <img src={`data:image/png;base64,${analysisResult?.visualizations.preprocessed}`} alt="Preprocessed MRI" className="preview-image" />
              <p className="desc-text">Gambar diubah ke grayscale, diburamkan, dan ukurannya disesuaikan.</p>
               {analysisResult?.metadata.preprocessed_dimensions && (
                <p className="desc-text">Dimensi: {analysisResult.metadata.preprocessed_dimensions.width}x{analysisResult.metadata.preprocessed_dimensions.height} px</p>
              )}
            </div>
          </div>
        );
      
      case "features":
          return (
            <div className="grid-container">
              <div className="visualization-card">
                <h3 className="section-title-small">HOG (Histogram of Oriented Gradients)</h3>
                <img src={`data:image/png;base64,${analysisResult?.visualizations.hog}`} alt="HOG Visualization" className="preview-image" />
                <p className="desc-text">Visualisasi gradien atau tepi pada gambar untuk menangkap bentuk objek.</p>
              </div>
              <div className="visualization-card">
                <h3 className="section-title-small">GLCM (Gray-Level Co-occurrence Matrix)</h3>
                <img src={`data:image/png;base64,${analysisResult?.visualizations.glcm}`} alt="GLCM Visualization" className="preview-image" />
                <p className="desc-text">Matriks yang merepresentasikan hubungan tekstur antar piksel.</p>
              </div>
            </div>
          );

      case "pca":
        return (
           <div className="grid-container-single">
              <div className="visualization-card-large">
                <h3 className="section-title-small">PCA (Principal Component Analysis)</h3>
                {analysisResult?.visualizations.pca ? (
                  <>
                    <img src={`data:image/png;base64,${analysisResult?.visualizations.pca}`} alt="PCA Visualization" className="preview-image-large" />
                    <p className="desc-text">Fitur-fitur yang telah diekstraksi direduksi dimensinya untuk mengambil komponen yang paling penting.</p>
                  </>
                ) : (
                  <p className="preview-placeholder">PCA tidak digunakan dalam model ini.</p>
                )}
              </div>
            </div>
        );

      case "result":
        return (
            <div className="prediction-card-standalone">
              <h2 className="section-title">Hasil Akhir Klasifikasi</h2>
              {analysisResult ? (
                <div className="prediction-content">
                  <span className="label-pill">{analysisResult.label}</span>
                  <p className="prediction-text">Sistem memprediksi citra ini sebagai:</p>
                  <p className="prediction-main"><strong>{analysisResult.label}</strong></p>
                  <p className="confidence-text">Tingkat Keyakinan: <strong>{analysisResult.confidence}%</strong></p>
                </div>
              ) : (
                <p className="preview-placeholder">Hasil akan muncul di sini.</p>
              )}
            </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="page-root" style={{ minHeight: "calc(100vh - 120px)" }}>
      <div className="glass-card">
        <header className="header">
          <div>
            <h1 className="title">Brain Tumor AI-Analyzer</h1>
            <p className="subtitle">
              Platform analisis citra MRI untuk klasifikasi tumor otak menggunakan Machine Learning.
            </p>
          </div>
           <div className="badge">Gemini-Powered</div>
        </header>
        
        <nav className="tab-nav">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              className={`tab-button ${activeTab === tab.id ? "active" : ""}`}
              onClick={() => setActiveTab(tab.id)}
              disabled={isTabDisabled(tab.id)}
            >
              {tab.title}
            </button>
          ))}
        </nav>

        <main className="content">
          {error && <div className="error-alert">{error}</div>}
          {renderTabContent()}
        </main>
      </div>
    </div>
  );
};

export default TumorDetector;