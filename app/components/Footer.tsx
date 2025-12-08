// app/components/Footer.tsx
import React from 'react';

const Footer = () => {
  return (
    <footer style={{ backgroundColor: '#222', color: 'white', padding: '1rem', textAlign: 'center', position: 'relative', bottom: 0, width: '100%' }}>
      <p>&copy; {new Date().getFullYear()} Brain Scan. All Rights Reserved.</p>
    </footer>
  );
};

export default Footer;
