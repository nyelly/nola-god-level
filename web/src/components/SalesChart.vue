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
      if (!chartCanvas.value) return
      
      if (chartInstance) {
        chartInstance.destroy()
      }
      
      const ctx = chartCanvas.value.getContext('2d')
      
      const labels = ['01', '05', '10', '15', '20', '25', '30']
      const valores = [520000, 525000, 530000, 535000, 545000, 555000, 570000]
      
      chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Vendas',
            data: valores,
            borderColor: 'red',
            backgroundColor: 'rgba(255, 0, 0, 0.1)',
            borderWidth: 2,
            fill: true
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              ticks: {
                callback: function(value) {
                  return value.toLocaleString('pt-BR')
                }
              }
            }
          }
        }
      })
    }
    
    onMounted(() => {
      createChart()
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
}
</style>