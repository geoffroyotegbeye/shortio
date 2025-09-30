import { useState } from 'react';
import ConfigurationForm from '../components/ConfigurationForm';
import VideoPlayer from '../components/VideoPlayer';
import LoadingSpinner from '../components/LoadingSpinner';
import EmptyState from '../components/EmptyState';
import ErrorMessage from '../components/ErrorMessage';
import { videoApi } from '../services/videoApi';
import type { VideoGenerationRequest, GenerationStatus } from '../types/video';

export default function GenerateVideo() {
  const [status, setStatus] = useState<GenerationStatus>('idle');
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>('');

  const handleGenerateVideo = async (data: VideoGenerationRequest) => {
    setStatus('loading');
    setErrorMessage('');
    setVideoUrl(null);

    try {
      const response = await videoApi.generateVideo(data);
      setVideoUrl(response.video_url);
      setStatus('success');
    } catch (error) {
      console.error('Error generating video:', error);
      setErrorMessage('La génération a échoué. Veuillez réessayer.');
      setStatus('error');
    }
  };

  const handleReset = () => {
    setStatus('idle');
    setVideoUrl(null);
    setErrorMessage('');
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            Générateur de Vidéo IA
          </h1>
          <p className="text-gray-400">
            Transformez vos concepts en vidéos captivantes
          </p>
        </header>

        <div className="grid lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
          <div className="lg:col-span-1">
            <ConfigurationForm
              onSubmit={handleGenerateVideo}
              isLoading={status === 'loading'}
            />
          </div>

          <div className="lg:col-span-2">
            <div className="bg-gray-800 rounded-xl p-6 min-h-[400px]">
              {status === 'idle' && <EmptyState />}

              {status === 'loading' && <LoadingSpinner />}

              {status === 'success' && videoUrl && (
                <VideoPlayer
                  videoUrl={videoUrl}
                  onGenerateAnother={handleReset}
                />
              )}

              {status === 'error' && (
                <ErrorMessage
                  message={errorMessage}
                  onRetry={handleReset}
                />
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}