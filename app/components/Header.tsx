// app/components/Header.tsx
"use client";

import React from "react";

const Header = () => {
  return (
    <header className="header-root">
      <div className="header-container">
        <div className="header-content">
          {/* Logo Section */}
          <div className="logo-section">
            <div className="logo-icon">🧠</div>
            <div className="logo-text">
              <h1 className="logo-title">BrainTumor-Scan</h1>
              <p className="logo-subtitle">AI-Powered Medical Imaging</p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="nav-links">
            <a href="#features" className="nav-link">
              Features
            </a>
            <a href="#about" className="nav-link">
              About
            </a>
            <a href="#contact" className="nav-link">
              Contact
            </a>
          </nav>

          {/* CTA Button */}
          <button className="header-cta-button">
            <span className="cta-icon">✨</span>
            Get Started
          </button>
        </div>
      </div>

      <style jsx>{`
        .header-root {
          position: sticky;
          top: 0;
          z-index: 50;
          background: rgba(255, 255, 255, 0.85);
          backdrop-filter: blur(12px);
          border-bottom: 1px solid rgba(255, 138, 61, 0.15);
          box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
        }

        .header-container {
          max-width: 75rem;
          margin: 0 auto;
          padding: 0 1.5rem;
        }

        .header-content {
          display: flex;
          align-items: center;
          justify-content: space-between;
          height: 4.5rem;
          gap: 2rem;
        }

        .logo-section {
          display: flex;
          align-items: center;
          gap: 0.875rem;
          cursor: pointer;
          transition: transform 0.2s ease;
        }

        .logo-section:hover {
          transform: translateY(-1px);
        }

        .logo-icon {
          font-size: 2rem;
          filter: drop-shadow(0 2px 8px rgba(255, 123, 57, 0.3));
          animation: pulse 3s ease-in-out infinite;
        }

        @keyframes pulse {
          0%,
          100% {
            transform: scale(1);
          }
          50% {
            transform: scale(1.05);
          }
        }

        .logo-text {
          display: flex;
          flex-direction: column;
          gap: 0.125rem;
        }

        .logo-title {
          font-size: 1.25rem;
          font-weight: 700;
          background: linear-gradient(135deg, #ff5b2a 0%, #ff8a3d 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          margin: 0;
          letter-spacing: -0.02em;
        }

        .logo-subtitle {
          font-size: 0.75rem;
          color: #7a5035;
          margin: 0;
          font-weight: 500;
        }

        .nav-links {
          display: flex;
          align-items: center;
          gap: 2rem;
          flex: 1;
          justify-content: center;
        }

        .nav-link {
          font-size: 0.9375rem;
          font-weight: 500;
          color: #5b3425;
          text-decoration: none;
          position: relative;
          transition: color 0.2s ease;
        }

        .nav-link::after {
          content: "";
          position: absolute;
          bottom: -0.375rem;
          left: 0;
          width: 0;
          height: 2px;
          background: linear-gradient(90deg, #ff5b2a, #ff8a3d);
          transition: width 0.3s ease;
        }

        .nav-link:hover {
          color: #ff5b2a;
        }

        .nav-link:hover::after {
          width: 100%;
        }

        .header-cta-button {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.625rem 1.5rem;
          border: none;
          border-radius: 624.9375rem;
          background: linear-gradient(135deg, #ff8a3d, #ff5b2a);
          color: white;
          font-weight: 600;
          font-size: 0.9375rem;
          cursor: pointer;
          box-shadow: 0 4px 16px rgba(255, 91, 42, 0.3);
          transition: all 0.2s ease;
        }

        .header-cta-button:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 24px rgba(255, 91, 42, 0.4);
        }

        .cta-icon {
          font-size: 1rem;
          animation: sparkle 2s ease-in-out infinite;
        }

        @keyframes sparkle {
          0%,
          100% {
            opacity: 1;
            transform: scale(1);
          }
          50% {
            opacity: 0.7;
            transform: scale(1.15);
          }
        }

        @media (max-width: 768px) {
          .nav-links {
            display: none;
          }

          .header-content {
            gap: 1rem;
          }

          .logo-title {
            font-size: 1.125rem;
          }

          .header-cta-button {
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
          }
        }
      `}</style>
    </header>
  );
};

export default Header;
