<template>
  <div class="dashboard">
    <KPICards 
      :loading="loadingKPIs" 
      :kpis="kpisData" 
    />
    
    <!-- Grid Principal -->
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
        <h3>Performance por Canal</h3>
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
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { analyticsAPI } from '../services/api'
import KPICards from './KPICards.vue'
import SalesChart from './SalesChart.vue'
import ChannelPerformance from './ChannelPerformance.vue'
import TopProducts from './TopProducts.vue'
import StoresList from './StoresList.vue'

export default {
  name: 'Dashboard',
  components: {
    KPICards,
    SalesChart,
    ChannelPerformance,
    TopProducts,
    StoresList
  },
  setup() {
    // Estados de loading
    const loadingKPIs = ref(true)
    const loadingTrends = ref(true)
    const loadingChannels = ref(true)
    const loadingProducts = ref(true)
    const loadingStores = ref(true)
    
    // Dados
    const kpisData = ref({})
    const trendsData = ref([])
    const channelsData = ref([])
    const productsData = ref([])
    const storesData = ref([])
    
    // Função para carregar todos os dados
    const loadDashboardData = async () => {
      try {
        const [
          kpisResponse,
          trendsResponse, 
          channelsResponse,
          productsResponse,
          storesResponse
        ] = await Promise.all([
          analyticsAPI.getDailyKPIs(),
          analyticsAPI.getSalesTrends(),
          analyticsAPI.getChannelPerformance(),
          analyticsAPI.getTopProducts(),
          analyticsAPI.getStores()
        ])
        
        // Atualizar dados
        kpisData.value = kpisResponse.data.data
        trendsData.value = trendsResponse.data.data.trends
        channelsData.value = channelsResponse.data.data.channels
        productsData.value = productsResponse.data.data.products
        storesData.value = storesResponse.data.data.stores
        
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
      } finally {
        loadingKPIs.value = false
        loadingTrends.value = false
        loadingChannels.value = false
        loadingProducts.value = false
        loadingStores.value = false
      }
    }
    
    onMounted(() => {
      loadDashboardData()
    })
    
    return {
      loadingKPIs,
      loadingTrends,
      loadingChannels,
      loadingProducts,
      loadingStores,
      kpisData,
      trendsData,
      channelsData,
      productsData,
      storesData
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px 0;
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

@media (max-width: 1024px) {
  .lg\:grid-cols-2 {
    grid-template-columns: 1fr;
  }
}
</style>