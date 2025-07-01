<template>
  <div>
    <Navbar />
    <div class="log-container">
      <!-- LOG TABEL -->
      <div>
        <div class="header-section">
          <h1 class="page-title">Log Update</h1>
          <router-link to="/" class="btn btn-back">
            <i class="fas fa-arrow-left"></i> Kembali
          </router-link>
        </div>

        <div class="log-table-section">
          <div v-if="loading" class="text-gray-500 text-center py-6">Memuat log...</div>
          <div v-else-if="logs.length === 0" class="text-gray-500 text-center py-6">Belum ada log update.</div>
          <div v-else class="overflow-x-auto">
            <table class="log-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Waktu</th>
                  <th>Aksi</th>
                  <th>Detail</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(log, index) in logs" :key="log?.id || index">
                  <td>{{ index + 1 }}</td>
                  <td>{{ formatDate(log.waktu) }}</td>
                  <td><span :class="aksiColor(log.aksi)">{{ log.aksi }}</span></td>
                  <td>{{ log.detail_aksi }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script>
import axios from '@/api/axios'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'LogUpdates',
  components: { Navbar, Footer },
  data() {
    return {
      logs: [],
      loading: true,
    }
  },
  created() {
    this.fetchLogs()
  },
  methods: {
    fetchLogs() {
      axios.get('/api/log-updates/')
        .then(res => {
          const data = res.data
          this.logs = Array.isArray(data) ? data : (data.results || [])
        })
        .catch(err => {
          console.error('Gagal memuat log:', err)
        })
        .finally(() => {
          this.loading = false
        })
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleString('id-ID', {
        dateStyle: 'short',
        timeStyle: 'short'
      })
    },
    aksiColor(aksi) {
      if (aksi === 'Tambah') return 'text-green-600 font-semibold'
      if (aksi === 'Hapus') return 'text-red-600 font-semibold'
      if (aksi === 'Update') return 'text-yellow-600 font-semibold'
      return 'text-gray-700'
    }
  }
}
</script>


<style scoped>
/* LAYOUT */
.log-container {
  padding: 120px 0 3rem;
  max-width: 75%;
  margin: 0 auto;
  min-height: calc(100vh);
  display: flex;
  flex-direction: column;
  justify-content: center;
  
}

/* FORM TOKEN */
.form {
  background: #fff;
  border-radius: 10px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  margin: 0 auto;
  max-width: 500px;
}
.form-title {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.input-group {
  position: relative;
  width: 100%;
}

.input-token {
  width: 100%;
  padding: 0.5rem 2.5rem 0.5rem 1rem; /* kanan diperbesar utk tempat icon */
  font-size: 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  outline: none;
}

.toggle-icon {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: #64748b;
  font-size: 1.1rem;
}
.input-token {
  width: 100%;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.btn-submit {
  background: #005eff;
  color: white;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.95rem;
  cursor: pointer;
}
.btn-submit:hover {
  background: #0044b9;
}
.success-msg {
  background-color: #d1fae5;
  color: #065f46;
  padding: 0.6rem 1rem;
  border-radius: 6px;
}
.error-msg {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 0.6rem 1rem;
  border-radius: 6px;
}

/* TABEL LOG */
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}
.page-title {
  font-size: 1.4rem;
  color: #2c3e50;
  font-weight: bold;
}
.btn-back {
  background-color: #005eff;
  color: white;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 500;
  gap: 0.5rem;
  display: flex;
  align-items: center;
  transition: background-color 0.3s;
}
.btn-back:hover {
  background-color: #0044b9;
}
.log-table-section {
  background: white;
  border-radius: 10px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  overflow-x: auto;
}
.log-table {
  width: 100%;
  min-width: 600px;
  border-collapse: collapse;
  font-size: 0.95rem;
}
.log-table th {
  background-color: #005eff;
  color: white;
  padding: 0.75rem;
  text-align: left;
}
.log-table td {
  padding: 0.75rem;
  border-top: 1px solid #e5e7eb;
}
.log-table tr:hover {
  background-color: #f9fafb;
}

/* POPUP */
.popup-dynamic {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 1rem 2rem;
  border-radius: 10px;
  font-weight: bold;
  z-index: 9999;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  animation: popup-scale 0.3s ease;
  text-align: center;
  max-width: 90%;
  word-wrap: break-word;
}

.popup-dynamic.success {
  background: #38a169;
  color: white;
}
.popup-dynamic.error {
  background: #e53e3e;
  color: white;
}
.popup-dynamic.warning {
  background: #dd6b20;
  color: white;
}
@keyframes popup-scale {
  from {
    transform: translateX(-50%) scale(0.8);
    opacity: 0;
  }
  to {
    transform: translateX(-50%) scale(1);
    opacity: 1;
  }
}
.fade-enter-active {
  transition: opacity 0.4s ease;
}
.fade-leave-active {
  transition: opacity 0.8s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .log-container {
    max-width: 90%;
    padding: 100px 0 3rem;
  }
  .form {
    max-width: 100%;
  }
  .page-title {
    font-size: 1.2rem;
  }
  .btn-back {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
  .log-table-section {
    padding: 1rem;
  }
}
</style>