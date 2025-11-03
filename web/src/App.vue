<template>
  <div id="app">
    <!-- Tela Simples de Login -->
    <AuthSimple 
      v-if="currentScreen === 'auth-simple'"
      @proceed-to-auth-complete="handleSimpleAuth"
    />
    
    <!-- Tela Completa de Login -->
    <AuthComplete 
      v-else-if="currentScreen === 'auth-complete'"
      :prefill-data="loginData"
      @login-success="handleLoginSuccess"
      @go-back="goBackToSimpleAuth"
    />
    
    <div v-else class="dashboard-container">
      <Dashboard />
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import AuthSimple from './components/AuthSimple.vue'
import AuthComplete from './components/AuthComplete.vue'
import Dashboard from './components/Dashboard.vue'

export default {
  name: 'App',
  components: {
    AuthSimple,
    AuthComplete,
    Dashboard
  },
  setup() {
    const currentScreen = ref('auth-simple')
    const loginData = ref({})

    const handleSimpleAuth = (data) => {
      loginData.value = data
      currentScreen.value = 'auth-complete'
    }

    const handleLoginSuccess = (userData) => {
      console.log('Login realizado:', userData)
      currentScreen.value = 'dashboard'
    }

    const goBackToSimpleAuth = () => {
      currentScreen.value = 'auth-simple'
      loginData.value = {}
    }

    return {
      currentScreen,
      loginData,
      handleSimpleAuth,
      handleLoginSuccess,
      goBackToSimpleAuth
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #2c3e50;
  line-height: 1.6;
  min-height: 100vh;
}

#app {
  min-height: 100vh;
}

.dashboard-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}
</style>