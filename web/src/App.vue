<template>
  <div id="app">
    <div class="dashboard-header">
      <h1 class="dashboard-title">🍔 Nola Analytics</h1>
      <p class="dashboard-subtitle">Dashboard de Analytics para Restaurantes</p>
    </div>
    
    <div class="container">
      <Dashboard />
    </div>
  </div>
</template>

<script>
import Dashboard from './components/Dashboard.vue'

export default {
  name: 'App',
  components: {
    Dashboard
  }
}
</script>