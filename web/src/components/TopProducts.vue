<template>
  <div class="top-products">
    <div v-if="loading" class="loading">Carregando produtos...</div>
    <div v-else-if="products.length === 0" class="no-data">
      Nenhum produto vendido ainda
    </div>
    <div v-else class="products-list">
      <div 
        v-for="(product, index) in products" 
        :key="product.product_id || index"
        class="product-item"
      >
        <div class="product-rank">#{{ index + 1 }}</div>
        
        <div class="product-info">
          <div class="product-name">{{ product.produto }}</div>
          <div class="product-stats">
            <div class="stat">
              <span class="stat-value">{{ formatNumber(product.vezes_vendido) }} vendidos</span>
            </div>
            <div class="stat stat-revenue">
              <span class="stat-label">receita</span>
              <span class="stat-value">{{ formatCurrency(product.receita_total) }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="products.length < 5" class="info-message">
        Apenas {{ products.length }} produto(s) encontrado(s)
      </div>
    </div>
  </div>
</template>

<script>
import { formatNumber, formatCurrency } from '../utils/formatters'

export default {
  name: 'TopProducts',
  props: {
    products: Array, 
    loading: Boolean
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
.top-products {
  max-height: 400px;
  overflow-y: auto;
  padding: 20px;
}

.loading, .no-data {
  text-align: center;
  padding: 40px 20px;
  color: #7f8c8d;
  font-size: 1.1rem;
}

.products-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.product-item {
  display: flex;
  align-items: flex-start;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  width: 100%;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.product-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.product-rank {
  font-weight: bold;
  font-size: 1.3rem;
  color: #2c3e50;
  margin-right: 20px;
  min-width: 40px;
}

.product-info {
  flex: 1;
}

.product-name {
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 8px;
  font-size: 1.2rem;
}

.product-stats {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat {
  display: block;
}

.stat-value {
  font-weight: bold;
  color: #2c3e50;
  font-size: 1rem;
  display: block;
}

.stat-label {
  font-size: 0.8rem;
  color: #7f8c8d;
  text-transform: lowercase;
  display: block;
}

.stat-revenue {
  margin-top: 8px;
}

.stat-revenue .stat-value {
  color: #27ae60;
  font-size: 1.1rem;
  font-weight: bold;
}

.top-products::-webkit-scrollbar {
  width: 6px;
}

.top-products::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.top-products::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.info-message {
  text-align: center;
  padding: 15px;
  color: #7f8c8d;
  font-style: italic;
  margin-top: 10px;
}
</style>