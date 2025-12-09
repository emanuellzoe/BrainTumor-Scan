// app/components/TumorDetector.tsx
"use client";

import React, { useState, useEffect } from "react";

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

const TABS: { id: Tab; title: string; icon: string }[] = [
  { id: "upload", title: "Upload Image", icon: "📤" },
  { id: "preprocessing", title: "Preprocessing", icon: "⚙️" },
  { id: "features", title: "Feature Extraction", icon: "🔍" },
  { id: "pca", title: "PCA Analysis", icon: "📊" },
  { id: "result", title: "Prediction", icon: "🎯" },
];

const TumorDetector = () => {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(
    null
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>("upload");
  const [progress, setProgress] = useState(0);

  const updateFile = (newFile: File | null) => {
    setFile(newFile);
    setAnalysisResult(null);
    setError(null);
    setActiveTab("upload");
    setProgress(0);

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
      setError("Please select a brain MRI image first.");
      return;
    }

    setError(null);
    setLoading(true);
    setProgress(0);

    // Simulate progress
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return prev;
        }
        return prev + 10;
      });
    }, 200);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || "Failed to process image.");
      }

      const data = (await res.json()) as AnalysisResult;
      setProgress(100);
      setAnalysisResult(data);

      // Auto-navigate to preprocessing after 500ms
      setTimeout(() => {
        setActiveTab("preprocessing");
      }, 500);
    } catch (err: any) {
      setError(err.message || "An error occurred while contacting the API.");
    } finally {
      clearInterval(progressInterval);
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
              const pastedFile = new File([blob], "pasted_image.png", {
                type: blob.type,
              });
              updateFile(pastedFile);
              event.preventDefault();
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
  }, []);

  const renderTabContent = () => {
    switch (activeTab) {
      case "upload":
        return (
          <div className="upload-container">
            <label className="upload-box">
              <input
                type="file"
                accept=".png,.jpg,.jpeg"
                onChange={handleFileChange}
                className="upload-input"
              />
              <div className="upload-inner">
                <div className="upload-icon">🧠</div>
                <p className="upload-title">Upload Brain MRI</p>
                <p className="upload-text">
                  Click here or drag & drop your image
                </p>
                <p className="upload-text-alt">
                  You can also paste from clipboard (Ctrl+V)
                </p>
                {file && (
                  <p className="upload-file-name">
                    Selected: <strong>{file.name}</strong>
                  </p>
                )}
              </div>
            </label>

            {preview && (
              <div className="preview-card-small">
                <h3 className="section-title-small">Preview</h3>
                <img
                  src={preview}
                  alt="MRI Preview"
                  className="preview-image"
                />
              </div>
            )}

            <button
              onClick={handleAnalyze}
              className="primary-button"
              disabled={loading || !file}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing...
                </>
              ) : (
                <>
                  <span>🔬</span>
                  Start Analysis
                </>
              )}
            </button>

            {loading && (
              <div className="progress-container">
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
                <p className="progress-text">{progress}% Complete</p>
              </div>
            )}
          </div>
        );

      case "preprocessing":
        return (
          <div className="grid-container">
            <div className="visualization-card">
              <h3 className="section-title-small">Original Image</h3>
              <img
                src={preview!}
                alt="Original MRI"
                className="preview-image"
              />
              {analysisResult?.metadata.original_dimensions && (
                <p className="desc-text">
                  Dimensions:{" "}
                  {analysisResult.metadata.original_dimensions.width}x
                  {analysisResult.metadata.original_dimensions.height} px
                </p>
              )}
            </div>
            <div className="visualization-card">
              <h3 className="section-title-small">Preprocessed Result</h3>
              <img
                src={`data:image/png;base64,${analysisResult?.visualizations.preprocessed}`}
                alt="Preprocessed MRI"
                className="preview-image"
              />
              <p className="desc-text">
                Image converted to grayscale, blurred, and resized for optimal
                processing.
              </p>
              {analysisResult?.metadata.preprocessed_dimensions && (
                <p className="desc-text">
                  Dimensions:{" "}
                  {analysisResult.metadata.preprocessed_dimensions.width}x
                  {analysisResult.metadata.preprocessed_dimensions.height} px
                </p>
              )}
            </div>
          </div>
        );

      case "features":
        return (
          <div className="grid-container">
            <div className="visualization-card">
              <h3 className="section-title-small">
                HOG (Histogram of Oriented Gradients)
              </h3>
              <img
                src={`data:image/png;base64,${analysisResult?.visualizations.hog}`}
                alt="HOG Visualization"
                className="preview-image"
              />
              <p className="desc-text">
                Visualizes gradient directions to capture object shapes and
                contours in the image.
              </p>
            </div>
            <div className="visualization-card">
              <h3 className="section-title-small">
                GLCM (Gray-Level Co-occurrence Matrix)
              </h3>
              <img
                src={`data:image/png;base64,${analysisResult?.visualizations.glcm}`}
                alt="GLCM Visualization"
                className="preview-image"
              />
              <p className="desc-text">
                Matrix representing texture relationships between neighboring
                pixels.
              </p>
            </div>
          </div>
        );

      case "pca":
        return (
          <div className="grid-container-single">
            <div className="visualization-card-large">
              <h3 className="section-title-small">
                PCA (Principal Component Analysis)
              </h3>
              {analysisResult?.visualizations.pca ? (
                <>
                  <img
                    src={`data:image/png;base64,${analysisResult?.visualizations.pca}`}
                    alt="PCA Visualization"
                    className="preview-image-large"
                  />
                  <p className="desc-text">
                    Dimensionality reduction technique extracting the most
                    significant components from feature space.
                  </p>
                </>
              ) : (
                <div className="pca-not-used">
                  <span className="pca-icon">📊</span>
                  <p className="preview-placeholder">
                    PCA analysis is not utilized in this model configuration.
                  </p>
                </div>
              )}
            </div>
          </div>
        );

      case "result":
        return (
          <div className="prediction-card-standalone">
            <h2 className="section-title">Final Classification Result</h2>
            {analysisResult ? (
              <div className="prediction-content">
                <div className="result-icon">
                  {analysisResult.label.toLowerCase().includes("tumor")
                    ? "🔴"
                    : "🟢"}
                </div>
                <span className="label-pill">{analysisResult.label}</span>
                <p className="prediction-text">
                  The system predicts this image as:
                </p>
                <p className="prediction-main">
                  <strong>{analysisResult.label}</strong>
                </p>
                <div className="confidence-container">
                  <p className="confidence-text">
                    Confidence Level:{" "}
                    <strong>{analysisResult.confidence}%</strong>
                  </p>
                  <div className="confidence-bar">
                    <div
                      className="confidence-fill"
                      style={{
                        width: `${analysisResult.confidence}%`,
                      }}
                    ></div>
                  </div>
                </div>

                <button
                  onClick={() => {
                    setActiveTab("upload");
                    updateFile(null);
                  }}
                  className="secondary-button"
                >
                  Analyze New Image
                </button>
              </div>
            ) : (
              <p className="preview-placeholder">Results will appear here.</p>
            )}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="page-root">
      <div className="glass-card">
        <header className="header">
          <div>
            <h1 className="title">Brain Tumor AI-Analyzer</h1>
            <p className="subtitle">
              Advanced medical imaging platform for brain tumor classification
              using state-of-the-art Machine Learning.
            </p>
          </div>
          <div className="badge">Machine Learning Grup A</div>
        </header>

        <nav className="tab-nav">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              className={`tab-button ${activeTab === tab.id ? "active" : ""}`}
              onClick={() => setActiveTab(tab.id)}
              disabled={isTabDisabled(tab.id)}
            >
              <span className="tab-icon">{tab.icon}</span>
              {tab.title}
            </button>
          ))}
        </nav>

        <main className="content">
          {error && (
            <div className="error-alert">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}
          {renderTabContent()}
        </main>
      </div>

      <style jsx>{`
        .spinner {
          display: inline-block;
          width: 1rem;
          height: 1rem;
          border: 2px solid rgba(255, 255, 255, 0.3);
          border-top-color: white;
          border-radius: 50%;
          animation: spin 0.6s linear infinite;
        }

        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }

        .tab-icon {
          font-size: 1.125rem;
          margin-right: 0.5rem;
        }

        .error-alert {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .error-icon {
          font-size: 1.25rem;
        }

        .progress-container {
          width: 100%;
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .progress-bar {
          width: 100%;
          height: 0.5rem;
          background: rgba(255, 138, 61, 0.2);
          border-radius: 624.9375rem;
          overflow: hidden;
        }

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, #ff5b2a, #ff8a3d);
          transition: width 0.3s ease;
          border-radius: 624.9375rem;
        }

        .progress-text {
          text-align: center;
          font-size: 0.875rem;
          font-weight: 600;
          color: #7a5035;
        }

        .result-icon {
          font-size: 4rem;
          margin-bottom: 1rem;
        }

        .confidence-container {
          width: 100%;
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          margin-top: 1rem;
        }

        .confidence-bar {
          width: 100%;
          height: 0.75rem;
          background: rgba(255, 138, 61, 0.15);
          border-radius: 624.9375rem;
          overflow: hidden;
          border: 1px solid rgba(255, 138, 61, 0.3);
        }

        .confidence-fill {
          height: 100%;
          background: linear-gradient(90deg, #ff5b2a, #ff8a3d, #ffb347);
          transition: width 0.5s ease;
          border-radius: 624.9375rem;
        }

        .secondary-button {
          margin-top: 1.5rem;
          padding: 0.75rem 2rem;
          border: 2px solid #ff8a3d;
          background: transparent;
          color: #ff5b2a;
          font-weight: 700;
          font-size: 0.9375rem;
          border-radius: 624.9375rem;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .secondary-button:hover {
          background: linear-gradient(135deg, #ff8a3d, #ff5b2a);
          color: white;
          transform: translateY(-2px);
          box-shadow: 0 0.5rem 1.25rem rgba(255, 91, 42, 0.3);
        }

        .pca-not-used {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 1rem;
          padding: 3rem 2rem;
        }

        .pca-icon {
          font-size: 4rem;
          opacity: 0.6;
        }
      `}</style>
    </div>
  );
};

export default TumorDetector;
