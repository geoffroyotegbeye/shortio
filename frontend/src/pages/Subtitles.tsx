import { useState, useRef } from 'react';
import { Upload, FileVideo, Download, Loader2 } from 'lucide-react';

type SubtitlePosition = 'top' | 'middle' | 'bottom';

export default function Subtitles() {
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [videoPreview, setVideoPreview] = useState<string | null>(null);
  const [subtitleText, setSubtitleText] = useState('');
  const [position, setPosition] = useState<SubtitlePosition>('bottom');
  const [isProcessing, setIsProcessing] = useState(false);
  const [processedVideoUrl, setProcessedVideoUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type.startsWith('video/')) {
      setVideoFile(file);
      const url = URL.createObjectURL(file);
      setVideoPreview(url);
      setProcessedVideoUrl(null);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith('video/')) {
      setVideoFile(file);
      const url = URL.createObjectURL(file);
      setVideoPreview(url);
      setProcessedVideoUrl(null);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleProcess = async () => {
    if (!videoFile || !subtitleText.trim()) return;

    setIsProcessing(true);

    try {
      const formData = new FormData();
      formData.append('video', videoFile);
      formData.append('subtitle_text', subtitleText);
      formData.append('position', position);

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
    setSubtitleText('');
    setPosition('bottom');
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
    <div className="min-h-[calc(100vh-4rem)] bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            Ajouter des Sous-titres Dynamiques
          </h1>
          <p className="text-gray-400">
            Uploadez votre vidéo et personnalisez vos sous-titres
          </p>
        </header>

        <div className="grid lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-gray-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold text-white mb-4">Upload Vidéo</h2>

              <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={() => fileInputRef.current?.click()}
                className="border-2 border-dashed border-gray-600 rounded-lg p-8 text-center cursor-pointer hover:border-purple-500 transition-colors duration-200"
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
                      <p className="text-gray-400 text-sm">
                        Cliquez pour changer
                      </p>
                    </>
                  ) : (
                    <>
                      <Upload size={48} className="text-gray-500" />
                      <p className="text-white font-medium">
                        Glissez-déposez votre vidéo
                      </p>
                      <p className="text-gray-400 text-sm">
                        ou cliquez pour parcourir
                      </p>
                    </>
                  )}
                </div>
              </div>
            </div>

            <div className="bg-gray-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold text-white mb-4">Configuration</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Texte des sous-titres
                  </label>
                  <textarea
                    value={subtitleText}
                    onChange={(e) => setSubtitleText(e.target.value)}
                    placeholder="Entrez le texte à afficher..."
                    className="w-full bg-gray-900 border border-gray-700 text-white rounded-lg px-4 py-3 min-h-[100px] focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent placeholder-gray-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Position des sous-titres
                  </label>
                  <div className="grid grid-cols-3 gap-2">
                    <button
                      onClick={() => setPosition('top')}
                      className={`py-2 px-3 rounded-lg font-medium transition-all duration-200 ${
                        position === 'top'
                          ? 'bg-purple-600 text-white'
                          : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                      }`}
                    >
                      Haut
                    </button>
                    <button
                      onClick={() => setPosition('middle')}
                      className={`py-2 px-3 rounded-lg font-medium transition-all duration-200 ${
                        position === 'middle'
                          ? 'bg-purple-600 text-white'
                          : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                      }`}
                    >
                      Milieu
                    </button>
                    <button
                      onClick={() => setPosition('bottom')}
                      className={`py-2 px-3 rounded-lg font-medium transition-all duration-200 ${
                        position === 'bottom'
                          ? 'bg-purple-600 text-white'
                          : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                      }`}
                    >
                      Bas
                    </button>
                  </div>
                </div>
              </div>

              <button
                onClick={handleProcess}
                disabled={!videoFile || !subtitleText.trim() || isProcessing}
                className="w-full mt-6 bg-gradient-to-r from-purple-500 to-pink-600 text-white py-3 px-6 rounded-lg font-medium hover:from-purple-600 hover:to-pink-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isProcessing ? (
                  <>
                    <Loader2 size={20} className="animate-spin" />
                    Traitement...
                  </>
                ) : (
                  'Ajouter les sous-titres'
                )}
              </button>
            </div>
          </div>

          <div className="lg:col-span-2">
            <div className="bg-gray-800 rounded-xl p-6 min-h-[500px]">
              {!videoPreview && !processedVideoUrl ? (
                <div className="flex flex-col items-center justify-center py-16 text-center">
                  <div className="bg-gray-700 rounded-full p-6 mb-4">
                    <FileVideo size={48} className="text-purple-500" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-200 mb-2">
                    Aucune vidéo uploadée
                  </h3>
                  <p className="text-gray-400 max-w-md">
                    Uploadez une vidéo pour commencer à ajouter des sous-titres personnalisés
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-white">
                      {processedVideoUrl ? 'Vidéo avec sous-titres' : 'Aperçu'}
                    </h3>
                    {processedVideoUrl && (
                      <button
                        onClick={handleReset}
                        className="text-gray-400 hover:text-white transition-colors duration-200"
                      >
                        Nouvelle vidéo
                      </button>
                    )}
                  </div>

                  <div className="bg-gray-900 rounded-lg overflow-hidden">
                    <video
                      src={processedVideoUrl || videoPreview || ''}
                      controls
                      className="w-full h-auto"
                      key={processedVideoUrl || videoPreview}
                    >
                      Votre navigateur ne supporte pas la lecture de vidéos.
                    </video>
                  </div>

                  {processedVideoUrl && (
                    <button
                      onClick={handleDownload}
                      className="w-full bg-gradient-to-r from-purple-500 to-pink-600 text-white py-3 px-6 rounded-lg font-medium hover:from-purple-600 hover:to-pink-700 transition-all duration-200 flex items-center justify-center gap-2"
                    >
                      <Download size={20} />
                      Télécharger la vidéo
                    </button>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}