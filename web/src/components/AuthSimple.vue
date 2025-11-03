<template>
  <div class="auth-simple">
    <div class="login-container">
      <div class="login-card">
        <div class="logo-section">
          <h1>🍔 Nola Analytics</h1>
          <p>Sistema de Analytics para Restaurantes</p>
        </div>
        
        <div class="login-form">
          <div class="input-group">
            <label for="username">👤 Nome de usuário</label>
            <input 
              type="text" 
              id="username"
              v-model="username"
              placeholder="Digite seu Nome"
              @keyup.enter="proceedToAuthComplete"
            >
          </div>
          
          <div class="login-options">
            <label class="remember-me">
              <input type="checkbox" v-model="rememberMe">
              <span>Lembre-se de mim</span>
            </label>
          </div>
          
          <button 
            class="login-btn"
            @click="proceedToAuthComplete"
            :disabled="!username"
          >
            LOGIN
          </button>
        </div>
        
        <div class="footer">
          <p>Entre com seu Nome para continuar</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'AuthSimple',
  emits: ['proceed-to-auth-complete'],
  setup(props, { emit }) {
    const username = ref('')
    const rememberMe = ref(false)

    const proceedToAuthComplete = () => {
      if (username.value.trim()) {
        emit('proceed-to-auth-complete', {
          username: username.value,
          rememberMe: rememberMe.value
        })
      }
    }

    return {
      username,
      rememberMe,
      proceedToAuthComplete
    }
  }
}
</script>

<style scoped>
.auth-simple {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 400px;
}

.login-card {
  background: white;
  border-radius: 15px;
  padding: 40px 30px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.logo-section h1 {
  color: #2c3e50;
  font-size: 2rem;
  margin-bottom: 10px;
}

.logo-section p {
  color: #7f8c8d;
  margin-bottom: 30px;
  font-size: 1rem;
}

.input-group {
  margin-bottom: 20px;
  text-align: left;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #2c3e50;
  font-size: 0.9rem;
}

.input-group input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.input-group input:focus {
  outline: none;
  border-color: #3498db;
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  font-size: 0.9rem;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #2c3e50;
  cursor: pointer;
}

.remember-me input {
  margin: 0;
}

.forgot-password {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

.forgot-password:hover {
  text-decoration: underline;
}

.login-btn {
  width: 100%;
  padding: 12px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-btn:hover:not(:disabled) {
  background: #2980b9;
  transform: translateY(-2px);
}

.login-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
}

.footer {
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #e9ecef;
}

.footer p {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin: 0;
}

@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }
  
  .logo-section h1 {
    font-size: 1.7rem;
  }
  
  .login-options {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
}
</style>