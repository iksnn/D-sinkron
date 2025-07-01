<template>
  <div>
    <Navbar />
    <div class="produk-detail-container">
      <div class="header-section">
        <h1 class="page-title">{{ produkHukum.aturan }}</h1>
        <router-link :to="{ name: 'ProdukHukum' }" class="btn btn-back">
          <i class="fas fa-arrow-left"></i> Kembali
        </router-link>
      </div>

      <div class="detail-content">
        <div class="detail-card">
          <div class="detail-row">
            <span class="detail-label">Jenis/Bentuk Peraturan:</span>
            <span class="detail-value">{{ produkHukum.level2 || '-' }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Nomor:</span>
            <span class="detail-value">{{ produkHukum.nomor || '-' }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Tahun:</span>
            <span class="detail-value">{{ produkHukum.tahun || '-' }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Remark:</span>
            <span class="detail-value">{{ produkHukum.allRemarks || '-' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Status:</span>
            <span class="detail-value">
              <template v-if="produkHukum.status.length">
                <ul class="status-list">
                  <li v-for="(link, index) in produkHukum.status" :key="index">
                    <a :href="link" target="_blank" rel="noopener noreferrer" class="status-link">
                      Status Berdasarkan JDIH BPK
                    </a>
                  </li>
                </ul>
              </template>
              <template v-else>
                <span class="text-muted">Status tidak ditemukan</span>
              </template>
            </span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Dokumen:</span>
            <span class="detail-value">
              <template v-if="produkHukum.links.length">
                <ul class="status-list">
                  <li v-for="(link, index) in produkHukum.links" :key="index">
                    <a :href="link" target="_blank" rel="noopener noreferrer" class="download-button">
                      📄 Download Dokumen {{ index + 1 }}
                    </a>
                  </li>
                </ul>
              </template>
              <template v-else>
                <span class="text-muted">Dokumen tidak ditemukan</span>
              </template>
            </span>
          </div>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'

export default {
  components: {
    Navbar,
    Footer
  },
  data() {
    return {
      produkHukum: {
        aturan: '',
        nomor: '',
        tahun: '',
        level2: '',
        allRemarks: '',
        status: [],
        links: []
      }
    }
  },
  computed: {
    ...mapState('produkHukum', ['produkHukumList'])
  },
  async created() {
    if (!this.produkHukumList.length) {
      await this.fetchAll()
    }
    this.loadProdukHukumDetail()
  },
  watch: {
    produkHukumList(val) {
      if (val.length && !this.produkHukum.aturan) {
        this.loadProdukHukumDetail()
      }
    }
  },
  methods: {
    ...mapActions('produkHukum', ['fetchAll']),
    extractNomorTahun(aturan) {
      if (!aturan) return { nomor: '-', tahun: '-' }
      const tahunMatch = aturan.match(/\b(19|20)\d{2}\b/)
      const tahun = tahunMatch ? tahunMatch[0] : '-'
      let nomor = aturan
        .replace(/\bTahun\s+\d{4}\b/i, '')
        .replace(/\bThn\.?\s+\d{4}\b/i, '')
        .replace(/\b\d{4}\b/, '')
        .replace(/\s*\/\s*\d{4}\b/, '')
        .replace(/^[^\d]*(\d+)\s*\/?.*$/, '$1')
        .replace(/\s+/g, ' ')
        .replace(/\bNo\.[\s]*/i, '')
        .replace(/\bNomor[\s]*/i, '')
        .replace(/\bNmr[\s]*/i, '')
        .replace(/[/,.]\s*$/, '')
        .trim()
      if (!nomor) {
        nomor = aturan.split(/\s+/).slice(0, 3).join(' ') || '-'
      }
      return { nomor, tahun }
    },
    loadProdukHukumDetail() {
      const id = decodeURIComponent(this.$route.params.id)
      const { level1, level2, level3, level4 } = this.$route.query

      const matchingItems = this.produkHukumList.filter(item => {
        const matchesAturan = Array.from({ length: 9 }, (_, i) => item[`aturan${i + 1}`] === id).some(Boolean)
        const matchesLevel =
          (!level1 || item.level1 === level1) &&
          (!level2 || item.level2 === level2) &&
          (!level3 || item.level3 === level3) &&
          (!level4 || item.level4 === level4)
        return matchesAturan && matchesLevel
      })

      if (matchingItems.length === 0) {
        this.$router.push({ name: 'ProdukHukum' })
        return
      }

      const firstMatch = matchingItems[0]
      const { nomor, tahun } = this.extractNomorTahun(id)

      const remarksSet = new Set()
      const statusSet = new Set()
      const linkSet = new Set()

      matchingItems.forEach(item => {
        for (let i = 1; i <= 9; i++) {
          if (item[`aturan${i}`] === id) {
            if (item[`remark${i}`]) remarksSet.add(item[`remark${i}`])
            if (item[`status${i}`]) statusSet.add(item[`status${i}`])
            if (item[`link${i}`]) linkSet.add(item[`link${i}`])
          }
        }
      })

      this.produkHukum = {
        aturan: id,
        nomor,
        tahun,
        level2: firstMatch.level2 || '',
        allRemarks: Array.from(remarksSet).join(', '),
        status: Array.from(statusSet),
        links: Array.from(linkSet)
      }
    }
  }
}
</script>

<style scoped>
.produk-detail-container {
  padding: 120px 2% 3rem;
  max-width: 1120px;
  margin: 0 auto;
}
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}
.page-title {
  font-size: 1.3rem;
  color: #2c3e50;
  margin: 0;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-align: left;
}
.btn-back {
  background-color: #005eff;
  color: white;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 500;
  display: flex;
  align-items: center;
  transition: background-color 0.3s;
}
.btn-back:hover {
  background-color: #0044b9;
}
.detail-content {
  background: white;
  border-radius: 12px;
  padding: 2rem 1.5rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15);
}
.detail-card {
  width: 100%;
  border-collapse: collapse;
}
.detail-row {
  display: flex;
  align-items: flex-start;
  border-radius: 12px;
  border-bottom: 1px solid #e5e7eb;
  padding: 1rem 2rem;
  background: #f9fafe;
}
.detail-row:nth-child(even) {
  background: #f3f6fb;
}
.detail-label {
  font-weight: 600;
  min-width: 220px;
  color: #2d3748;
  text-align: left;
  padding-right: 1.5rem;
  flex-shrink: 0;
}
.detail-value {
  flex: 1;
  color: #222;
  text-align: left;
  word-break: break-word;
}
.status-list {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
}
.status-link {
  color: #005eff;
  text-decoration: none;
  cursor: pointer;
  font-weight: 500;
}
.status-link:hover {
  text-decoration: underline;
  color: #003e99;
}
.download-button {
  display: inline-block;
  padding: 0.45rem 1rem;
  background-color: #005eff;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  transition: background-color 0.3s ease;
  font-weight: 500;
  margin-bottom: 0.3rem;
}
.download-button:hover {
  background-color: #003e99;
}
.text-muted {
  color: #888;
  font-style: italic;
}
@media (max-width: 768px) {
  .produk-detail-container {
    padding: 90px 3.5% 2rem;
  }
  .header-section {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  .detail-content {
    padding: 1.2rem 1rem;
  }
  .detail-row {
    flex-direction: column;
    gap: 0.5rem;
    padding: 0.8rem 0;
  }
  .detail-label {
    min-width: auto;
    padding-right: 0;
  }
}
</style>
