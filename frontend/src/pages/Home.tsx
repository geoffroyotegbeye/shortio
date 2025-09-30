import { Link } from 'react-router-dom';
import { Sparkles, FileVideo, ArrowRight } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-[calc(100vh-4rem)] bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
            Créez des Vidéos Exceptionnelles
            <span className="block mt-2 bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
              Avec l'Intelligence Artificielle
            </span>
          </h1>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Générez des vidéos captivantes ou ajoutez des sous-titres dynamiques à vos contenus existants
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          <Link
            to="/generate"
            className="group bg-gray-800 rounded-2xl p-8 border-2 border-gray-700 hover:border-blue-500 transition-all duration-300 hover:scale-105"
          >
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 w-16 h-16 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-200">
              <Sparkles size={32} className="text-white" />
            </div>

            <h2 className="text-2xl font-bold text-white mb-3">
              Générer une Vidéo IA
            </h2>
            <p className="text-gray-400 mb-6">
              Transformez vos idées en vidéos courtes captivantes. Entrez simplement un concept et laissez l'IA créer votre contenu.
            </p>

            <div className="flex items-center gap-2 text-blue-400 font-medium group-hover:gap-3 transition-all duration-200">
              Commencer
              <ArrowRight size={20} />
            </div>
          </Link>

          <Link
            to="/subtitles"
            className="group bg-gray-800 rounded-2xl p-8 border-2 border-gray-700 hover:border-purple-500 transition-all duration-300 hover:scale-105"
          >
            <div className="bg-gradient-to-r from-purple-500 to-pink-600 w-16 h-16 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-200">
              <FileVideo size={32} className="text-white" />
            </div>

            <h2 className="text-2xl font-bold text-white mb-3">
              Ajouter des Sous-titres
            </h2>
            <p className="text-gray-400 mb-6">
              Uploadez votre vidéo et ajoutez des sous-titres dynamiques personnalisés. Choisissez la position et le style qui vous conviennent.
            </p>

            <div className="flex items-center gap-2 text-purple-400 font-medium group-hover:gap-3 transition-all duration-200">
              Commencer
              <ArrowRight size={20} />
            </div>
          </Link>
        </div>

        <div className="mt-20 text-center">
          <h3 className="text-2xl font-bold text-white mb-8">Pourquoi VideoAI Studio ?</h3>
          <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            <div className="bg-gray-800/50 rounded-xl p-6">
              <div className="text-3xl mb-3">⚡</div>
              <h4 className="text-lg font-semibold text-white mb-2">Rapide</h4>
              <p className="text-gray-400 text-sm">
                Génération en quelques secondes seulement
              </p>
            </div>
            <div className="bg-gray-800/50 rounded-xl p-6">
              <div className="text-3xl mb-3">🎨</div>
              <h4 className="text-lg font-semibold text-white mb-2">Personnalisable</h4>
              <p className="text-gray-400 text-sm">
                Contrôlez chaque aspect de vos créations
              </p>
            </div>
            <div className="bg-gray-800/50 rounded-xl p-6">
              <div className="text-3xl mb-3">🚀</div>
              <h4 className="text-lg font-semibold text-white mb-2">Professionnel</h4>
              <p className="text-gray-400 text-sm">
                Qualité production pour tous vos projets
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}