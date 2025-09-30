import { useState } from 'react';
import { Sparkles } from 'lucide-react';
import { FaDice } from 'react-icons/fa'; // Importer l'icône de dé
import type { VideoGenerationRequest } from '../types/video';

interface ConfigurationFormProps {
  onSubmit: (data: VideoGenerationRequest) => void;
  isLoading: boolean;
}

export default function ConfigurationForm({ onSubmit, isLoading }: ConfigurationFormProps) {
  const [concept, setConcept] = useState('');
  const [nImages, setNImages] = useState(3);
  const [category, setCategory] = useState<'astuce' | 'motivation' | 'lifestyle'>('astuce');
  const [lang, setLang] = useState<'fr' | 'en'>('fr');

  const examplePrompts = [
    "Une astuce de productivité pour arrêter de procrastiner",
    "L'histoire surprenante derrière un objet du quotidien",
    "Trois faits psychologiques qui vont vous étonner",
    "Comment la motivation fonctionne réellement, selon la science",
    "Une recette simple et rapide pour un repas sain en moins de 15 minutes",
    "Le secret pour se réveiller plein d'énergie tous les matins",
    "Un exercice de respiration de 2 minutes pour calmer l'anxiété instantanément"
  ];

  const generateRandomPrompt = () => {
    const randomIndex = Math.floor(Math.random() * examplePrompts.length);
    setConcept(examplePrompts[randomIndex]);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (concept.trim()) {
      onSubmit({ prompt: concept, n_images: nImages, category, lang });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-800 rounded-xl p-6 space-y-6">
      <div>
        <div className="flex justify-between items-center mb-2">
          <label htmlFor="concept" className="block text-sm font-medium text-gray-300">
            Concept de la vidéo <span className="text-red-400">*</span>
          </label>
          <button
            type="button"
            onClick={generateRandomPrompt}
            className="text-gray-400 hover:text-blue-400 transition-colors duration-200 flex items-center gap-1 text-xs"
            title="Générer une idée aléatoire"
          >
            <FaDice />
            Idée aléatoire
          </button>
        </div>
        <textarea
          id="concept"
          value={concept}
          onChange={(e) => setConcept(e.target.value)}
          placeholder="Ex: Une astuce incroyable pour apprendre une nouvelle langue..."
          className="w-full bg-gray-900 border border-gray-700 text-white rounded-lg px-4 py-3 min-h-[120px] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-500"
          required
        />
      </div>

      <div className="border-t border-gray-700 pt-6">
        <h3 className="text-sm font-medium text-gray-300 mb-4">Options avancées</h3>

        <div className="space-y-4">
          <div>
            <label htmlFor="images" className="block text-sm font-medium text-gray-400 mb-2">
              Nombre d'images: {nImages}
            </label>
            <input
              type="range"
              id="images"
              min="1"
              max="5"
              value={nImages}
              onChange={(e) => setNImages(Number(e.target.value))}
              className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>1</span>
              <span>5</span>
            </div>
          </div>

          <div>
            <label htmlFor="category" className="block text-sm font-medium text-gray-400 mb-2">
              Catégorie
            </label>
            <select
              id="category"
              value={category}
              onChange={(e) => setCategory(e.target.value as 'astuce' | 'motivation' | 'lifestyle')}
              className="w-full bg-gray-900 border border-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="astuce">Astuce</option>
              <option value="motivation">Motivation</option>
              <option value="lifestyle">Lifestyle</option>
            </select>
          </div>

          <div>
            <label htmlFor="lang" className="block text-sm font-medium text-gray-400 mb-2">
              Langue
            </label>
            <select
              id="lang"
              value={lang}
              onChange={(e) => setLang(e.target.value as 'fr' | 'en')}
              className="w-full bg-gray-900 border border-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="fr">Français</option>
              <option value="en">Anglais</option>
            </select>
          </div>
        </div>
      </div>

      <button
        type="submit"
        disabled={!concept.trim() || isLoading}
        className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 px-6 rounded-lg font-medium hover:from-blue-600 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
      >
        <Sparkles size={20} />
        Générer la vidéo
      </button>
    </form>
  );
}