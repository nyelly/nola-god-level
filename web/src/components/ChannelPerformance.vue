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
import { formatNumber, formatCurrency } from '../utils/formatters'

export default {
  name: 'ChannelPerformance',
  props: {
    data: Array,
    loading: Boolean
  },
  setup() {
    const getChannelIcon = (channelName) => {
      const icons = {
        'Balcão': '',
        'iFood': '',
        'Rappi': '',
        'WhatsApp': '',
        'App Próprio': '',
        'Telefone': '',
        'Uber Eats': ''
      }
      return icons[channelName] || ''
    }
    
    const getChannelPercentage = (faturamento, totalFaturamento = 10000000) => {
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

.canal {
  margin-bottom: 15px;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  border-left: 4px solid #3498db;
  transition: all 0.3s ease;
}

.canal:hover {
  transform: translateX(5px);
  background: #e9ecef;
}

.info {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  margin-bottom: 12px;
  align-items: center;
}

.info strong {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1rem;
}

.info span {
  color: #7f8c8d;
  font-weight: 500;
}

.barra {
  background: #e0e0e0;
  height: 10px;
  border-radius: 5px;
  margin: 8px 0;
  overflow: hidden;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.preenchido {
  background: linear-gradient(90deg, #ff6b6b, #ff8e8e);
  height: 10px;
  border-radius: 5px;
  transition: width 1s ease-in-out;
  box-shadow: 0 2px 8px rgba(255, 59, 59, 0.3);
  position: relative;
}

.preenchido::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, 
    rgba(255,255,255,0.3) 0%, 
    rgba(255,255,255,0.1) 50%, 
    rgba(255,255,255,0.3) 100%);
  border-radius: 5px;
}

.valor {
  font-weight: bold;
  color: #2c3e50;
  font-size: 14px;
  text-align: right;
  margin-top: 5px;
  font-size: 0.95rem;
}

.channel-item {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 15px;
  border-left: 4px solid #3498db;
  transition: all 0.3s ease;
}

.channel-item:hover {
  transform: translateX(5px);
  background: #e9ecef;
}

.channel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
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
  gap: 12px;
  margin-bottom: 12px;
}

.stat {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  align-items: center;
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
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
  margin: 8px 0;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #db3434, #b92929);
  border-radius: 4px;
  transition: width 0.5s ease-in-out;
  position: relative;
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, 
    rgba(255,255,255,0.3) 0%, 
    rgba(255,255,255,0.1) 50%, 
    rgba(255,255,255,0.3) 100%);
  border-radius: 4px;
}

.channels-list::-webkit-scrollbar {
  width: 8px;
}

.channels-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.channels-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
  transition: background 0.3s ease;
}

.channels-list::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Estados de loading */
.loading {
  text-align: center;
  padding: 40px 20px;
  color: #7f8c8d;
  font-style: italic;
}

/* Responsividade */
@media (max-width: 768px) {
  .canal, .channel-item {
    padding: 15px;
    margin-bottom: 12px;
  }
  
  .channel-stats {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  
  .info {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .barra, .progress-bar {
    height: 8px;
  }
}
</style>
