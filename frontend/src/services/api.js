import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const analyticsAPI = {
  // KPIs
  getDailyKPIs: () => api.get('/kpis/daily'),
  getKPISummary: () => api.get('/kpis/summary'),
  
  // Vendas
  getTopProducts: () => api.get('/sales/top-products'),
  getChannelPerformance: () => api.get('/sales/channels'),
  
  // Analytics
  getSalesTrends: () => api.get('/analytics/trends'),
  
  // Lojas
  getStores: () => api.get('/stores/list'),
  getStoresPerformance: () => api.get('/stores/performance'),
  
  // Produtos
  getCategories: () => api.get('/products/categories'),
  getTopItems: () => api.get('/products/top-items')
}

export default api