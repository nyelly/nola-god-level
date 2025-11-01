<template>
  <div class="kpi-cards">
    <div class="cards-grid">
      <!-- Total de Vendas -->
      <div class="kpi-card">
        <div class="kpi-value">{{ formatNumber(kpis.total_vendas) }}</div>
        <div class="kpi-label">Vendas Hoje</div>
      </div>
      
      <!-- Faturamento -->
      <div class="kpi-card">
        <div class="kpi-value">{{ formatCurrency(kpis.faturamento_total) }}</div>
        <div class="kpi-label">Faturamento</div>
      </div>
      
      <!-- Ticket Médio -->
      <div class="kpi-card">
        <div class="kpi-value">{{ formatCurrency(kpis.ticket_medio) }}</div>
        <div class="kpi-label">Ticket Médio</div>
      </div>
      
      <!-- Descontos -->
      <div class="kpi-card">
        <div class="kpi-value">{{ formatCurrency(kpis.total_descontos) }}</div>
        <div class="kpi-label">Descontos</div>
      </div>
    </div>
    
    <div v-if="loading" class="loading">Carregando métricas...</div>
  </div>
</template>

<script>
import { formatNumber, formatCurrency } from '../utils/formatters'

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

.cards-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: 15px;
}

.kpi-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.kpi-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 5px;
}

.kpi-label {
  font-size: 0.9rem;
  color: #7f8c8d;
}

@media (max-width: 768px) {
  .cards-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 480px) {
  .cards-grid {
    grid-template-columns: 1fr;
  }
}
</style>