import { useState, useRef } from 'react';
import { Upload, FileVideo, Download, Loader2, Wand2 } from 'lucide-react';

export default function Subtitles() {
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [videoPreview, setVideoPreview] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processedVideoUrl, setProcessedVideoUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type.startsWith('video/')) {
      setVideoFile(file);
      const url = URL.createObjectURL(file);
      setVideoPreview(url);
      setProcessedVideoUrl(null); // Reset processed video on new file
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith('video/')) {
      setVideoFile(file);
      const url = URL.createObjectURL(file);
      setVideoPreview(url);
      setProcessedVideoUrl(null); // Reset processed video on new file
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleProcess = async () => {
    if (!videoFile) return;

    setIsProcessing(true);
    setProcessedVideoUrl(null);

    try {
      const formData = new FormData();
      formData.append('video_file', videoFile);

      const response = await fetch('http://localhost:8000/api/v1/add-subtitles', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Failed to process video');

      const data = await response.json();
      setProcessedVideoUrl(data.video_url);
    } catch (error) {
      console.error('Error processing video:', error);
      alert('Erreur lors du traitement de la vidéo. Veuillez réessayer.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleReset = () => {
    setVideoFile(null);
    setVideoPreview(null);
    setProcessedVideoUrl(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleDownload = () => {
    if (processedVideoUrl) {
      const link = document.createElement('a');
      link.href = processedVideoUrl;
      link.download = 'video_with_subtitles.mp4';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-3">
            Sous-titrage Automatique par IA
          </h1>
          <p className="text-lg text-gray-400 max-w-2xl mx-auto">
            Uploadez une vidéo et laissez notre intelligence artificielle générer et incruster les sous-titres pour vous.
          </p>
        </header>

        <div className="grid lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
          {/* Colonne de gauche : Upload et Contrôles */}
          <div className="space-y-6 flex flex-col bg-gray-800 rounded-xl p-6 border border-gray-700">
            <h2 className="text-2xl font-semibold text-white mb-4">1. Choisissez une vidéo</h2>
            <div
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onClick={() => fileInputRef.current?.click()}
              className="border-2 border-dashed border-gray-600 rounded-lg p-8 text-center cursor-pointer hover:border-purple-500 transition-colors duration-200 flex-grow flex flex-col justify-center"
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="video/*"
                onChange={handleFileChange}
                className="hidden"
              />
              <div className="flex flex-col items-center gap-3">
                {videoFile ? (
                  <>
                    <FileVideo size={48} className="text-purple-500" />
                    <p className="text-white font-medium">{videoFile.name}</p>
                    <p className="text-gray-400 text-sm">Cliquez pour changer</p>
                  </>
                ) : (
                  <>
                    <Upload size={48} className="text-gray-500" />
                    <p className="text-white font-medium">Glissez-déposez votre vidéo</p>
                    <p className="text-gray-400 text-sm">ou cliquez pour parcourir</p>
                  </>
                )}
              </div>
            </div>

            <div className="space-y-4 pt-4">
              <button
                onClick={handleProcess}
                disabled={!videoFile || isProcessing}
                className="w-full bg-gradient-to-r from-purple-500 to-purple-600 text-white py-4 px-6 rounded-lg font-bold text-lg hover:from-purple-600 hover:to-purple-700 transition-all duration-200 flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isProcessing ? (
                  <>
                    <Loader2 className="animate-spin" size={24} />
                    Génération en cours...
                  </>
                ) : (
                  <>
                    <Wand2 size={24} />
                    Générer les sous-titres
                  </>
                )}
              </button>

              {videoFile && (
                <button
                  onClick={handleReset}
                  className="w-full bg-gray-700 text-white py-2 rounded-lg hover:bg-gray-600 transition-colors"
                >
                  Recommencer
                </button>
              )}
            </div>
          </div>

          {/* Colonne de droite : Affichage Vidéo */}
          <div className="bg-gray-800 rounded-xl p-4 flex items-center justify-center border border-gray-700">
            <div className="w-full flex justify-center">
              <div className="bg-gray-900 rounded-lg overflow-hidden w-full max-w-[360px] aspect-[9/16] flex items-center justify-center">
                {processedVideoUrl ? (
                  <video src={processedVideoUrl} controls autoPlay className="w-full h-full object-cover" />
                ) : videoPreview ? (
                  <video src={videoPreview} controls className="w-full h-full object-cover" />
                ) : (
                  <div className="text-center text-gray-500 px-4">
                    <FileVideo size={64} className="mx-auto mb-4" />
                    <p className="font-medium text-lg">L'aperçu de votre vidéo</p>
                    <p>apparaîtra ici.</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {processedVideoUrl && (
          <div className="mt-8 text-center">
            <button
              onClick={handleDownload}
              className="bg-gradient-to-r from-blue-500 to-blue-600 text-white py-3 px-8 rounded-lg font-medium hover:from-blue-600 hover:to-blue-700 transition-all duration-200 flex items-center justify-center gap-2 mx-auto"
            >
              <Download size={20} />
              Télécharger la vidéo finale
            </button>
          </div>
        )}
      </div>
    </div>
  );
}