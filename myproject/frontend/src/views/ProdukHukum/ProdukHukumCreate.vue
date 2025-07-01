<template>
  <div>
    <Navbar />
    <div class="container">
      <!-- Form Token -->
      <div v-if="!isAuthenticated" class="form-token">
        <h2 class="form-title">🔐 Masukkan Token Akses</h2>
      <div class="input-group">
        <input v-model="token" :type="showToken ? 'text': 'password'" placeholder="Token" class="input-token" />
        <i :class="showToken ? 'fa fa-eye-slash' : 'fa fa-eye'" class="toggle-icon" @click=toggleShowToken></i>  
      </div>
        <button class="btn-submit" @click="verifyToken">Verifikasi</button>
      </div>

      <!-- Form Upload -->
      <div v-else>
        <div class="header">
          <h1 class="title">Tambah Produk Hukum</h1>
          <router-link to="/" class="btn-back">
            <i class="fas fa-arrow-left"></i> Kembali
          </router-link>
        </div>

        <form @submit.prevent="submitForm" enctype="multipart/form-data" class="form">
          <input
            type="file"
            id="file"
            ref="fileInput"
            @change="handleFileUpload"
            accept=".xlsx"
            class="hidden"
          />

          <label for="file" class="upload-area">
            <div class="upload-content">
              <svg class="upload-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2" />
              </svg>
              <p class="upload-text"><span class="font-semibold">Klik untuk upload</span> atau drag & drop</p>
              <p class="upload-subtext">Hanya file Excel (.xlsx)</p>
            </div>
          </label>

          <div v-if="file" class="file-preview">
            <span>{{ file.name }}</span>
            <button type="button" class="btn-cancel" @click="removeFile">Hapus</button>
          </div>

          <button type="submit" class="btn-submit">Upload</button>
        </form>
      </div>
    </div>
    <Footer />

    <!-- Global Popup -->
    <transition name="fade">
      <div v-if="showPopup" :class="['popup-dynamic', popupType]">
        {{ popupMessage }}
      </div>
    </transition>
  </div>
</template>

<script>
import axios from '@/api/axios'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'ProdukHukumCreate',
  components: { Navbar, Footer },
  data() {
    return {
      token: '',
      isAuthenticated: false,
      file: null,
      showPopup: false,
      popupMessage: '',
      popupType: '',
      showToken: false
    }
  },
  created() {
    this.checkSession()
    this.startSessionWatcher()
    document.addEventListener('visibilitychange', this.handleTabFocus)
  },
  beforeUnmount() {
    document.removeEventListener('visibilitychange', this.handleTabFocus)
  },
  methods: {
    checkSession() {
      const storedTime = localStorage.getItem('authTime')
      if (storedTime && Date.now() - parseInt(storedTime) < 2 * 60 * 1000) {
        this.isAuthenticated = true
      } else {
        this.isAuthenticated = false
      }
    },
    startSessionWatcher() {
      setInterval(() => {
        const storedTime = localStorage.getItem('authTime')
        if (storedTime && Date.now() - parseInt(storedTime) >= 2 * 60 * 1000) {
          localStorage.removeItem('authTime')
          this.isAuthenticated = false
          this.showPopupMessage('⏰ Sesi Anda telah habis. Silakan masukkan token kembali.', 'warning')
        }
      }, 10000)
    },
    handleTabFocus() {
      if (document.visibilityState === 'visible') {
        this.checkSession()
      }
    },
    showPopupMessage(message, type = 'success') {
      this.popupMessage = message
      this.popupType = type
      this.showPopup = true
      setTimeout(() => {
        this.showPopup = false
        this.popupMessage = ''
        this.popupType = ''
      }, 3000)
    },
    toggleShowToken() {
      this.showToken = !this.showToken
    },
    async verifyToken() {
      try {
        const res = await axios.post('/api/verify-token/', { token: this.token })
        if (res.data.status === 'success') {
          localStorage.setItem('authTime', Date.now().toString())
          this.isAuthenticated = true
          this.token = ''
          this.showPopupMessage('✅ Token valid, akses diizinkan.', 'success')
        } else {
          this.showPopupMessage('❌ Token salah. Coba lagi.', 'error')
        }
      } catch (e) {
        this.showPopupMessage('⚠️ Gagal menghubungi server.', 'error')
      }
    },
    handleFileUpload(event) {
      this.file = event.target.files[0]
    },
    removeFile() {
      this.file = null
      this.$refs.fileInput.value = ''
    },
    async submitForm() {
      if (!this.file) {
        alert('Silakan pilih file terlebih dahulu.')
        return
      }

      const formData = new FormData()
      formData.append('file', this.file)

      try {
        await axios.post('/api/produk-hukum/upload-excel/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        this.file = null
        this.$refs.fileInput.value = ''
        this.showPopupMessage('🎉 File berhasil diunggah!', 'success')
      } catch (err) {
        const msg = err.response?.data?.error || '❌ Gagal mengunggah file.'
        this.showPopupMessage(msg, 'error')
      }
    }
  }
}
</script>
<style scoped>
.container {
  padding: 160px 1.5rem 10rem;
  max-width: 700px;
  margin: 0 auto;
  height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a202c;
}

.btn-back {
  background: #005eff;
  color: #fff;
  padding: 0.6rem 1rem;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 500;
  transition: background 0.3s;
}

.btn-back:hover {
  background: #0044b9;
}

.form {
  background: #fff;
  border-radius: 10px;
  padding: 2rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
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
  top: 40%;
  transform: translateY(-50%);
  cursor: pointer;
  color: #64748b;
  font-size: 1.1rem;
}

.form-token{
  background: #fff;
  border-radius: 10px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  margin: 7rem auto;
  max-width: 340px;
}

.form-title {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 1rem;
}
.input-token {
  width: 100%;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.upload-area {
  border: 2px dashed #ccc;
  border-radius: 10px;
  padding: 2rem;
  background-color: #f9fafb;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.upload-area:hover {
  background-color: #edf2f7;
}

.upload-icon {
  width: 40px;
  height: 40px;
  color: #999;
  margin-bottom: 0.5rem;
}

.upload-text {
  font-size: 0.95rem;
  color: #444;
}

.upload-subtext {
  font-size: 0.8rem;
  color: #777;
}

.file-preview {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f1f5f9;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
}

.btn-cancel {
  background: transparent;
  border: none;
  color: #e3342f;
  font-weight: 600;
  cursor: pointer;
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
  transition: background 0.3s ease;
}

.btn-submit:hover {
  background: #0044b9;
}

/* Dynamic Popup */
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

/* Fade transition */
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

/* Input & Feedback */
.success-msg {
  background-color: #d1fae5;
  color: #065f46;
  padding: 0.6rem 1rem;
  margin-top: 1rem;
  border-radius: 6px;
}
.error-msg {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 0.6rem 1rem;
  margin-top: 1rem;
  border-radius: 6px;
}
.input-token {
  width: 100%;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin-bottom: 0.8rem;
}
</style>
