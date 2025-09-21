import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

// Create axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

class AuthService {
  setAuthToken(token) {
    if (token) {
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
    } else {
      delete apiClient.defaults.headers.common['Authorization']
    }
  }

  async login(credentials) {
    return apiClient.post('/auth/login', credentials)
  }

  async register(userData) {
    return apiClient.post('/auth/register', userData)
  }
}

export const authService = new AuthService()
export { apiClient }