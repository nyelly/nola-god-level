<template>
  <div class="auth-complete">
    <div class="login-container">
      <div class="login-card">
        <div class="header">
          <button class="back-btn" @click="goBack">
            ← Voltar
          </button>
          <h1>🔐 Login Completo</h1>
          <p>Bem-vindo de volta, {{ prefillUsername }}</p>
        </div>
        
        <div class="login-form">
          <div class="input-group">
            <label for="username">👤 nome de usuário</label>
            <input 
              type="text" 
              id="username"
              v-model="username"
              :placeholder="prefillUsername"
              readonly
            >
          </div>
          
          <div class="input-group">
            <label for="password">🔒 Senha</label>
            <input 
              type="password" 
              id="password"
              v-model="password"
              placeholder="Digite sua senha"
              @keyup.enter="handleLogin"
            >
          </div>
          
          <div class="login-options">
            <label class="remember-me">
              <input type="checkbox" v-model="rememberMe">
              <span>Manter conectado</span>
            </label>
          </div>
          
          <button 
            class="login-btn"
            @click="handleLogin"
            :disabled="!password"
          >
            ENTRAR NO SISTEMA
          </button>
        </div>
        
        <div class="security-notice">
          <p>🔒 Suas credenciais são protegidas com criptografia</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'AuthComplete',
  props: {
    prefillData: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['login-success', 'go-back'],
  setup(props, { emit }) {
    const username = ref('')
    const password = ref('')
    const projectPassword = ref('')
    const rememberMe = ref(false)

    onMounted(() => {
      username.value = props.prefillData.username || ''
      rememberMe.value = props.prefillData.rememberMe || false
    })

    const prefillUsername = props.prefillData.username || 'Usuário'

    const handleLogin = () => {
      if (password.value.trim()) {
        const userData = {
          username: username.value,
          rememberMe: rememberMe.value,
          project: projectPassword.value ? 'Com projeto' : 'Sem projeto'
        }
        emit('login-success', userData)
      }
    }

    const goBack = () => {
      emit('go-back')
    }

    return {
      username,
      password,
      projectPassword,
      rememberMe,
      prefillUsername,
      handleLogin,
      goBack
    }
  }
}
</script>

<style scoped>
.auth-complete {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 450px;
}

.login-card {
  background: white;
  border-radius: 15px;
  padding: 40px 30px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.header {
  text-align: center;
  margin-bottom: 30px;
  position: relative;
}

.back-btn {
  position: absolute;
  left: 0;
  top: 0;
  background: none;
  border: 1px solid #e9ecef;
  padding: 8px 15px;
  border-radius: 6px;
  cursor: pointer;
  color: #7f8c8d;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: #f8f9fa;
  border-color: #3498db;
  color: #3498db;
}

.header h1 {
  color: #2c3e50;
  font-size: 1.8rem;
  margin-bottom: 8px;
}

.header p {
  color: #7f8c8d;
  margin: 0;
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

.input-group input:read-only {
  background: #f8f9fa;
  color: #7f8c8d;
  cursor: not-allowed;
}

.login-options {
  margin-bottom: 25px;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #2c3e50;
  cursor: pointer;
  font-size: 0.9rem;
}

.remember-me input {
  margin: 0;
}

.login-btn {
  width: 100%;
  padding: 14px;
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.login-btn:hover:not(:disabled) {
  background: #219653;
  transform: translateY(-2px);
}

.login-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
}

.security-notice {
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #e9ecef;
  text-align: center;
}

.security-notice p {
  color: #7f8c8d;
  font-size: 0.8rem;
  margin: 0;
}

@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }
  
  .header h1 {
    font-size: 1.5rem;
  }
  
  .back-btn {
    position: relative;
    margin-bottom: 15px;
    width: 100%;
  }
}
</style>