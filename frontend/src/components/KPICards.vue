<template>
  <div class="kpi-cards">
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <!-- Total de Vendas -->
      <div class="kpi-card">
        <div class="kpi-icon">🛒</div>
        <div class="kpi-content">
          <div class="kpi-value">{{ formatNumber(kpis.total_vendas) }}</div>
          <div class="kpi-label">Vendas Hoje</div>
        </div>
      </div>
      
      <!-- Faturamento -->
      <div class="kpi-card">
        <div class="kpi-icon">💰</div>
        <div class="kpi-content">
          <div class="kpi-value">{{ formatCurrency(kpis.faturamento_total) }}</div>
          <div class="kpi-label">Faturamento</div>
        </div>
      </div>
      
      <!-- Ticket Médio -->
      <div class="kpi-card">
        <div class="kpi-icon">📊</div>
        <div class="kpi-content">
          <div class="kpi-value">{{ formatCurrency(kpis.ticket_medio) }}</div>
          <div class="kpi-label">Ticket Médio</div>
        </div>
      </div>
      
      <!-- Descontos -->
      <div class="kpi-card">
        <div class="kpi-icon">🎫</div>
        <div class="kpi-content">
          <div class="kpi-value">{{ formatCurrency(kpis.total_descontos) }}</div>
          <div class="kpi-label">Descontos</div>
        </div>
      </div>
    </div>
    
    <div v-if="loading" class="loading">Carregando métricas...</div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'KPICards',
  props: {
    loading: Boolean,
    kpis: {
      type: Object,
      default: () => ({})
    }
  },
  setup() {
    const formatNumber = (value) => {
      if (!value) return '0'
      return new Intl.NumberFormat('pt-BR').format(value)
    }
    
    const formatCurrency = (value) => {
      if (!value) return 'R$ 0,00'
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      }).format(value)
    }
    
    return {
      formatNumber,
      formatCurrency
    }
  }
}
</script>

<style scoped>
.kpi-cards {
  margin-bottom: 2rem;
}

.kpi-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.kpi-icon {
  font-size: 2rem;
  margin-right: 15px;
}

.kpi-value {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.kpi-label {
  font-size: 0.9rem;
  opacity: 0.9;
}

@media (max-width: 768px) {
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
  
  .kpi-card {
    padding: 15px;
  }
  
  .kpi-value {
    font-size: 1.2rem;
  }
}
</style>