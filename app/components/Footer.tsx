// app/components/Footer.tsx
"use client";

import React from "react";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer-root">
      <div className="footer-container">
        {/* Top Section */}
        <div className="footer-top">
          <div className="footer-brand">
            <div className="footer-logo">
              <span className="footer-logo-icon">🧠</span>
              <span className="footer-logo-text">BrainTumor-Scan</span>
            </div>
            <p className="footer-description">
              Revolutionizing medical imaging with AI-powered brain tumor
              detection. Fast, accurate, and accessible for healthcare
              professionals.
            </p>
          </div>

          <div className="footer-links-group">
            <div className="footer-column">
              <h3 className="footer-column-title">Product</h3>
              <a href="#features" className="footer-link">
                Features
              </a>
              <a href="#pricing" className="footer-link">
                Pricing
              </a>
              <a href="#api" className="footer-link">
                API
              </a>
              <a href="#docs" className="footer-link">
                Documentation
              </a>
            </div>

            <div className="footer-column">
              <h3 className="footer-column-title">Company</h3>
              <a href="#about" className="footer-link">
                About Us
              </a>
              <a href="#team" className="footer-link">
                Team
              </a>
              <a href="#careers" className="footer-link">
                Careers
              </a>
              <a href="#contact" className="footer-link">
                Contact
              </a>
            </div>

            <div className="footer-column">
              <h3 className="footer-column-title">Resources</h3>
              <a href="#blog" className="footer-link">
                Blog
              </a>
              <a href="#research" className="footer-link">
                Research
              </a>
              <a href="#support" className="footer-link">
                Support
              </a>
              <a href="#status" className="footer-link">
                Status
              </a>
            </div>
          </div>
        </div>

        {/* Divider */}
        <div className="footer-divider"></div>

        {/* Bottom Section */}
        <div className="footer-bottom">
          <div className="footer-legal">
            <p className="footer-copyright">
              © {currentYear} BrainTumor-Scan. All rights reserved.
            </p>
            <div className="footer-legal-links">
              <a href="#privacy" className="footer-legal-link">
                Privacy Policy
              </a>
              <span className="footer-separator">•</span>
              <a href="#terms" className="footer-legal-link">
                Terms of Service
              </a>
            </div>
          </div>

          <div className="footer-socials">
            <a
              href="https://github.com/emanuellzoe/BrainTumor-Scan"
              target="_blank"
              rel="noopener noreferrer"
              className="footer-social-link"
              aria-label="GitHub"
            >
              <svg
                viewBox="0 0 24 24"
                fill="currentColor"
                className="footer-social-icon"
              >
                <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.17 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.167 22 16.418 22 12c0-5.523-4.477-10-10-10z" />
              </svg>
            </a>
            <a
              href="#twitter"
              className="footer-social-link"
              aria-label="Twitter"
            >
              <svg
                viewBox="0 0 24 24"
                fill="currentColor"
                className="footer-social-icon"
              >
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
              </svg>
            </a>
            <a
              href="#linkedin"
              className="footer-social-link"
              aria-label="LinkedIn"
            >
              <svg
                viewBox="0 0 24 24"
                fill="currentColor"
                className="footer-social-icon"
              >
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
              </svg>
            </a>
          </div>
        </div>
      </div>

      <style jsx>{`
        .footer-root {
          background: linear-gradient(
              180deg,
              rgba(255, 255, 255, 0.05) 0%,
              rgba(43, 15, 11, 0.95) 100%
            ),
            radial-gradient(circle at bottom, #ff7b39 0%, #2b0f0b 70%);
          color: rgba(255, 255, 255, 0.9);
          padding: 4rem 1.5rem 2rem;
          margin-top: 4rem;
          position: relative;
          overflow: hidden;
        }

        .footer-root::before {
          content: "";
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 1px;
          background: linear-gradient(
            90deg,
            transparent 0%,
            rgba(255, 138, 61, 0.5) 50%,
            transparent 100%
          );
        }

        .footer-container {
          max-width: 75rem;
          margin: 0 auto;
        }

        .footer-top {
          display: grid;
          grid-template-columns: 1.5fr 1fr;
          gap: 4rem;
          margin-bottom: 3rem;
        }

        .footer-brand {
          max-width: 28rem;
        }

        .footer-logo {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 1rem;
        }

        .footer-logo-icon {
          font-size: 2rem;
          filter: drop-shadow(0 0 12px rgba(255, 138, 61, 0.6));
        }

        .footer-logo-text {
          font-size: 1.5rem;
          font-weight: 700;
          background: linear-gradient(135deg, #ff8a3d 0%, #ffb347 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .footer-description {
          font-size: 0.9375rem;
          line-height: 1.6;
          color: rgba(255, 255, 255, 0.7);
          margin: 0;
        }

        .footer-links-group {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 2rem;
        }

        .footer-column {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .footer-column-title {
          font-size: 0.875rem;
          font-weight: 600;
          color: #ff8a3d;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          margin: 0 0 0.5rem 0;
        }

        .footer-link {
          font-size: 0.9375rem;
          color: rgba(255, 255, 255, 0.7);
          text-decoration: none;
          transition: all 0.2s ease;
          width: fit-content;
        }

        .footer-link:hover {
          color: #ffb347;
          transform: translateX(4px);
        }

        .footer-divider {
          height: 1px;
          background: linear-gradient(
            90deg,
            transparent 0%,
            rgba(255, 138, 61, 0.3) 50%,
            transparent 100%
          );
          margin: 2rem 0;
        }

        .footer-bottom {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 2rem;
        }

        .footer-legal {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .footer-copyright {
          font-size: 0.875rem;
          color: rgba(255, 255, 255, 0.6);
          margin: 0;
        }

        .footer-legal-links {
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }

        .footer-legal-link {
          font-size: 0.875rem;
          color: rgba(255, 255, 255, 0.6);
          text-decoration: none;
          transition: color 0.2s ease;
        }

        .footer-legal-link:hover {
          color: #ff8a3d;
        }

        .footer-separator {
          color: rgba(255, 255, 255, 0.3);
        }

        .footer-socials {
          display: flex;
          gap: 1rem;
        }

        .footer-social-link {
          width: 2.5rem;
          height: 2.5rem;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          background: rgba(255, 138, 61, 0.1);
          border: 1px solid rgba(255, 138, 61, 0.3);
          color: rgba(255, 255, 255, 0.7);
          transition: all 0.3s ease;
        }

        .footer-social-link:hover {
          background: rgba(255, 138, 61, 0.2);
          border-color: #ff8a3d;
          color: #ffb347;
          transform: translateY(-2px);
        }

        .footer-social-icon {
          width: 1.25rem;
          height: 1.25rem;
        }

        @media (max-width: 1024px) {
          .footer-top {
            grid-template-columns: 1fr;
            gap: 3rem;
          }

          .footer-links-group {
            grid-template-columns: repeat(3, 1fr);
          }
        }

        @media (max-width: 768px) {
          .footer-root {
            padding: 3rem 1rem 1.5rem;
          }

          .footer-links-group {
            grid-template-columns: 1fr;
            gap: 2rem;
          }

          .footer-bottom {
            flex-direction: column;
            align-items: flex-start;
            gap: 1.5rem;
          }

          .footer-legal {
            width: 100%;
          }
        }
      `}</style>
    </footer>
  );
};

export default Footer;
