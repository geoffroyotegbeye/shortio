export interface VideoGenerationRequest {
  prompt: string;
  n_images: number;
  category: 'astuce' | 'motivation' | 'lifestyle';
  lang: 'fr' | 'en';
}

export interface VideoGenerationResponse {
  video_url: string;
}

export type GenerationStatus = 'idle' | 'loading' | 'success' | 'error';