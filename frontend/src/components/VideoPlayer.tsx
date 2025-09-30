import { Download } from 'lucide-react';

interface VideoPlayerProps {
  videoUrl: string;
  onGenerateAnother: () => void;
}

export default function VideoPlayer({ videoUrl, onGenerateAnother }: VideoPlayerProps) {
  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = videoUrl;
    link.download = 'video.mp4';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="w-full space-y-4">
      <div className="bg-gray-900 rounded-lg overflow-hidden">
        <video
          src={videoUrl}
          controls
          className="w-full h-auto"
          autoPlay
        >
          Votre navigateur ne supporte pas la lecture de vidéos.
        </video>
      </div>

      <div className="flex gap-3">
        <button
          onClick={handleDownload}
          className="flex-1 bg-gradient-to-r from-blue-500 to-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:from-blue-600 hover:to-blue-700 transition-all duration-200 flex items-center justify-center gap-2"
        >
          <Download size={20} />
          Télécharger la vidéo
        </button>

        <button
          onClick={onGenerateAnother}
          className="flex-1 bg-gray-700 text-white py-3 px-6 rounded-lg font-medium hover:bg-gray-600 transition-all duration-200"
        >
          Générer une autre vidéo
        </button>
      </div>
    </div>
  );
}