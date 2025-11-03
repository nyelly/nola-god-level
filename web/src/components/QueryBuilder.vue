<template>
  <div class="query-builder">

    <div class="builder-grid">
      <!-- Métricas -->
      <div class="builder-section">
        <h4>📊 Métricas</h4>
        <div class="items-grid">
          <div 
            v-for="metric in availableMetrics" 
            :key="metric.id"
            class="item-card"
            :class="{ selected: selectedMetrics.includes(metric.id) }"
            @click="toggleMetric(metric.id)"
          >
            <div class="item-name">{{ metric.name }}</div>
          </div>
        </div>
      </div>

      <!-- Dimensões -->
      <div class="builder-section">
        <h4>📈 Dimensões</h4>
        <div class="items-grid">
          <div 
            v-for="dimension in availableDimensions" 
            :key="dimension.id"
            class="item-card"
            :class="{ selected: selectedDimensions.includes(dimension.id) }"
            @click="toggleDimension(dimension.id)"
          >
            <div class="item-name">{{ dimension.name }}</div>
          </div>
        </div>
      </div>

      <!-- Filtros -->
      <div class="builder-section">
        <h4>🎯 Filtros</h4>

        <!-- Filtros dinâmicos baseados nas dimensões selecionadas -->
        <div class="dynamic-filters">
          <!-- Filtro de Data -->
          <div v-if="selectedDimensions.includes('data')" class="filter-group">
            <label>Filtrar Data:</label>
            <div class="date-picker-wrapper">
              <input 
                type="date" 
                v-model="filters.data"
                @change="updateDateFilter"
              >
            </div>
          </div>

          <!-- Filtro de Hora -->
          <div v-if="selectedDimensions.includes('hora')" class="filter-group">
            <label>Filtrar Hora:</label>
            <div class="time-input-wrapper">
              <input 
                type="time" 
                v-model="filters.hora"
                @change="updateTimeFilter"
              >
            </div>
          </div>

          <!-- Filtro de Dia da Semana -->
          <div v-if="selectedDimensions.includes('dia_semana')" class="filter-group">
            <label>Filtrar Dia da Semana:</label>
            <select v-model="filters.dia_semana" @change="updateDayFilter">
              <option value="">Todos os dias</option>
              <option v-for="day in daysOfWeek" :key="day.value" :value="day.value">
                {{ day.label }}
              </option>
            </select>
          </div>

          <!-- Filtro de Loja -->
          <div v-if="selectedDimensions.includes('loja')" class="filter-group">
            <label>Filtrar Loja:</label>
            <select v-model="filters.loja" @change="updateStoreFilter">
              <option value="">Todas as lojas</option>
              <option v-for="store in availableStores" :key="store.id" :value="store.id">
                {{ store.nome }}
              </option>
            </select>
          </div>

          <!-- Filtro de Canal -->
          <div v-if="selectedDimensions.includes('canal')" class="filter-group">
            <label>Filtrar Canal:</label>
            <select v-model="filters.canal" @change="updateChannelFilter">
              <option value="">Todos os canais</option>
              <option v-for="channel in availableChannels" :key="channel" :value="channel">
                {{ channel }}
              </option>
            </select>
          </div>

          <!-- Filtro de Categoria -->
          <div v-if="selectedDimensions.includes('categoria')" class="filter-group">
            <label>Filtrar Categoria:</label>
            <select v-model="filters.categoria" @change="updateCategoryFilter">
              <option value="">Todas as categorias</option>
              <option v-for="category in availableCategories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>

          <!-- Filtro de Produto -->
          <div v-if="selectedDimensions.includes('produto')" class="filter-group">
            <label>Filtrar Produto:</label>
            <select v-model="filters.produto" @change="updateProductFilter">
              <option value="">Todos os produtos</option>
              <option v-for="product in availableProducts" :key="product.id" :value="product.id">
                {{ product.nome }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Ações -->
    <div class="actions-section">
      <button 
        class="btn-run" 
        @click="runQuery"
        :disabled="!canRunQuery"
      >
        🚀 Executar Consulta
      </button>
      
      <button 
        class="btn-save" 
        @click="saveToDashboard"
        :disabled="!queryResult"
      >
        💾 Salvar no Dashboard
      </button>
    </div>

    <!-- Visualização APENAS de Linha -->
    <div v-if="selectedMetrics.length > 0 && selectedDimensions.length > 0" class="multi-visualization">
      <h4>📊 Visualizações Geradas</h4>
      
      <!-- Container da visualização de linha -->
      <div class="viz-container">
        <!-- Gráfico de Linha -->
        <div class="viz-panel">
          <h5>Gráfico de Linha</h5>
          <div v-if="queryResult" class="chart-container">
            <canvas ref="lineChart"></canvas>
          </div>
          <div v-else class="chart-placeholder">
            <div class="placeholder-icon">📈</div>
            <p>Execute a consulta para ver o gráfico de linha</p>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="preview-section">
      <div v-if="loading" class="loading">
        <div class="loading-spinner"></div>
        <p>Executando consulta...</p>
      </div>
      <div v-else class="no-data">
        <div class="no-data-icon">📊</div>
        <p>Selecione métricas e dimensões para ver os dados</p>
        <small>Clique em "Executar Consulta" para gerar a visualização</small>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import { formatNumber, formatCurrency } from '../utils/formatters.js'

Chart.register(...registerables)

export default {
  name: 'QueryBuilder',
  setup() {
    // Dados disponíveis
    const availableMetrics = ref([])
    const availableDimensions = ref([])
    
    // Listas dinâmicas para filtros
    const availableStores = ref([])
    const availableChannels = ref([])
    const availableCategories = ref([])
    const availableProducts = ref([])
    const daysOfWeek = ref([
      { value: '1', label: 'Segunda-feira' },
      { value: '2', label: 'Terça-feira' },
      { value: '3', label: 'Quarta-feira' },
      { value: '4', label: 'Quinta-feira' },
      { value: '5', label: 'Sexta-feira' },
      { value: '6', label: 'Sábado' },
      { value: '0', label: 'Domingo' }
    ])
    
    // Estado da query
    const selectedMetrics = ref([])
    const selectedDimensions = ref([])
    const filters = ref({
      data: '',
      hora: '',
      dia_semana: '',
      loja: '',
      canal: '',
      categoria: '',
      produto: ''
    })
    
    // Resultados e visualização
    const queryResult = ref(null)
    const loading = ref(false)
    const lineChart = ref(null)
    let chartInstance = null

    // Computed
    const canRunQuery = computed(() => {
      return selectedMetrics.value.length > 0 && selectedDimensions.value.length > 0
    })

    // Métodos
    const loadAvailableData = async () => {
      try {
        // Carregar métricas e dimensões
        availableMetrics.value = [
          { id: 'total_vendas', name: 'TOTAL VENDAS', expression: 'COUNT(*)' },
          { id: 'faturamento_total', name: 'FATURAMENTO TOTAL', expression: 'SUM(valor_total)' },
          { id: 'ticket_medio', name: 'TICKET MEDIO', expression: 'AVG(valor_total)' },
          { id: 'total_descontos', name: 'TOTAL DESCONTOS', expression: 'SUM(desconto)' },
          { id: 'produtos_vendidos', name: 'PRODUTOS VENDIDOS', expression: 'SUM(quantidade)' },
          { id: 'vezes_vendido', name: 'VEZES VENDIDO', expression: 'COUNT(DISTINCT pedido_id)' }
        ]
        
        availableDimensions.value = [
          { id: 'data', name: 'Data', type: 'date' },
          { id: 'hora', name: 'Hora', type: 'time' },
          { id: 'dia_semana', name: 'Dia Semana', type: 'string' },
          { id: 'loja', name: 'Loja', type: 'string' },
          { id: 'canal', name: 'Canal', type: 'string' },
          { id: 'categoria', name: 'Categoria', type: 'string' },
          { id: 'produto', name: 'Produto', type: 'string' }
        ]

        // Carregar dados dinâmicos para filtros
        await loadDynamicFilterData()

      } catch (error) {
        console.error('Erro ao carregar dados:', error)
      }
    }

    const loadDynamicFilterData = async () => {
      try {
        availableStores.value = [
          { id: '1', nome: 'Loja Centro' },
          { id: '2', nome: 'Loja Shopping' },
          { id: '3', nome: 'Loja Zona Sul' },
          { id: '4', nome: 'Loja Zona Norte' }
        ]

        availableChannels.value = ['iFood', 'Rappi', 'Balcão', 'WhatsApp', 'App Próprio', 'Telefone']
        availableCategories.value = ['Lanches', 'Bebidas', 'Sobremesas', 'Combos', 'Promoções']

        availableProducts.value = [
          { id: '1', nome: 'Hambúrguer Clássico' },
          { id: '2', nome: 'Hambúrguer Especial' },
          { id: '3', nome: 'Pizza Margherita' },
          { id: '4', nome: 'Pizza Calabresa' },
          { id: '5', nome: 'Refrigerante' },
          { id: '6', nome: 'Suco Natural' },
          { id: '7', nome: 'Batata Frita' },
          { id: '8', nome: 'Combo Família' }
        ]
      } catch (error) {
        console.error('Erro ao carregar dados dos filtros:', error)
      }
    }

    const toggleMetric = (metricId) => {
      const index = selectedMetrics.value.indexOf(metricId)
      if (index > -1) {
        selectedMetrics.value.splice(index, 1)
      } else {
        selectedMetrics.value.push(metricId)
      }
    }

    const toggleDimension = (dimensionId) => {
      const index = selectedDimensions.value.indexOf(dimensionId)
      if (index > -1) {
        selectedDimensions.value.splice(index, 1)
        filters.value[dimensionId] = ''
      } else {
        selectedDimensions.value.push(dimensionId)
      }
    }

    // Métodos de atualização de filtros
    const updateDateFilter = () => {
      console.log('Filtro de data atualizado:', filters.value.data)
    }

    const updateTimeFilter = () => {
      console.log('Filtro de hora atualizado:', filters.value.hora)
    }

    const updateDayFilter = () => {
      console.log('Filtro de dia da semana atualizado:', filters.value.dia_semana)
    }

    const updateStoreFilter = () => {
      console.log('Filtro de loja atualizado:', filters.value.loja)
    }

    const updateChannelFilter = () => {
      console.log('Filtro de canal atualizado:', filters.value.canal)
    }

    const updateCategoryFilter = () => {
      console.log('Filtro de categoria atualizado:', filters.value.categoria)
    }

    const updateProductFilter = () => {
      console.log('Filtro de produto atualizado:', filters.value.produto)
    }

    const runQuery = async () => {
      if (!canRunQuery.value) return
      
      loading.value = true
      queryResult.value = null
      
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        const mockData = generateMockData()
        queryResult.value = mockData
        
        nextTick(() => {
          createLineChart()
        })
        
      } catch (error) {
        console.error('Erro na consulta:', error)
        alert('Erro ao executar consulta: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    const generateMockData = () => {
      const dimensions = selectedDimensions.value
      const metrics = selectedMetrics.value
      
      const filteredData = generateFilteredMockData(dimensions, metrics)
      
      const columns = [
        ...dimensions.map(dim => ({
          name: availableDimensions.value.find(d => d.id === dim)?.name || dim
        })),
        ...metrics.map(metric => ({
          name: availableMetrics.value.find(m => m.id === metric)?.name || metric
        }))
      ]
      
      return { data: filteredData, columns }
    }

    const generateFilteredMockData = (dimensions, metrics) => {
      const data = []
      const baseCount = dimensions.includes('hora') ? 24 : 
                      dimensions.includes('data') ? 30 : 10
      
      for (let i = 0; i < baseCount; i++) {
        const row = {}
        
        // Preencher dimensões
        dimensions.forEach(dim => {
          const dimName = availableDimensions.value.find(d => d.id === dim)?.name || dim
          switch(dim) {
            case 'data':
              const date = new Date()
              date.setDate(date.getDate() - i)
              row[dimName] = date.toISOString().split('T')[0]
              break
            case 'hora':
              row[dimName] = `${i}h`
              break
            case 'dia_semana':
              const days = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
              row[dimName] = days[i % 7]
              break
            case 'loja':
              const stores = availableStores.value
              row[dimName] = stores[i % stores.length]?.nome || 'Loja Padrão'
              break
            case 'canal':
              const channels = availableChannels.value
              row[dimName] = channels[i % channels.length]
              break
            case 'categoria':
              const categories = availableCategories.value
              row[dimName] = categories[i % categories.length]
              break
            case 'produto':
              const products = availableProducts.value
              row[dimName] = products[i % products.length]?.nome || 'Produto Padrão'
              break
          }
        })
        
        // Preencher métricas
        metrics.forEach(metric => {
          const metricName = availableMetrics.value.find(m => m.id === metric)?.name || metric
          switch(metric) {
            case 'total_vendas':
              row[metricName] = Math.floor(Math.random() * 100) + 20
              break
            case 'faturamento_total':
              row[metricName] = Math.floor(Math.random() * 5000) + 1000
              break
            case 'ticket_medio':
              row[metricName] = Math.floor(Math.random() * 50) + 30
              break
            case 'total_descontos':
              row[metricName] = Math.floor(Math.random() * 200) + 50
              break
            case 'produtos_vendidos':
              row[metricName] = Math.floor(Math.random() * 200) + 50
              break
            case 'vezes_vendido':
              row[metricName] = Math.floor(Math.random() * 50) + 10
              break
          }
        })
        
        data.push(row)
      }
      
      return data
    }

    const createLineChart = () => {
      if (!lineChart.value || !queryResult.value) return

      // Destruir gráfico existente
      if (chartInstance) {
        chartInstance.destroy()
      }

      const ctx = lineChart.value.getContext('2d')
      const data = prepareChartData()

      if (!data) return

      chartInstance = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom'
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  let label = context.dataset.label || ''
                  if (label) label += ': '
                  if (context.parsed !== null) {
                    if (context.dataset.label?.toLowerCase().includes('faturamento')) {
                      label += formatCurrency(context.parsed)
                    } else {
                      label += formatNumber(context.parsed)
                    }
                  }
                  return label
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  if (value >= 1000) {
                    return formatNumber(value)
                  }
                  return value
                }
              }
            }
          }
        }
      })
    }

    const prepareChartData = () => {
      if (!queryResult.value || queryResult.value.data.length === 0) return null

      const data = queryResult.value.data
      const columns = queryResult.value.columns

      const dimensionCols = columns.filter(col => 
        selectedDimensions.value.some(dim => 
          col.name.toLowerCase().includes(dim.toLowerCase().replace('_', ' '))
        )
      )
      const metricCols = columns.filter(col => 
        selectedMetrics.value.some(metric => 
          col.name.toLowerCase().includes(metric.toLowerCase().replace('_', ' '))
        )
      )

      if (dimensionCols.length === 0 || metricCols.length === 0) return null

      const dimension = dimensionCols[0].name
      const metric = metricCols[0].name

      return {
        labels: data.map(item => String(item[dimension])),
        datasets: [{
          label: metric,
          data: data.map(item => Number(item[metric])),
          borderColor: '#3498db',
          backgroundColor: 'rgba(52, 152, 219, 0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4
        }]
      }
    }

    const saveToDashboard = () => {
      if (!queryResult.value) return
      
      const visualizationConfig = {
        metrics: selectedMetrics.value,
        dimensions: selectedDimensions.value,
        filters: filters.value,
        data: queryResult.value,
        createdAt: new Date().toISOString()
      }
      
      const savedCharts = JSON.parse(localStorage.getItem('savedCharts') || '[]')
      savedCharts.push(visualizationConfig)
      localStorage.setItem('savedCharts', JSON.stringify(savedCharts))
      
      alert('Visualização salva no dashboard!')
    }

    onMounted(() => {
      loadAvailableData()
    })

    return {
      availableMetrics,
      availableDimensions,
      availableStores,
      availableChannels,
      availableCategories,
      availableProducts,
      daysOfWeek,
      selectedMetrics,
      selectedDimensions,
      filters,
      queryResult,
      loading,
      lineChart,
      canRunQuery,
      toggleMetric,
      toggleDimension,
      updateDateFilter,
      updateTimeFilter,
      updateDayFilter,
      updateStoreFilter,
      updateChannelFilter,
      updateCategoryFilter,
      updateProductFilter,
      runQuery,
      saveToDashboard
    }
  }
}
</script>

<style scoped>
.query-builder {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.builder-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.builder-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #e9ecef;
}

.builder-section h4 {
  margin-bottom: 15px;
  color: #2c3e50;
  font-size: 1.2rem;
}

.items-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 400px;
  overflow-y: auto;
  padding: 10px;
}

.item-card {
  padding: 15px;
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.item-card:hover {
  border-color: #3498db;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.item-card.selected {
  border-color: #27ae60;
  background: #d4edda;
}

.item-name {
  font-weight: bold;
  color: #2c3e50;
  font-size: 14px;
}

.filter-group {
  margin-bottom: 15px;
}

.filter-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #2c3e50;
  font-size: 14px;
}

.filter-group select, .filter-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.dynamic-filters {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e9ecef;
}

.actions-section {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.btn-run, .btn-save {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  font-size: 14px;
}

.btn-run {
  background: #27ae60;
  color: white;
}

.btn-run:hover:not(:disabled) {
  background: #219653;
  transform: translateY(-2px);
}

.btn-run:disabled {
  background: #95a5a6;
  cursor: not-allowed;
  transform: none;
}

.btn-save {
  background: #3498db;
  color: white;
}

.btn-save:hover:not(:disabled) {
  background: #2980b9;
  transform: translateY(-2px);
}

.btn-save:disabled {
  background: #95a5a6;
  cursor: not-allowed;
  transform: none;
}

.multi-visualization {
  margin-top: 30px;
  background: #f8f9fa;
  padding: 25px;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.multi-visualization h4 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 1.3rem;
  text-align: center;
}

.viz-container {
  min-height: 500px;
  position: relative;
}

.viz-panel {
  background: white;
  padding: 25px;
  border-radius: 10px;
  border: 1px solid #e9ecef;
  height: 100%;
}

.viz-panel h5 {
  margin-bottom: 20px;
  color: #2c3e50;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 10px;
  font-size: 1.1rem;
}

.chart-container {
  height: 400px;
  position: relative;
}

.chart-container canvas {
  width: 100% !important;
  height: 100% !important;
}

.chart-placeholder {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
  font-style: italic;
  background: #f8f9fa;
  border-radius: 8px;
  border: 2px dashed #e9ecef;
}

.placeholder-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  opacity: 0.5;
}

.preview-section {
  text-align: center;
  padding: 60px 20px;
  background: #f8f9fa;
  border-radius: 12px;
  border: 2px dashed #e9ecef;
  margin: 20px 0;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.no-data-icon {
  font-size: 4rem;
  opacity: 0.7;
}

.no-data p {
  color: #2c3e50;
  font-size: 1.2rem;
  margin: 0;
}

.no-data small {
  color: #7f8c8d;
  font-size: 0.9rem;
}

@media (max-width: 1024px) {
  .builder-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .builder-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-section {
    flex-direction: column;
    align-items: center;
  }
  
  .btn-run, .btn-save {
    width: 100%;
    max-width: 300px;
  }
  
  .items-grid {
    max-height: 300px;
  }
}

@media (max-width: 480px) {
  .query-builder {
    padding: 10px;
  }
  
  .builder-section {
    padding: 15px;
  }
  
  .multi-visualization {
    padding: 15px;
  }
  
  .viz-panel {
    padding: 15px;
  }
  
  .chart-container {
    height: 300px;
  }
}
</style>