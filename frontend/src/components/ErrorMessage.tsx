import { AlertCircle } from 'lucide-react';

interface ErrorMessageProps {
  message: string;
  onRetry: () => void;
}

export default function ErrorMessage({ message, onRetry }: ErrorMessageProps) {
  return (
    <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-6">
      <div className="flex items-start gap-3">
        <AlertCircle className="text-red-400 flex-shrink-0 mt-1" size={24} />
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-red-300 mb-1">
            Erreur de génération
          </h3>
          <p className="text-red-200/80 mb-4">
            {message}
          </p>
          <button
            onClick={onRetry}
            className="bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg font-medium transition-colors duration-200"
          >
            Réessayer
          </button>
        </div>
      </div>
    </div>
  );
}