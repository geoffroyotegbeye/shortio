import { Link, useLocation } from 'react-router-dom';
import { Video, Sparkles } from 'lucide-react';

export default function Header() {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="bg-gray-900/80 backdrop-blur-sm border-b border-gray-800 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2 group">
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-2 rounded-lg group-hover:scale-110 transition-transform duration-200">
              <Video size={24} className="text-white" />
            </div>
            <span className="text-xl font-bold text-white">VideoAI Studio</span>
          </Link>

          <nav className="flex items-center gap-1">
            <Link
              to="/"
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                isActive('/')
                  ? 'bg-gray-800 text-white'
                  : 'text-gray-400 hover:text-white hover:bg-gray-800/50'
              }`}
            >
              Accueil
            </Link>
            <Link
              to="/generate"
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center gap-2 ${
                isActive('/generate')
                  ? 'bg-gray-800 text-white'
                  : 'text-gray-400 hover:text-white hover:bg-gray-800/50'
              }`}
            >
              <Sparkles size={16} />
              Générer Vidéo
            </Link>
            <Link
              to="/subtitles"
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                isActive('/subtitles')
                  ? 'bg-gray-800 text-white'
                  : 'text-gray-400 hover:text-white hover:bg-gray-800/50'
              }`}
            >
              Sous-titres
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
}