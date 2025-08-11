import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log('Making API request:', config.method?.toUpperCase(), config.url)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log('API response received:', response.status, response.config.url)
    return response
  },
  (error) => {
    console.error('API error:', error.response?.status, error.response?.data)
    return Promise.reject(error)
  }
)

export const nutritionApi = {
  // Get meal recommendations
  getRecommendations: (userProfile) => {
    return apiClient.post('/recommendations', userProfile)
  },

  // Health check
  healthCheck: () => {
    return apiClient.get('/health')
  },

  // Get API info
  getInfo: () => {
    return apiClient.get('/')
  }
}

export default apiClient
