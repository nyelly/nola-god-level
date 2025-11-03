import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// API original (dashboard básico)
export const dashboardApi = {
  getDailyKPIs: () => api.get('/kpis/daily'),
  getKPISummary: () => api.get('/kpis/summary'),
  getTopProducts: () => api.get('/sales/top-products'),
  getChannelPerformance: () => api.get('/sales/channels'),
  getSalesTrends: () => api.get('/analytics/trends'),
  getStores: () => api.get('/stores/list'),
  getStoresPerformance: () => api.get('/stores/performance'),
  getCategories: () => api.get('/products/categories'),
  getTopItems: () => api.get('/products/top-items')
}

// API do analytics explorer (nova)
export { analyticsApi } from './analyticsApi.js'

export default api