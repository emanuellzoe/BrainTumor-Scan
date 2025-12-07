"use client";

import React, { useState } from "react";

type PredictionResult = {
  label: string;
  confidence: number;
};

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0] || null;
    setFile(f);
    setResult(null);
    setError(null);

    if (f) {
      const url = URL.createObjectURL(f);
      setPreview(url);
    } else {
      setPreview(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    if (!file) {
      setError("Silakan pilih gambar MRI otak terlebih dahulu.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const res = await fetch("/api/predict", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "Gagal memproses gambar.");
      }

      const data = (await res.json()) as PredictionResult;
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Terjadi kesalahan.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="page-root">
      <div className="glass-card">
        <header className="header">
          <div>
            <h1 className="title">Medical Brain Tumor Scan</h1>
            <p className="subtitle">
              Upload citra MRI otak, lalu sistem akan mengidentifikasi kategori
              tumor: <strong>Glioma</strong>, <strong>Meningioma</strong>,{" "}
              <strong>Pituitary</strong>, atau <strong>No Tumor</strong>.
            </p>
          </div>
          <div className="badge">Brain Scan AI</div>
        </header>

        <section className="content">
          <form className="upload-section" onSubmit={handleSubmit}>
            <label className="upload-box">
              <input
                type="file"
                accept=".png,.jpg,.jpeg"
                onChange={handleFileChange}
                className="upload-input"
              />
              <div className="upload-inner">
                <div className="upload-icon">🧠</div>
                <p className="upload-title">Upload MRI Otak</p>
                <p className="upload-text">
                  Klik di sini atau seret &amp; jatuhkan gambar (.png, .jpg, .jpeg)
                </p>
                {file && (
                  <p className="upload-file-name">
                    File terpilih: <strong>{file.name}</strong>
                  </p>
                )}
              </div>
            </label>

            <button type="submit" className="primary-button" disabled={loading}>
              {loading ? "Menganalisis..." : "Analisis Gambar"}
            </button>

            {error && <div className="error-alert">{error}</div>}
          </form>

          <div className="result-section">
            <div className="preview-card">
              <h2 className="section-title">Input Otak (MRI)</h2>
              <div className="preview-area">
                {preview ? (
                  <img
                    src={preview}
                    alt="MRI Preview"
                    className="preview-image"
                  />
                ) : (
                  <p className="preview-placeholder">
                    Belum ada gambar yang diupload.
                  </p>
                )}
              </div>
            </div>

            <div className="prediction-card">
              <h2 className="section-title">Hasil Klasifikasi</h2>
              {result ? (
                <div className="prediction-content">
                  <span className="label-pill">{result.label}</span>
                  <p className="prediction-text">
                    Sistem memprediksi bahwa citra MRI ini termasuk ke dalam
                    kategori:
                  </p>
                  <p className="prediction-main">
                    <strong>{result.label}</strong>
                  </p>
                  <p className="confidence-text">
                    Perkiraan confidence:{" "}
                    <strong>{(result.confidence * 100).toFixed(2)}%</strong>
                  </p>
                </div>
              ) : (
                <p className="preview-placeholder">
                  Hasil klasifikasi akan muncul di sini setelah analisis.
                </p>
              )}
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
