import { Film } from 'lucide-react';

export default function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="bg-gray-800 rounded-full p-6 mb-4">
        <Film size={48} className="text-blue-500" />
      </div>
      <h3 className="text-xl font-semibold text-gray-200 mb-2">
        Créez votre première vidéo
      </h3>
      <p className="text-gray-400 max-w-md">
        Entrez un concept créatif et laissez l'IA générer une vidéo courte captivante pour vous.
      </p>
    </div>
  );
}