<template>
  <div>
    <!-- Hero Section -->
    <section class="hero" id="home">
      <main class="content">
        <h1>Selamat Datang</h1>
        <p>Database Sektoral Bidang Pajak Daerah dan Retribusi Daerah</p>
        <router-link to="/produk-hukum" class="cta1">Produk Hukum</router-link>
      </main>
    </section>

    <!-- Statistik Angka -->
    <section class="stats-section" style="text-align: center; margin-top: 40px;">
      <h2>Statistik Peraturan</h2>
      <p><strong>Total Peraturan:</strong> {{ totalPeraturan }}</p>
      <div class="stats-list" style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
        <div
          v-for="stat in stats"
          :key="stat.label"
          class="stat-box"
          style="background: #f2f2f2; padding: 10px 20px; border-radius: 10px;"
        >
          <p><strong>{{ stat.label }}:</strong> {{ stat.value }}</p>
        </div>
      </div>
    </section>

    <!-- Grafik Utama -->
    <!-- <section class="chart-section">
      <h2 style="text-align:center; margin-top: 40px;">Grafik Sektoral</h2>
      <div class="chart-container" style="max-width: 700px; margin: 0 auto;">
        <ChartBar
          v-if="chartData"
          :chartData="chartData"
          :chartOptions="chartOptions"
        />
      </div>
    </section> -->

    <section
      class="chart-section"
      :class="{'no-padding-bottom': detailChartData}"
    >
      <h2 style="text-align:center; margin-top: 40px;">Grafik Sektoral</h2>
      <div class="chart-container" style="max-width: 600px; margin: 0 auto;">
        <ChartBar
          v-if="chartData"
          :chartData="chartData"
          :chartOptions="chartOptions"
        />
      </div>
    </section>

    <!-- Grafik Detail -->
    <section v-if="detailChartData" class="chart-section-detail">
      <h2 style="text-align:center; margin-top: 40px;">Grafik Detail</h2>
      <div class="chart-container" style="max-width: 700px; margin: 0 auto;">
        <ChartBar
          :chartData="detailChartData"
          :chartOptions="detailChartOptions"
        />
      </div>
    </section>
  </div>
</template>

<script>
import ChartBar from '@/components/ChartBar.vue'
import axios from 'axios'

export default {
  name: 'Hero',
  components: { ChartBar },
  data() {
    return {
      chartData: null,
      chartOptions: {},
      detailChartData: null,
      detailChartOptions: {},
      totalPeraturan: 0,
      stats: [],
      chartResponse: null
    }
  },
  async mounted() {
    try {
      const response = await axios.get('http://localhost:8000/api/chart-data/')
      this.chartResponse = response.data
      const chart = response.data.chart_all

      this.chartData = {
        labels: chart.labels,
        datasets: [
          {
            label: 'Jumlah Peraturan',
            data: chart.values,
            backgroundColor: ['#3498db', '#e67e22', '#9b59b6']
          }
        ]
      }

      this.chartOptions = {
        responsive: true,
        onClick: this.handleChartClick,
        plugins: {
          legend: { position: 'top' },
          title: {
            display: true,
            text: 'Distribusi Peraturan Berdasarkan Sektor'
          }
        }
      }

      this.totalPeraturan = chart.values.reduce((a, b) => a + b, 0)
      this.stats = chart.labels.map((label, index) => ({
        label,
        value: chart.values[index]
      }))
    } catch (error) {
      console.error('Gagal ambil data chart:', error)
    }
  },
  methods: {
    handleChartClick(evt, elements) {
      if (elements.length > 0) {
        const index = elements[0].index
        const label = this.chartData.labels[index]

        if (label === 'Pajak Daerah') {
          const data = this.chartResponse.chart_pajak
          this.detailChartData = {
            labels: data.labels,
            datasets: [
              {
                label: 'Jumlah Peraturan',
                data: data.values,
                backgroundColor: '#369EE3'
              }
            ]
          }
          this.detailChartOptions = {
            indexAxis: 'y',
            responsive: true,
            plugins: {
              legend: { position: 'top' },
              title: {
                display: true,
                text: 'Detail Pajak Daerah Berdasarkan Level 3'
              }
            }
          }
        } else if (label === 'Retribusi Daerah') {
          const data = this.chartResponse.chart_retribusi
          this.detailChartData = {
            labels: data.labels,
            datasets: [
              {
                label: 'Jumlah Peraturan',
                data: data.values,
                backgroundColor: '#f39c12'
              }
            ]
          }
          this.detailChartOptions = {
            indexAxis: 'y',
            responsive: true,
            plugins: {
              legend: { position: 'top' },
              title: {
                display: true,
                text: 'Detail Retribusi Daerah Berdasarkan Level 4'
              }
            }
          }
        } else if (label === 'Topik Umum') {
          const data = this.chartResponse.chart_topikumum
          this.detailChartData = {
            labels: data.labels,
            datasets: [
              {
                label: 'Jumlah Peraturan',
                data: data.values,
                backgroundColor: '#8e44ad'
              }
            ]
          }
          this.detailChartOptions = {
            indexAxis: 'y',
            responsive: true,
            plugins: {
              legend: { position: 'top' },
              title: {
                display: true,
                text: 'Detail Topik Umum Berdasarkan Level 3'
              }
            }
          }
        } else {
          this.detailChartData = null
        }
      }
    }
  }
}
</script>

<style scoped src="@/assets/css/main.css"></style>