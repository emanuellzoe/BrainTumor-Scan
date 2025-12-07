import Header from './components/Header';
import Footer from './components/Footer';
import TumorDetector from './components/TumorDetector';

export default function HomePage() {
  return (
    <div>
      <Header />
      <main>
        <TumorDetector />
      </main>
      <Footer />
    </div>
  );
}
