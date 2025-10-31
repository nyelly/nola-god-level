<template>
  <div class="top-products">
    <div v-if="loading" class="loading">Carregando produtos...</div>
    <div v-else-if="data.length === 0" class="empty-state">
      <div class="empty-icon">📊</div>
      <p>Nenhum dado de produtos disponível</p>
      <small>Execute: REFRESH MATERIALIZED VIEW mv_top_products;</small>
    </div>
    <div v-else class="products-list">
      <div 
        v-for="(product, index) in data" 
        :key="product.product_id"
        class="product-item"
        :class="{ 'top-3': index < 3 }"
      >
        <div class="product-rank">
          <span class="rank-number">#{{ index + 1 }}</span>
          <span class="rank-medal" v-if="index < 3">🏆</span>
        </div>
        
        <div class="product-info">
          <div class="product-name">{{ product.produto || `Produto ${product.product_id}` }}</div>
          <div class="product-category" v-if="product.categoria">{{ product.categoria }}</div>
        </div>
        
        <div class="product-stats">
          <div class="stat">
            <span class="stat-value">{{ formatNumber(product.vezes_vendido) }}</span>
            <span class="stat-label">vendas</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ formatCurrency(product.receita_total) }}</span>
            <span class="stat-label">receita</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'TopProducts',
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
    
    return {
      formatNumber,
      formatCurrency
    }
  }
}
</script>

<style scoped>
.top-products {
  max-height: 400px;
  overflow-y: auto;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #7f8c8d;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.products-list {
  space-y: 10px;
}

.product-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 8px;
  transition: all 0.3s ease;
}

.product-item.top-3 {
  background: linear-gradient(135deg, #fff3cd, #ffeaa7);
  border: 2px solid #ffd43b;
}

.product-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.product-rank {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 15px;
  min-width: 40px;
}

.rank-number {
  font-weight: bold;
  font-size: 1.2rem;
  color: #2c3e50;
}

.rank-medal {
  font-size: 0.8rem;
}

.product-info {
  flex: 1;
}

.product-name {
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 4px;
}

.product-category {
  font-size: 0.8rem;
  color: #7f8c8d;
  background: #e9ecef;
  padding: 2px 8px;
  border-radius: 12px;
  display: inline-block;
}

.product-stats {
  text-align: right;
}

.stat {
  margin-bottom: 4px;
}

.stat-value {
  font-weight: bold;
  color: #27ae60;
  display: block;
  font-size: 0.9rem;
}

.stat-label {
  font-size: 0.7rem;
  color: #7f8c8d;
  text-transform: uppercase;
}

/* Scrollbar */
.products-list::-webkit-scrollbar {
  width: 6px;
}

.products-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.products-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}
</style>