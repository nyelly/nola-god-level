<template>
  <div class="sales-chart">
    <div v-if="loading" class="loading">Carregando gráfico...</div>
    <canvas v-else ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
  name: 'SalesChart',
  props: {
    data: Array,
    loading: Boolean
  },
  setup(props) {
    const chartCanvas = ref(null)
    let chartInstance = null
    
    const createChart = () => {
      if (!chartCanvas.value || !props.data.length) return
      
      if (chartInstance) {
        chartInstance.destroy()
      }
      
      const ctx = chartCanvas.value.getContext('2d')
      
      chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: props.data.map(item => {
            const date = new Date(item.data)
            return date.toLocaleDateString('pt-BR')
          }),
          datasets: [{
            label: 'Faturamento Diário (R$)',
            data: props.data.map(item => item.valor),
            borderColor: '#3498db',
            backgroundColor: 'rgba(52, 152, 219, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Evolução do Faturamento'
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              ticks: {
                callback: function(value) {
                  return 'R$ ' + value.toLocaleString('pt-BR')
                }
              }
            }
          }
        }
      })
    }
    
    onMounted(() => {
      if (props.data.length) {
        createChart()
      }
    })
    
    watch(() => props.data, (newData) => {
      if (newData.length) {
        createChart()
      }
    })
    
    return {
      chartCanvas
    }
  }
}
</script>

<style scoped>
.sales-chart {
  height: 300px;
  position: relative;
}
</style>