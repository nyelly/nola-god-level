<template>
  <div class="channel-performance">
    <div v-if="loading" class="loading">Carregando canais...</div>
    <div v-else class="channels-list">
      <div 
        v-for="channel in data" 
        :key="channel.canal"
        class="channel-item"
      >
        <div class="channel-header">
          <span class="channel-name">{{ getChannelIcon(channel.canal) }} {{ channel.canal }}</span>
          <span class="channel-revenue">{{ formatCurrency(channel.faturamento) }}</span>
        </div>
        
        <div class="channel-stats">
          <div class="stat">
            <span class="stat-label">Vendas:</span>
            <span class="stat-value">{{ formatNumber(channel.total_vendas) }}</span>
          </div>
          <div class="stat">
            <span class="stat-label">Ticket Médio:</span>
            <span class="stat-value">{{ formatCurrency(channel.faturamento / channel.total_vendas) }}</span>
          </div>
        </div>
        
        <div class="progress-bar">
          <div 
            class="progress-fill"
            :style="{ width: getChannelPercentage(channel.faturamento) + '%' }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'ChannelPerformance',
  props: {
    data: Array,
    loading: Boolean
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
    
    const getChannelIcon = (channelName) => {
      const icons = {
        'Balcão': '🏪',
        'iFood': '🛵',
        'Rappi': '🚗',
        'WhatsApp': '💬',
        'App Próprio': '📱',
        'Telefone': '📞',
        'Uber Eats': '🍔'
      }
      return icons[channelName] || '📊'
    }
    
    const getChannelPercentage = (faturamento, totalFaturamento = 10000000) => {
      // Simulação de porcentagem baseada no faturamento
      return Math.min((faturamento / totalFaturamento) * 100, 100)
    }
    
    return {
      formatNumber,
      formatCurrency,
      getChannelIcon,
      getChannelPercentage
    }
  }
}
</script>

<style scoped>
.channel-performance {
  max-height: 400px;
  overflow-y: auto;
}

.channel-item {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 10px;
  border-left: 4px solid #3498db;
}

.channel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.channel-name {
  font-weight: bold;
  color: #2c3e50;
  font-size: 1.1rem;
}

.channel-revenue {
  font-weight: bold;
  color: #27ae60;
  font-size: 1rem;
}

.channel-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 10px;
}

.stat {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
}

.stat-label {
  color: #7f8c8d;
}

.stat-value {
  font-weight: bold;
  color: #2c3e50;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3498db, #2980b9);
  border-radius: 3px;
  transition: width 0.3s ease;
}

/* Scrollbar personalizada */
.channels-list::-webkit-scrollbar {
  width: 6px;
}

.channels-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.channels-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.channels-list::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>