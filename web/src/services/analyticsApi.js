import api from './api.js'

export const analyticsApi = {
  // Query Builder
  runCustomQuery: (query) => api.post('/explorer/query', query),
  getAvailableMetrics: () => api.get('/explorer/metrics'),
  getAvailableDimensions: () => api.get('/explorer/dimensions'),
  getInsightTemplates: () => api.get('/explorer/insights/templates'),
  
  // Business Insights
  getTopProductsByTime: (params) => api.get('/insights/top-products-by-time', { params }),
  getInactiveCustomers: (params) => api.get('/insights/inactive-customers', { params }),
  getDeliveryPerformance: () => api.get('/insights/delivery-performance'),
  getProductMargins: () => api.get('/insights/product-margins'),
  
  // Dashboards
  saveDashboard: (dashboard) => api.post('/dashboards', dashboard),
  getUserDashboards: () => api.get('/dashboards'),
  getDashboardTemplates: () => api.get('/dashboards/templates'),
  deleteDashboard: (id) => api.delete(`/dashboards/${id}`)
}