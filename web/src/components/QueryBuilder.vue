<template>
  <div class="query-builder">
  

    <div class="builder-grid">
      <!-- Coluna 1: Métricas -->
      <div class="builder-section">
        <h4>📊 Métricas </h4>
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

      <!-- Coluna 2: Dimensões -->
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

      <!-- Coluna 3: Filtros -->
      <div class="builder-section">
        <h4>🎯 Filtros</h4>
        
        <div class="filter-group">
          <label>Período:</label>
          <select v-model="timeRange" @change="handleTimeRangeChange">
            <option value="last_7_days">Últimos 7 dias</option>
            <option value="last_30_days">Últimos 30 dias</option>
            <option value="last_90_days">Últimos 90 dias</option>
            <option value="this_month">Este mês</option>
            <option value="last_month">Mês anterior</option>
            <option value="custom">Personalizado</option>
          </select>
        </div>

        <div v-if="timeRange === 'custom'" class="filter-group">
          <label>Data inicial:</label>
          <input type="date" v-model="startDate">
          <label>Data final:</label>
          <input type="date" v-model="endDate">
        </div>

        <!-- Filtros dinâmicos baseados nas dimensões selecionadas -->
        <div v-for="dimension in selectedDimensions" :key="'filter-' + dimension" class="filter-group">
          <label>Filtrar {{ getDimensionName(dimension) }}:</label>
          <input 
            type="text" 
            :placeholder="`Ex: iFood, Balcão...`"
            @change="updateDimensionFilter(dimension, $event.target.value)"
          >
        </div>
      </div>
    </div>

    <!-- Visualização -->
    <div class="visualization-section">
      <h4>📊 Visualização</h4>
      <div class="viz-options">
        <button 
          v-for="viz in visualizationTypes" 
          :key="viz.type"
          class="viz-btn"
          :class="{ active: visualization === viz.type }"
          @click="visualization = viz.type"
        >
          {{ viz.icon }} {{ viz.name }}
        </button>
      </div>

      <!-- Preview dos dados -->
      <div class="preview-section">
        <div v-if="loading" class="loading">Executando consulta...</div>
        <div v-else-if="queryResult" class="result-preview">
          <h5>Resultado ({{ queryResult.data.length }} registros)</h5>
          <div class="result-table">
            <table>
              <thead>
                <tr>
                  <th v-for="col in queryResult.columns" :key="col.name">{{ col.name }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in queryResult.data.slice(0, 10)" :key="index">
                  <td v-for="col in queryResult.columns" :key="col.name">
                    {{ formatValue(row[col.name], col.name) }}
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="queryResult.data.length > 10" class="more-records">
              ... e mais {{ queryResult.data.length - 10 }} registros
            </div>
          </div>
        </div>
        <div v-else class="no-data">
          👆 Selecione métricas e dimensões para ver os dados
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

      <button class="btn-template" @click="loadInsightTemplates">
        🎯 Carregar Templates
      </button>
    </div>

    <!-- Templates de Insights -->
    <div v-if="showTemplates" class="templates-section">
      <h4>💡 Insights Pré-configurados</h4>
      <div class="templates-grid">
        <div 
          v-for="insight in insightTemplates" 
          :key="insight.id"
          class="template-card"
          @click="loadTemplate(insight)"
        >
          <div class="template-icon">💡</div>
          <div class="template-content">
            <div class="template-name">{{ insight.name }}</div>
            <div class="template-desc">{{ insight.description }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { formatNumber, formatCurrency } from '../utils/formatters.js'
import { analyticsApi } from '../services/analyticsApi.js'

export default {
  name: 'QueryBuilder',
  setup() {
    // Dados disponíveis
    const availableMetrics = ref([])
    const availableDimensions = ref([])
    const insightTemplates = ref([])
    
    // Estado da query
    const selectedMetrics = ref([])
    const selectedDimensions = ref([])
    const timeRange = ref('last_30_days')
    const startDate = ref('')
    const endDate = ref('')
    const visualization = ref('table')
    const filters = ref({})
    
    // Resultados
    const queryResult = ref(null)
    const loading = ref(false)
    const showTemplates = ref(false)

    // Opções de visualização
    const visualizationTypes = [
      { type: 'table', name: 'Tabela', icon: '📋' },
      { type: 'line', name: 'Linha', icon: '📈' },
      { type: 'bar', name: 'Barras', icon: '📊' },
      { type: 'pie', name: 'Pizza', icon: '🥧' }
    ]

    // Computed
    const canRunQuery = computed(() => {
      return selectedMetrics.value.length > 0 && selectedDimensions.value.length > 0
    })

    // Métodos
    const loadAvailableData = async () => {
      try {
        const [metricsRes, dimensionsRes] = await Promise.all([
          analyticsApi.getAvailableMetrics(),
          analyticsApi.getAvailableDimensions()
        ])
        
        availableMetrics.value = Object.entries(metricsRes.data.data.metrics).map(([id, config]) => ({
          id,
          name: id.replace(/_/g, ' ').toUpperCase(),
          expression: config.expression
        }))
        
        availableDimensions.value = Object.entries(dimensionsRes.data.data.dimensions).map(([id, config]) => ({
          id,
          name: id.charAt(0).toUpperCase() + id.slice(1),
          type: config.type
        }))
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
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
        delete filters.value[dimensionId]
      } else {
        selectedDimensions.value.push(dimensionId)
      }
    }

    const updateDimensionFilter = (dimension, value) => {
      if (value.trim()) {
        filters.value[dimension] = value.split(',').map(v => v.trim())
      } else {
        delete filters.value[dimension]
      }
    }

    const getDimensionName = (dimensionId) => {
      const dimension = availableDimensions.value.find(d => d.id === dimensionId)
      return dimension ? dimension.name : dimensionId
    }

    const runQuery = async () => {
      if (!canRunQuery.value) return
      
      loading.value = true
      queryResult.value = null
      
      try {
        const query = {
          metrics: selectedMetrics.value,
          dimensions: selectedDimensions.value,
          filters: filters.value,
          time_range: timeRange.value,
          visualization: visualization.value
        }
        
        if (timeRange.value === 'custom' && startDate.value && endDate.value) {
          query.start_date = startDate.value
          query.end_date = endDate.value
        }
        
        const response = await analyticsApi.runCustomQuery(query)
        queryResult.value = response.data
      } catch (error) {
        console.error('Erro na consulta:', error)
        alert('Erro ao executar consulta: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    const formatValue = (value, columnName) => {
      if (columnName.includes('faturamento') || columnName.includes('receita')) {
        return formatCurrency(value)
      } else if (typeof value === 'number') {
        return formatNumber(value)
      }
      return value
    }

    const loadInsightTemplates = async () => {
      try {
        const response = await analyticsApi.getInsightTemplates()
        insightTemplates.value = response.data.data.insights
        showTemplates.value = true
      } catch (error) {
        console.error('Erro ao carregar templates:', error)
      }
    }

    const loadTemplate = (insight) => {
      selectedMetrics.value = [...insight.query.metrics]
      selectedDimensions.value = [...insight.query.dimensions]
      timeRange.value = insight.query.time_range
      visualization.value = insight.query.visualization
      filters.value = { ...insight.query.filters }
      showTemplates.value = false
    }

    const saveToDashboard = () => {
      alert('Funcionalidade de salvamento será implementada!')
    }

    const handleTimeRangeChange = () => {
      if (timeRange.value !== 'custom') {
        startDate.value = ''
        endDate.value = ''
      }
    }

    onMounted(() => {
      loadAvailableData()
    })

    return {
      availableMetrics,
      availableDimensions,
      insightTemplates,
      selectedMetrics,
      selectedDimensions,
      timeRange,
      startDate,
      endDate,
      visualization,
      queryResult,
      loading,
      showTemplates,
      visualizationTypes,
      canRunQuery,
      toggleMetric,
      toggleDimension,
      updateDimensionFilter,
      getDimensionName,
      runQuery,
      formatValue,
      loadInsightTemplates,
      loadTemplate,
      saveToDashboard,
      handleTimeRangeChange
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

.builder-header {
  text-align: center;
  margin-bottom: 30px;
}

.builder-header h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.builder-header p {
  color: #7f8c8d;
  font-size: 1.1rem;
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
  margin-bottom: 5px;
  font-size: 14px;
}

.item-expression, .item-type {
  font-size: 12px;
  color: #7f8c8d;
  font-family: monospace;
}

.filter-group {
  margin-bottom: 15px;
}

.filter-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #2c3e50;
}

.filter-group select, .filter-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.visualization-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.viz-options {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.viz-btn {
  padding: 10px 15px;
  border: 2px solid #e9ecef;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.viz-btn.active {
  border-color: #3498db;
  background: #3498db;
  color: white;
}

.viz-btn:hover {
  transform: translateY(-2px);
}

.preview-section {
  min-height: 200px;
}

.loading, .no-data {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
  font-style: italic;
}

.result-table {
  max-height: 400px;
  overflow: auto;
}

.result-table table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.result-table th,
.result-table td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}

.result-table th {
  background: #f8f9fa;
  font-weight: bold;
  color: #2c3e50;
}

.more-records {
  text-align: center;
  padding: 10px;
  color: #7f8c8d;
  font-style: italic;
}

.actions-section {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.btn-run, .btn-save, .btn-template {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-run {
  background: #27ae60;
  color: white;
}

.btn-run:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

.btn-save {
  background: #3498db;
  color: white;
}

.btn-save:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

.btn-template {
  background: #f39c12;
  color: white;
}

.templates-section {
  background: #fff3cd;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #ffeaa7;
}

.templates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 15px;
}

.template-card {
  display: flex;
  align-items: center;
  padding: 15px;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
}

.template-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.template-icon {
  font-size: 2rem;
  margin-right: 15px;
}

.template-name {
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 5px;
}

.template-desc {
  font-size: 0.9rem;
  color: #7f8c8d;
}

@media (max-width: 768px) {
  .builder-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-section {
    flex-direction: column;
  }
  
  .items-grid {
    max-height: 300px;
  }
}
</style>