<template>
  <div class="p-6">
    <Navbar />
    <h1 class="text-2xl font-bold text-center mb-6 mt-6">
      Data PDRD
    </h1>

    <!-- Dropdown Filter -->
    <div class="flex-wrap">
      <select v-model="selectedTahun" @change="fetchData" class="dropdown">
        <option value="">Pilih Tahun</option>
        <option v-for="tahun in tahunList" :key="tahun" :value="tahun">{{ tahun }}</option>
      </select>

      <select v-model="selectedProvinsi" @change="fetchData" class="dropdown">
        <option value="">Pilih Provinsi</option>
        <option v-for="prov in provinsiList" :key="prov" :value="prov">{{ prov }}</option>
      </select>

      <select v-if="selectedProvinsi" v-model="selectedDaerah" @change="fetchData" class="dropdown">
        <option value="">Pilih Daerah</option>
        <option v-for="daerah in daerahList" :key="daerah" :value="daerah">{{ daerah }}</option>
      </select>

      <!-- Reset Button -->
      <button 
        class="btn-reset"
        @click="resetFilters"
        :disabled="!hasActiveFilters">
        <i class="fas fa-undo"></i> Reset Filter
      </button>
    </div>
    <!-- Warning Text -->
    <p v-if="!selectedDaerah" class="warning-text">
      ⚠️ Silakan pilih provinsi dan daerah terlebih dahulu untuk menampilkan data grafik dan tabel.
    </p>
    <!-- Chart -->
    <section>
      <h3 style="text-align:center; margin-top: 40px;">Grafik Data PDRD</h3>
      <div class="chart-container">
        <canvas id="barChartPotensi"></canvas>
      </div>
    </section>

    <!-- TABEL -->
    <section v-if="selectedProvinsi && selectedDaerah">
      <h3 style="text-align:center; margin-top: 40px;">Tabel Data DRD</h3>
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Rincian</th>
              <th>Anggaran</th>
              <th>Realisasi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="tableFiltered.length === 0">
              <td colspan="3" class="text-center">Tidak ada data.</td>
            </tr>
            <tr v-for="(item, index) in paginatedTableData" :key="index">
              <td>{{ item.rincian }}</td>
              <td>{{ formatCurrency(item.anggaran) }}</td>
              <td>{{ formatCurrency(item.realisasi) }}</td>
            </tr>
          </tbody>
        </table>
        <div class="pagination-container">
          <button class="pagination-button" :disabled="currentPage === 1" @click="currentPage--">← Prev</button>
          <span class="pagination-text">Halaman {{ currentPage }} dari {{ totalPages }}</span>
          <button class="pagination-button" :disabled="currentPage === totalPages" @click="currentPage++">Next →</button>
        </div>
      </div>
    </section>
    <Footer />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import Chart from 'chart.js/auto'
import dataPotensiAPI from '@/api/dataPotensi'

export default {
  name: 'DataPotensi',
  components: {
    Navbar,
    Footer
  },
  data() {
    return {
      provinsiList: [],
      daerahList: [],
      tahunList: [],
      selectedProvinsi: '',
      selectedDaerah: '',
      selectedTahun: '',
      chartLabels: [],
      chartAnggaran: [],
      chartRealisasi: [],
      totalAnggaran: 0,
      totalRealisasi: 0,
      chartInstance: null,
      tableBasedonTahun: [],
      tableBasedonRincian: [],
      currentPage: 1,
      perPage: 10,
    }
  },
  computed: {
    hasActiveFilters() {
      return this.selectedProvinsi !== '' || this.selectedDaerah !== '' || this.selectedTahun !== ''
    },
    tableFiltered() {
      return this.tableBasedonTahun
    },
    paginatedTableData() {
      const start = (this.currentPage - 1) * this.perPage
      const end = start + this.perPage
      return this.tableBasedonTahun.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.tableBasedonTahun.length / this.perPage)
    }
  },
  methods: {
    async fetchData() {
      try {
        const res = await dataPotensiAPI.getMetadata({
          provinsi: this.selectedProvinsi,
          daerah: this.selectedDaerah,
          tahun: this.selectedTahun
        })

        this.provinsiList = res.data.provinsi_list
        this.daerahList = res.data.daerah_list
        this.tahunList = res.data.tahun_list
        this.totalAnggaran = res.data.total_anggaran
        this.totalRealisasi = res.data.total_realisasi
        this.chartLabels = res.data.chart_labels
        this.chartAnggaran = res.data.chart_anggaran
        this.chartRealisasi = res.data.chart_realisasi
        this.tableBasedonTahun = res.data.table_data_rinci

        if (this.selectedProvinsi && this.selectedDaerah) {
          this.renderChart()
        } else {
          this.chartInstance?.destroy()
          this.chartInstance = null
        }
      } catch (error) {
        console.error('Gagal mengambil data potensi:', error)
      }
    },
    async resetFilters() {
      this.selectedProvinsi = ''
      this.selectedDaerah = ''
      this.selectedTahun = ''
      this.tableBasedonRincian = []
      await this.fetchData()
    },
    async handleChartClick(event) {
      const points = this.chartInstance.getElementsAtEventForMode(event, 'nearest', { intersect: true }, true)
      if (points.length === 0) return

      const firstPoint = points[0]
      const jenis = this.chartInstance.data.labels[firstPoint.index]
      const kategori_apbd = this.chartInstance.data.datasets[firstPoint.datasetIndex].label

      // Ambil hanya filter yang tersedia
      const params = {
        jenis,
        kategori_apbd
      }

      if (this.selectedProvinsi) params.provinsi = this.selectedProvinsi
      if (this.selectedDaerah) params.daerah = this.selectedDaerah
      if (this.selectedTahun) params.tahun = this.selectedTahun

      try {
        const res = await dataPotensiAPI.getRincianByJenis(params)
        this.tableBasedonRincian = res.data
      } catch (err) {
        console.error('Gagal mengambil rincian:', err)
      }
    },

renderChart() {
  if (this.chartInstance) {
    this.chartInstance.destroy()
  }

  this.$nextTick(() => {
    const ctx = document.getElementById('barChartPotensi')
    if (!ctx) return  // Amanin jika masih null

    this.chartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: this.chartLabels,
        datasets: [
          {
            label: 'Anggaran',
            data: this.chartAnggaran,
            backgroundColor: '#3b82f6',
            borderRadius: 8
          },
          {
            label: 'Realisasi',
            data: this.chartRealisasi,
            backgroundColor: 'Orange',
            borderRadius: 8
          },
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            labels: {
              color: '#1e293b',
              font: {
                size: 14,
                weight: '600'
              }
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const value = context.raw
                return `${context.dataset.label}: ${this.formatCurrency(value)}`
              }
            }
          }
        },
        scales: {
          x: {
            ticks: {
              color: '#1e293b',
              font: {
                weight: '500'
              }
            },
            grid: {
              display: false
            }
          },
          y: {
            beginAtZero: true,
            ticks: {
              color: '#1e293b',
              callback: (value) => this.formatCurrency(value),
              font: {
                weight: '500'
              }
            },
            grid: {
              color: '#e2e8f0'
            }
          }
        },
        onClick: this.handleChartClick.bind(this)
      }
    })
  })
},

    formatCurrency(value) {
      return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
      }).format(value || 0)
    }
  },
  mounted() {
    this.fetchData()
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

* {
  font-family: 'Inter', sans-serif;
  box-sizing: border-box;
}

.p-6 {
  background: linear-gradient(to bottom, #f8fafc, #e2e8f0);
  min-height: 100vh;
  padding-top: 8rem;
}

h1.text-center {
  text-align: center;
}

/* Dropdown Style */
.flex-wrap {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5rem;
  padding-top: 2rem
}

.dropdown {
  background-color: white;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  transition: all 0.3s ease-in-out;
}
.dropdown:hover {
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

/* Card Style */
.card {
  background-color: white;
  border-radius: 1rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  text-align: center;
  padding: 1.5rem;
  width: 420px;
  min-height: 140px;
  transition: transform 0.2s ease-in-out;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.card:hover {
  transform: translateY(-4px);
}
.border-left-blue {
  border-left: 6px solid #3b82f6;
}
.border-left-indigo {
  border-left: 6px solid #6366f1;
}
.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.card-value {
  font-size: 1.2rem;
  font-weight: 700;
  word-break: break-word;
}

/* Reset Button Styles */
.btn-reset {
  background-color: #005eff;
  color: #ffffff;
  padding: 0.6rem 1rem;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 0.9rem;
  gap: 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center; 
  height: 38px;
  transition: all 0.3s;
  white-space: nowrap;
}

.btn-reset:hover {
  background-color: #0044b9;
}

.btn-reset:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.warning-text {
  text-align: center;
  color: #b91c1c;
  font-weight: 600;
  margin-top: 1rem;
  font-size: 0.95rem;
}


/* Chart Style */
.chart-container {
  background-color: white;
  border-radius: 1.5rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
  padding: 3rem;
  max-width: 1000px;
  margin: 3rem auto;
  margin-top: 2rem;
}
canvas {
  width: 100% !important;
  height: 430px !important;
}

/* Table Style */
.table-container {
  margin: 0 auto 5rem;
  margin-top: 2rem;
  max-width: 1000px;
  overflow-x: auto;
  background-color: white;
  padding: 1rem 2rem;
  border-radius: 1.5rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.data-table th,
.data-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.data-table th {
  background-color: #f1f5f9;
  font-weight: 600;
  color: #1e293b;
}

.data-table td {
  color: #334155;
}

/* Pagination Style */
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  font-size: 0.95rem;
}

.pagination-button {
  background-color: #3b82f6;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.pagination-button:hover {
  background-color: #2563eb;
}

.pagination-button:disabled {
  background-color: #cbd5e1;
  cursor: not-allowed;
}

.pagination-text {
  font-weight: 500;
  color: #334155;
}

@media (max-width: 1024px) {
  .card {
    width: 50%;
    min-width: unset;
  }

  .chart-container {
    padding: 2rem;
    margin: 2rem 1rem 6rem;
  }

  canvas {
    height: 360px !important;
  }
}

@media (max-width: 768px) {
  .flex-wrap {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    padding-top: 2rem;
  }

  .dropdown {
    width: 100%;
    max-width: 360px;
  }

  .card {
    width: 100%;
    max-width: 360px;
    padding: 1.2rem;
  }

  .card-title {
    font-size: 1rem;
  }

  .card-value {
    font-size: 1.1rem;
  }

  .chart-container {
    padding: 1.5rem;
    margin: 2rem 1rem 4rem;
  }

  canvas {
    width: 95% !important;
    height: 200px !important;
  }
}

@media (max-width: 450px) {
  h1.text-center {
  text-align: center;
  font-size: 1.5rem;
}
  .flex-wrap {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    padding-top: 2rem;
  }

  .dropdown {
    width: 150%;
    max-width: 360px;
  }

  .card {
    width: 100%;
    min-height: 90px;
    padding: 1.2rem;
  }

  .card-title {
    font-size: 1rem;
  }

  .card-value {
    font-size: 1.1rem;
  }

  .chart-container {
    padding: 1.5rem;
    margin: 2rem 1rem 4rem;
  }

  canvas {
    width: 95% !important;
    height: 200px !important;
  }
}

</style>