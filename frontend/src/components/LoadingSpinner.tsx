import { Loader2 } from 'lucide-react';

export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-16 space-y-4">
      <Loader2 className="w-12 h-12 text-blue-500 animate-spin" />
      <div className="text-center">
        <p className="text-lg font-medium text-gray-200">Génération en cours...</p>
        <p className="text-sm text-gray-400 mt-1">Cela peut prendre une minute.</p>
      </div>
    </div>
  );
}