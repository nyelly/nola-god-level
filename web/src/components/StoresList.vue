<template>
  <div class="stores-list">
    <div v-if="loading" class="loading">Carregando lojas...</div>
    <div v-else class="stores-container">
      <div 
        v-for="store in data" 
        :key="store.id"
        class="store-item"
        :class="{ 'inactive': !store.ativo }"
      >
        <div class="store-icon">🏪</div>
        
        <div class="store-info">
          <div class="store-name">{{ store.nome }}</div>
          <div class="store-location">
            <span class="city">{{ store.cidade }}</span>
            <span class="state">- {{ store.estado }}</span>
          </div>
        </div>
        
        <div class="store-status">
          <span 
            class="status-badge"
            :class="store.ativo ? 'active' : 'inactive'"
          >
            {{ store.ativo ? 'Ativa' : 'Inativa' }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StoresList',
  props: {
    data: Array,
    loading: Boolean
  }
}
</script>

<style scoped>
.stores-list {
  max-height: 400px;
  overflow-y: auto;
}

.stores-container {
   margin-bottom: 8px;
}

.store-item {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #27ae60;
  transition: all 0.3s ease;
}

.store-item.inactive {
  border-left-color: #95a5a6;
  opacity: 0.7;
}

.store-item:hover {
  transform: translateX(5px);
  background: #e9ecef;
}

.store-icon {
  font-size: 1.5rem;
  margin-right: 15px;
}

.store-info {
  flex: 1;
}

.store-name {
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 4px;
}

.store-location {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.city {
  font-weight: 500;
}

.state {
  font-style: italic;
}

.store-status {
  margin-left: 10px;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
}

.status-badge.active {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.status-badge.inactive {
  background: #e2e3e5;
  color: #383d41;
  border: 1px solid #d6d8db;
}

.stores-container::-webkit-scrollbar {
  width: 6px;
}

.stores-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.stores-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}
</style>