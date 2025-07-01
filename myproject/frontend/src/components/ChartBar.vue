<!-- src/components/ChartBar.vue -->
<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale
} from 'chart.js'

// Registrasi Chart.js
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'ChartBar',
  components: { Bar },
  props: {
    chartData: Object,
    chartOptions: Object
  }
}
</script>
