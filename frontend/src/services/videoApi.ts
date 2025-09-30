import axios from 'axios';
import type { VideoGenerationRequest, VideoGenerationResponse } from '../types/video';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const videoApi = {
  generateVideo: async (data: VideoGenerationRequest): Promise<VideoGenerationResponse> => {
    const response = await axios.post<VideoGenerationResponse>(
      `${API_BASE_URL}/generate-video`,
      data
    );
    return response.data;
  }
};