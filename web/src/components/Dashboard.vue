<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>🍔 Nola Analytics</h1>
      <p>Dashboard Inteligente para Restaurantes</p>
      
      <div class="nav-tabs">
        <button 
          class="tab-btn"
          :class="{ active: activeTab === 'overview' }"
          @click="activeTab = 'overview'"
        >
          📊 Visão Geral
        </button>
        <button 
          class="tab-btn"
          :class="{ active: activeTab === 'explorer' }"
          @click="activeTab = 'explorer'"
        >
          🔍 Analytics Explorer
        </button>
        <button 
          class="tab-btn"
          :class="{ active: activeTab === 'insights' }"
          @click="activeTab = 'insights'"
        >
          💡 Insights
        </button>
      </div>
    </div>

    <!-- Tab: Visão Geral -->
    <div v-if="activeTab === 'overview'" class="tab-content">
      <KPICards 
        :loading="loadingKPIs" 
        :kpis="kpisData" 
      />
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Gráfico de Tendências -->
        <div class="card">
          <h3>📈 Tendências de Vendas (30 dias)</h3>
          <SalesChart 
            v-if="trendsData.length > 0"
            :data="trendsData" 
            :loading="loadingTrends"
          />
          <div v-else class="loading">Carregando tendências...</div>
        </div>
        
        <!-- Performance por Canal -->
        <div class="card">
          <h3> Performance por Canal</h3>
          <ChannelPerformance 
            v-if="channelsData.length > 0"
            :data="channelsData"
            :loading="loadingChannels"
          />
          <div v-else class="loading">Carregando canais...</div>
        </div>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <!-- Top Produtos -->
        <div class="card">
          <h3> Top Produtos</h3>
          <TopProducts 
            v-if="productsData.length > 0"
            :products="productsData"
            :loading="loadingProducts"
          />
          <div v-else class="loading">Carregando produtos...</div>
        </div>
        
        <!-- Lista de Lojas -->
        <div class="card">
          <h3>🏪 Nossas Lojas</h3>
          <StoresList 
            v-if="storesData.length > 0"
            :data="storesData"
            :loading="loadingStores"
          />
          <div v-else class="loading">Carregando lojas...</div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions">
        <h3>🚀 Ações Rápidas</h3>
        <div class="actions-grid">
          <button class="action-btn" @click="activeTab = 'explorer'">
            <span class="action-icon">🔍</span>
            <span class="action-text">Criar Análise Personalizada</span>
          </button>
          <button class="action-btn" @click="activeTab = 'insights'">
            <span class="action-icon">💡</span>
            <span class="action-text">Ver Insights do Negócio</span>
          </button>
          <button class="action-btn" @click="loadInactiveCustomers">
            <span class="action-icon">👥</span>
            <span class="action-text">Clientes Inativos</span>
          </button>
          <button class="action-btn" @click="loadDeliveryPerformance">
            <span class="action-icon">⏱️</span>
            <span class="action-text">Performance de Entrega</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Tab: Analytics Explorer -->
    <div v-if="activeTab === 'explorer'" class="tab-content">
      <!-- Caixa branca do Construtor de Consultas -->
      <div class="white-info-box">
        <h2>🔍 Construtor de Consultas</h2>
      </div>
      
      <QueryBuilder />
    </div>

    <!-- Tab: Business Insights -->
    <div v-if="activeTab === 'insights'" class="tab-content">
      <!-- Caixa branca dos Insights -->
      <div class="white-info-box">
        <h2>💡 Insights do Negócio</h2>
      </div>
      
      <BusinessInsightsPanel />
    </div>

    <!-- Loading geral -->
    <div v-if="loadingOverview && activeTab === 'overview'" class="overview-loading">
      <div class="loading-spinner"></div>
      <p>Carregando dashboard...</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { dashboardApi } from '../services/api.js'
import { analyticsApi } from '../services/analyticsApi.js'

// Componentes do dashboard básico
import KPICards from './KPICards.vue'
import SalesChart from './SalesChart.vue'
import ChannelPerformance from './ChannelPerformance.vue'
import TopProducts from './TopProducts.vue'
import StoresList from './StoresList.vue'

// Novos componentes de analytics
import QueryBuilder from './QueryBuilder.vue'
import BusinessInsightsPanel from './BusinessInsightsPanel.vue'

export default {
  name: 'Dashboard',
  components: {
    KPICards,
    SalesChart,
    ChannelPerformance,
    TopProducts,
    StoresList,
    QueryBuilder,
    BusinessInsightsPanel
  },
  setup() {
    // Estado das tabs
    const activeTab = ref('overview')
    
    // Estados de loading
    const loadingOverview = ref(true)
    const loadingKPIs = ref(true)
    const loadingTrends = ref(true)
    const loadingChannels = ref(true)
    const loadingProducts = ref(true)
    const loadingStores = ref(true)

    // Dados do dashboard
    const kpisData = ref({})
    const trendsData = ref([])
    const channelsData = ref([])
    const productsData = ref([])
    const storesData = ref([])

    // Dados dos insights
    const inactiveCustomers = ref([])
    const deliveryPerformance = ref([])

    // Carregar dados do dashboard básico
    const loadDashboardData = async () => {
      try {
        loadingOverview.value = true
        
        const [
          kpisResponse,
          trendsResponse, 
          channelsResponse,
          productsResponse,
          storesResponse
        ] = await Promise.all([
          dashboardApi.getDailyKPIs(),
          dashboardApi.getSalesTrends(),
          dashboardApi.getChannelPerformance(),
          dashboardApi.getTopProducts(),
          dashboardApi.getStores()
        ])
        
        // Atualizar dados
        kpisData.value = kpisResponse.data.data
        trendsData.value = trendsResponse.data.data.trends
        channelsData.value = channelsResponse.data.data.channels
        productsData.value = productsResponse.data.data.products
        storesData.value = storesResponse.data.data.stores
        
      } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error)
      } finally {
        loadingOverview.value = false
        loadingKPIs.value = false
        loadingTrends.value = false
        loadingChannels.value = false
        loadingProducts.value = false
        loadingStores.value = false
      }
    }

    // Carregar clientes inativos
    const loadInactiveCustomers = async () => {
      try {
        const response = await analyticsApi.getInactiveCustomers({
          min_orders: 3,
          days_inactive: 30
        })
        inactiveCustomers.value = response.data.data.customers
        activeTab.value = 'insights'
      } catch (error) {
        console.error('Erro ao carregar clientes inativos:', error)
      }
    }

    const loadDeliveryPerformance = async () => {
      try {
        const response = await analyticsApi.getDeliveryPerformance()
        deliveryPerformance.value = response.data.data.performance
        activeTab.value = 'insights'
      } catch (error) {
        console.error('Erro ao carregar performance de entrega:', error)
      }
    }

    watch(activeTab, (newTab) => {
      if (newTab === 'overview' && !trendsData.value.length) {
        loadDashboardData()
      }
    })

    onMounted(() => {
      loadDashboardData()
    })

    return {
      activeTab,
      loadingOverview,
      loadingKPIs,
      loadingTrends,
      loadingChannels,
      loadingProducts,
      loadingStores,
      kpisData,
      trendsData,
      channelsData,
      productsData,
      storesData,
      inactiveCustomers,
      deliveryPerformance,
      loadInactiveCustomers,
      loadDeliveryPerformance
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e9ecef;
}

.dashboard-header h1 {
  color: #2c3e50;
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.dashboard-header p {
  color: #7f8c8d;
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.nav-tabs {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 12px 24px;
  border: 2px solid #e9ecef;
  background: white;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  color: #7f8c8d;
}

.tab-btn:hover {
  transform: translateY(-2px);
  border-color: #3498db;
  color: #3498db;
}

.tab-btn.active {
  background: #3498db;
  border-color: #3498db;
  color: white;
}

.tab-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.grid {
  display: grid;
  gap: 1.5rem;
}

.grid-cols-1 {
  grid-template-columns: 1fr;
}

.grid-cols-2 {
  grid-template-columns: repeat(2, 1fr);
}

.gap-6 {
  gap: 1.5rem;
}

.mt-6 {
  margin-top: 1.5rem;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  border: 1px solid #e9ecef;
}

.card h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  border-bottom: 2px solid #0056b3;
  padding-bottom: 5px;
}

.loading {
  text-align: center;
  padding: 40px 20px;
  color: #7f8c8d;
  font-style: italic;
}

.overview-loading {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.quick-actions {
  margin-top: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
}

.quick-actions h3 {
  color: #2c3e50;
  margin-bottom: 20px;
  text-align: center;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.action-btn {
  display: flex;
  align-items: center;
  padding: 20px;
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.action-btn:hover {
  transform: translateY(-3px);
  border-color: #3498db;
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
}

.action-icon {
  font-size: 2rem;
  margin-right: 15px;
}

.action-text {
  font-weight: bold;
  color: #2c3e50;
}

.white-info-box {
  background: white;
  border-radius: 15px;
  padding: 25px 30px;
  margin-bottom: 30px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border: 1px solid #e9ecef;
  text-align: center;
}

.white-info-box h2 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 1.5rem;
}

.white-info-box p {
  color: #7f8c8d;
  font-size: 1.1rem;
  margin: 0;
}

@media (max-width: 1024px) {
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
  
  .nav-tabs {
    flex-direction: column;
    align-items: center;
  }
  
  .tab-btn {
    width: 200px;
  }
}

@media (max-width: 768px) {
  .dashboard {
    padding: 10px;
  }
  
  .dashboard-header h1 {
    font-size: 2rem;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .action-btn {
    padding: 15px;
  }
  
  .action-icon {
    font-size: 1.5rem;
  }
  
  .white-info-box {
    padding: 20px;
    margin-bottom: 20px;
  }
  
  .white-info-box h2 {
    font-size: 1.3rem;
  }
  
  .white-info-box p {
    font-size: 1rem;
  }
}
</style>