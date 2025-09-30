import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import GenerateVideo from './pages/GenerateVideo';
import Subtitles from './pages/Subtitles';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen">
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/generate" element={<GenerateVideo />} />
          <Route path="/subtitles" element={<Subtitles />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
