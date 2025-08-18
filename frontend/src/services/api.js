import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds for AI processing
  headers: {
    'Content-Type': 'application/json',
  },
});

export const trendService = {
  // Get trending data from all platforms
  getTrendingData: async () => {
    try {
      const response = await api.get('/trending');
      return response.data;
    } catch (error) {
      console.error('Error fetching trending data:', error);
      throw error;
    }
  },

  // Generate complete strategy
  getCompleteStrategy: async (targetAudience = 'Gen Z', niche = 'General') => {
    try {
      const response = await api.get('/strategy', {
        params: {
          target_audience: targetAudience,
          niche: niche
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error generating strategy:', error);
      throw error;
    }
  },

  // Analyze specific trends
  analyzeTrends: async (trendsData, targetAudience, niche) => {
    try {
      const response = await api.post('/analyze', {
        trends_data: trendsData,
        target_audience: targetAudience,
        niche: niche
      });
      return response.data;
    } catch (error) {
      console.error('Error analyzing trends:', error);
      throw error;
    }
  }
};

export default api;
