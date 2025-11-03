<template>
  <div class="business-insights">

    <div class="insights-grid">
      <!-- Insight 1: Top Produtos por Horário -->
      <div class="insight-card">
        <div class="insight-header">
          <h3>🍽️ Top Produtos por Horário</h3>
        </div>
        
        <div class="insight-controls">
          <div class="control-group">
            <label>Dia da semana:</label>
            <select v-model="topProductsParams.day_of_week">
              <option value="">Todos</option>
              <option value="0">Domingo</option>
              <option value="1">Segunda</option>
              <option value="2">Terça</option>
              <option value="3">Quarta</option>
              <option value="4">Quinta</option>
              <option value="5">Sexta</option>
              <option value="6">Sábado</option>
            </select>
          </div>
          
          <div class="control-group">
            <label>Hora:</label>
            <select v-model="topProductsParams.hour">
              <option value="">Todas</option>
              <option v-for="h in 24" :key="h" :value="h-1">{{ h-1 }}h</option>
            </select>
          </div>
          
          <div class="control-group">
            <label>Canal:</label>
            <select v-model="topProductsParams.channel">
              <option value="">Todos</option>
              <option value="iFood">iFood</option>
              <option value="Rappi">Rappi</option>
              <option value="Balcão">Balcão</option>
              <option value="WhatsApp">WhatsApp</option>
            </select>
          </div>
          
          <button class="btn-insight" @click="loadTopProductsByTime">
            🔍 Analisar
          </button>
        </div>

        <div v-if="loadingTopProducts" class="loading">Analisando dados...</div>
        <div v-else-if="topProductsData.length" class="insight-results">
          <h4>Top Produtos:</h4>
          <div class="products-list">
            <div 
              v-for="(product, index) in topProductsData" 
              :key="product.produto"
              class="product-item"
            >
              <div class="product-rank">#{{ index + 1 }}</div>
              <div class="product-info">
                <div class="product-name">{{ product.produto }}</div>
                <div class="product-stats">
                  <span class="stat">{{ product.vezes_vendido }} vendas</span>
                  <span class="stat revenue">{{ formatCurrency(product.receita_total) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Insight 2: Clientes Inativos -->
      <div class="insight-card">
        <div class="insight-header">
          <h3>👥 Clientes Inativos</h3>
        </div>
        
        <div class="insight-controls">
          <div class="control-group">
            <label>Mínimo de pedidos:</label>
            <input 
              type="number" 
              v-model="inactiveCustomersParams.min_orders" 
              min="1"
            >
          </div>
          
          <div class="control-group">
            <label>Dias inativo:</label>
            <input 
              type="number" 
              v-model="inactiveCustomersParams.days_inactive" 
              min="1"
            >
          </div>
          
          <button class="btn-insight" @click="loadInactiveCustomers">
            🔍 Buscar
          </button>
        </div>

        <div v-if="loadingInactiveCustomers" class="loading">Buscando clientes...</div>
        <div v-else-if="inactiveCustomersData.length" class="insight-results">
          <h4>Clientes Inativos ({{ inactiveCustomersData.length }}):</h4>
          <div class="customers-list">
            <div 
              v-for="customer in inactiveCustomersData" 
              :key="customer.email"
              class="customer-item"
            >
              <div class="customer-name">{{ customer.cliente }}</div>
              <div class="customer-details">
                <div class="detail">{{ customer.total_pedidos }} pedidos</div>
                <div class="detail">{{ customer.dias_inativo }} dias sem comprar</div>
                <div class="detail">Ticket: {{ formatCurrency(customer.ticket_medio) }}</div>
              </div>
              <div class="customer-contact">{{ customer.email }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Insight 3: Performance de Entrega -->
      <div class="insight-card">
        <div class="insight-header">
          <h3>⏱️ Performance de Entrega</h3>
        </div>
        
        <button class="btn-insight" @click="loadDeliveryPerformance">
          📊 Analisar Performance
        </button>

        <div v-if="loadingDelivery" class="loading">Analisando entregas...</div>
        <div v-else-if="deliveryData.length" class="insight-results">
          <h4>Tempos Médios de Entrega:</h4>
          <div class="delivery-stats">
            <div class="stat-card">
              <div class="stat-value">{{ getAverageDeliveryTime() }}min</div>
              <div class="stat-label">Tempo médio</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ getWorstDeliveryTime() }}min</div>
              <div class="stat-label">Pior horário</div>
            </div>
          </div>
          
          <div class="delivery-chart">
            <h5>Performance por Hora:</h5>
            <div 
              v-for="hour in getDeliveryByHour()" 
              :key="hour.hora"
              class="hour-performance"
            >
              <div class="hour-label">{{ hour.hora }}h</div>
              <div class="hour-bar">
                <div 
                  class="bar-fill"
                  :style="{ width: getDeliveryBarWidth(hour.tempo) + '%' }"
                  :class="getDeliveryBarClass(hour.tempo)"
                ></div>
              </div>
              <div class="hour-value">{{ hour.tempo }}min</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Insight 4: Margens de Produtos -->
      <div class="insight-card">
        <div class="insight-header">
          <h3>💰 Margens de Produtos</h3>
        </div>
        
        <button class="btn-insight" @click="loadProductMargins">
          💰 Analisar Margens
        </button>

        <div v-if="loadingMargins" class="loading">Analisando produtos...</div>
        <div v-else-if="marginsData.length" class="insight-results">
          <h4>Produtos com Maior Volume:</h4>
          <div class="margins-list">
            <div 
              v-for="product in marginsData" 
              :key="product.produto"
              class="margin-item"
            >
              <div class="product-main">
                <div class="product-name">{{ product.produto }}</div>
                <div class="product-category">{{ product.categoria }}</div>
              </div>
              <div class="product-stats">
                <div class="stat">{{ product.vezes_vendido }} vendas</div>
                <div class="stat">{{ formatCurrency(product.receita_total) }}</div>
                <div class="stat price">{{ formatCurrency(product.preco_medio_unitario) }} uni.</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { analyticsApi } from '../services/analyticsApi.js'
import { formatCurrency } from '../utils/formatters.js'

export default {
  name: 'BusinessInsightsPanel',
  setup() {
    // Estados de loading
    const loadingTopProducts = ref(false)
    const loadingInactiveCustomers = ref(false)
    const loadingDelivery = ref(false)
    const loadingMargins = ref(false)

    // Parâmetros das consultas
    const topProductsParams = ref({
      day_of_week: '',
      hour: '',
      channel: ''
    })

    const inactiveCustomersParams = ref({
      min_orders: 3,
      days_inactive: 30
    })

    // Dados dos insights
    const topProductsData = ref([])
    const inactiveCustomersData = ref([])
    const deliveryData = ref([])
    const marginsData = ref([])

    // Métodos
    const loadTopProductsByTime = async () => {
      loadingTopProducts.value = true
      try {
        const response = await analyticsApi.getTopProductsByTime(topProductsParams.value)
        topProductsData.value = response.data.data.products
      } catch (error) {
        console.error('Erro ao carregar top produtos:', error)
        alert('Erro ao carregar dados dos produtos')
      } finally {
        loadingTopProducts.value = false
      }
    }

    const loadInactiveCustomers = async () => {
      loadingInactiveCustomers.value = true
      try {
        const response = await analyticsApi.getInactiveCustomers(inactiveCustomersParams.value)
        inactiveCustomersData.value = response.data.data.customers
      } catch (error) {
        console.error('Erro ao carregar clientes inativos:', error)
        alert('Erro ao carregar clientes inativos')
      } finally {
        loadingInactiveCustomers.value = false
      }
    }

    const loadDeliveryPerformance = async () => {
      loadingDelivery.value = true
      try {
        const response = await analyticsApi.getDeliveryPerformance()
        deliveryData.value = response.data.data.performance
      } catch (error) {
        console.error('Erro ao carregar performance de entrega:', error)
        alert('Erro ao carregar performance de entrega')
      } finally {
        loadingDelivery.value = false
      }
    }

    const loadProductMargins = async () => {
      loadingMargins.value = true
      try {
        const response = await analyticsApi.getProductMargins()
        marginsData.value = response.data.data.products
      } catch (error) {
        console.error('Erro ao carregar margens:', error)
        alert('Erro ao carregar dados de margens')
      } finally {
        loadingMargins.value = false
      }
    }

    // Métodos auxiliares para delivery
    const getAverageDeliveryTime = () => {
      if (!deliveryData.value.length) return 0
      const total = deliveryData.value.reduce((sum, item) => sum + item.tempo_medio_entrega_minutos, 0)
      return Math.round(total / deliveryData.value.length)
    }

    const getWorstDeliveryTime = () => {
      if (!deliveryData.value.length) return 0
      return Math.max(...deliveryData.value.map(item => item.tempo_medio_entrega_minutos))
    }

    const getDeliveryByHour = () => {
      const byHour = {}
      deliveryData.value.forEach(item => {
        if (!byHour[item.hora]) {
          byHour[item.hora] = { hora: item.hora, tempo: 0, count: 0 }
        }
        byHour[item.hora].tempo += item.tempo_medio_entrega_minutos
        byHour[item.hora].count += 1
      })
      
      return Object.values(byHour)
        .map(hour => ({ ...hour, tempo: Math.round(hour.tempo / hour.count) }))
        .sort((a, b) => a.hora - b.hora)
    }

    const getDeliveryBarWidth = (tempo) => {
      const max = 60 // 60 minutos como máximo
      return Math.min((tempo / max) * 100, 100)
    }

    const getDeliveryBarClass = (tempo) => {
      if (tempo <= 30) return 'good'
      if (tempo <= 45) return 'warning'
      return 'bad'
    }

    return {
      loadingTopProducts,
      loadingInactiveCustomers,
      loadingDelivery,
      loadingMargins,
      topProductsParams,
      inactiveCustomersParams,
      topProductsData,
      inactiveCustomersData,
      deliveryData,
      marginsData,
      loadTopProductsByTime,
      loadInactiveCustomers,
      loadDeliveryPerformance,
      loadProductMargins,
      formatCurrency,
      getAverageDeliveryTime,
      getWorstDeliveryTime,
      getDeliveryByHour,
      getDeliveryBarWidth,
      getDeliveryBarClass
    }
  }
}
</script>

<style scoped>
.business-insights {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.insights-header {
  text-align: center;
  margin-bottom: 40px;
}

.insights-header h2 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.insights-header p {
  color: #7f8c8d;
  font-size: 1.1rem;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 25px;
}

.insight-card {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border: 1px solid #e9ecef;
  transition: transform 0.3s ease;
}

.insight-card:hover {
  transform: translateY(-5px);
}

.insight-header h3 {
  color: #2c3e50;
  margin-bottom: 8px;
}

.insight-header p {
  color: #7f8c8d;
  font-style: italic;
  margin-bottom: 20px;
  font-size: 0.9rem;
}

.insight-controls {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  margin-bottom: 20px;
  align-items: end;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.control-group label {
  font-weight: bold;
  color: #2c3e50;
  font-size: 0.9rem;
}

.control-group select,
.control-group input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  min-width: 120px;
}

.btn-insight {
  padding: 10px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s ease;
  height: fit-content;
}

.btn-insight:hover {
  background: #2980b9;
}

.loading {
  text-align: center;
  padding: 30px;
  color: #7f8c8d;
  font-style: italic;
}

.insight-results h4 {
  color: #2c3e50;
  margin-bottom: 15px;
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 8px;
}

/* Estilos específicos para cada tipo de resultado */
.products-list,
.customers-list,
.margins-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 300px;
  overflow-y: auto;
}

.product-item,
.customer-item,
.margin-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #3498db;
}

.product-rank {
  font-weight: bold;
  font-size: 1.2rem;
  color: #2c3e50;
  margin-right: 15px;
  min-width: 40px;
}

.product-info,
.customer-details,
.product-main {
  flex: 1;
}

.product-name,
.customer-name {
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 5px;
}

.product-category {
  font-size: 0.8rem;
  color: #7f8c8d;
  font-style: italic;
}

.product-stats,
.customer-details {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.stat {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.stat.revenue,
.stat.price {
  font-weight: bold;
  color: #27ae60;
}

.customer-contact {
  font-size: 0.8rem;
  color: #3498db;
  font-style: italic;
}

/* Delivery Stats */
.delivery-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.delivery-chart {
  margin-top: 20px;
}

.delivery-chart h5 {
  margin-bottom: 15px;
  color: #2c3e50;
}

.hour-performance {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 10px;
}

.hour-label {
  font-weight: bold;
  color: #2c3e50;
  min-width: 40px;
}

.hour-bar {
  flex: 1;
  height: 20px;
  background: #e9ecef;
  border-radius: 10px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 10px;
  transition: width 0.5s ease;
}

.bar-fill.good {
  background: #27ae60;
}

.bar-fill.warning {
  background: #f39c12;
}

.bar-fill.bad {
  background: #e74c3c;
}

.hour-value {
  font-weight: bold;
  color: #2c3e50;
  min-width: 50px;
}

@media (max-width: 768px) {
  .insights-grid {
    grid-template-columns: 1fr;
  }
  
  .insight-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .control-group {
    width: 100%;
  }
  
  .delivery-stats {
    grid-template-columns: 1fr;
  }
  
  .product-stats,
  .customer-details {
    flex-direction: column;
    gap: 5px;
  }
}
</style>