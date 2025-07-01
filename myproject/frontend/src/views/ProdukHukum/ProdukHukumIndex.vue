<!-- views/ProdukHukum/ProdukHukumIndex -->
<template>
  <div>
    <Navbar />
    <div class="produk-hukum-container">
      <div class="header-section">
        <h1 class="page-title">Produk Hukum</h1>
        <div class="header-actions">
          <div class="search-box">
            <i class="fas fa-search"></i>
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Cari produk hukum..." 
              @input="handleSearch"
            >
          </div>
          <router-link :to="{ name: 'ProdukHukumCreate' }" class="btn btn-add">
            <i class="fas fa-plus"></i> Tambah Baru
          </router-link>
        </div>
      </div>

      <!-- Filter Section -->
      <div class="filter-section">
        <!-- Dropdown Level - Compact Left-aligned Layout -->
        <div class="dropdown-levels">
          <!-- Level 1 - Always Visible -->
          <div class="level-select">
            <label class="level-label">Level 1</label>
            <select 
              v-model="levelModel[0]" 
              class="level-dropdown">
              <option value="">Semua</option>
              <option v-for="o in level1Options" :key="o" :value="o">{{ o }}</option>
            </select>
          </div>

          <!-- Level 2 - Hidden until Level 1 is selected -->
          <div class="level-select" v-if="levelModel[0]">
            <label class="level-label">Level 2</label>
            <select 
              v-model="levelModel[1]" 
              class="level-dropdown">
              <option value="">Semua</option>
              <option v-for="o in level2Options" :key="o" :value="o">{{ o }}</option>
            </select>
          </div>

          <!-- Level 3 - Hidden until Level 2 is selected -->
          <div class="level-select" v-if="levelModel[1]">
            <label class="level-label">Level 3</label>
            <select 
              v-model="levelModel[2]" 
              class="level-dropdown">
              <option value="">Semua</option>
              <option v-for="o in level3Options" :key="o" :value="o">{{ o }}</option>
            </select>
          </div>

          <!-- Level 4 - Hidden until Level 3 is selected -->
          <div class="level-select" v-if="levelModel[2]">
            <label class="level-label">Level 4</label>
            <select 
              v-model="levelModel[3]" 
              class="level-dropdown">
              <option value="">Semua</option>
              <option v-for="o in level4Options" :key="o" :value="o">{{ o }}</option>
            </select>
          </div>
        </div>

        <!-- Reset Button -->
        <button 
          class="btn-reset"
          @click="resetFilters"
          :disabled="!hasActiveFilters">
          <i class="fas fa-undo"></i> Reset Filter
        </button>
      </div>

      <!-- Table Section -->
      <div class="table-responsive">
        <table class="modern-table">
          <thead>
            <tr>
              <th class="aturan-column">Aturan</th>
              <th class="remark-column">Remark</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="(item, index) in filteredSearchResults" 
              :key="index"
            >
              <td 
                class="clickable-row"
                @click="goToDetail(item)"
                style="cursor:pointer"
              >
                {{ item.aturan }}
              </td>
              <td>{{ item.remark }}</td>
            </tr>
            <tr v-if="filteredSearchResults.length === 0">
              <td colspan="2" class="no-data">Tidak ada data yang ditemukan</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { debounce } from 'lodash'

export default {
  components: {
    Navbar,
    Footer
  },
  data() {
    return {
      levelModel: ['', '', '', ''],
      searchQuery: '',
      searchResults: []
    }
  },
  computed: {
    ...mapState('produkHukum', ['produkHukumList']),
    level1Options() {
      return [...new Set(this.produkHukumList.map(p => p.level1).filter(Boolean))]
    },
    level2Options() {
      if (!this.levelModel[0]) return []
      return [...new Set(
        this.produkHukumList
          .filter(p => p.level1 === this.levelModel[0])
          .map(p => p.level2)
          .filter(Boolean)
      )]
    },
    level3Options() {
      if (!this.levelModel[1]) return []
      return [...new Set(
        this.produkHukumList
          .filter(p => p.level1 === this.levelModel[0] && p.level2 === this.levelModel[1])
          .map(p => p.level3)
          .filter(Boolean)
      )]
    },
    level4Options() {
      if (!this.levelModel[2]) return []
      return [...new Set(
        this.produkHukumList
          .filter(p => p.level1 === this.levelModel[0] && p.level2 === this.levelModel[1] && p.level3 === this.levelModel[2])
          .map(p => p.level4)
          .filter(Boolean)
      )]
    },
    filteredProdukHukumList() {
      return this.produkHukumList.filter(p => {
        return (
          (!this.levelModel[0] || p.level1 === this.levelModel[0]) &&
          (!this.levelModel[1] || p.level2 === this.levelModel[1]) &&
          (!this.levelModel[2] || p.level3 === this.levelModel[2]) &&
          (!this.levelModel[3] || p.level4 === this.levelModel[3])
        )
      })
    },
flattenedAturanList() {
  const aturanMap = new Map()

  for (let i = 1; i <= 9; i++) {
    const aturanKey = `aturan${i}`
    const remarkKey = `remark${i}`

    this.filteredProdukHukumList.forEach(p => {
      const aturan = p[aturanKey]
      const remark = p[remarkKey]

      if (aturan) {
        if (!aturanMap.has(aturan)) {
          aturanMap.set(aturan, new Set())
        }
        if (remark) {
          aturanMap.get(aturan).add(remark)
        }
      }
    })
  }

  return Array.from(aturanMap.entries()).map(([aturan, remarkSet]) => {
    return {
      aturan,
      remark: Array.from(remarkSet).join(', ')
    }
  })
},

    hasActiveFilters() {
      return this.levelModel.some(level => level !== '')
    },
    filteredSearchResults() {
      if (!this.searchQuery) return this.flattenedAturanList
      return this.searchResults
    }
  },
  watch: {
    'levelModel[0]'() {
      this.levelModel[1] = ''
      this.levelModel[2] = ''
      this.levelModel[3] = ''
    },
    'levelModel[1]'() {
      this.levelModel[2] = ''
      this.levelModel[3] = ''
    },
    'levelModel[2]'() {
      this.levelModel[3] = ''
    },
    flattenedAturanList() {
      this.handleSearch()
    }
  },
  created() {
    this.fetchAll()
    this.handleSearch = debounce(this.performSearch, 300)
  },
  methods: {
    ...mapActions('produkHukum', ['fetchAll', 'delete']),
    resetFilters() {
      this.levelModel = ['', '', '', '']
      this.searchQuery = ''
    },
goToDetail(item) {
  const id = encodeURIComponent(item.aturan)
  const query = {
    level1: this.levelModel[0],
    level2: this.levelModel[1],
    level3: this.levelModel[2],
    level4: this.levelModel[3],
  }
  this.$router.push({
    name: 'ProdukHukumShow',
    params: { id },
    query
  })
},
    performSearch() {
      if (!this.searchQuery) {
        this.searchResults = this.flattenedAturanList
        return
      }
      
      const query = this.searchQuery.toLowerCase()
      this.searchResults = this.flattenedAturanList.filter(item => {
        return (
          (item.aturan && item.aturan.toLowerCase().includes(query)) ||
          (item.remark && item.remark.toLowerCase().includes(query))
        )
      })
    }
  }
}
</script>

<style scoped>
.produk-hukum-container {
    padding: 120px 2% 3rem; /* Sesuaikan dengan tinggi header */
    max-width: 1200px;
    margin: 0 auto;
}

.header-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1rem;
}

.page-title {
  font-size: 2rem;
  color: #2c3e50;
  margin: 0;
  text-align: center;
  width: 100%;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 1rem;
}

.search-box {
  flex-grow: 1;
  position: relative;
  max-width: 400px;
  
}

.search-box i {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #777;
}

.search-box input {
  width: 100%;
  padding: 0.6rem 1.2rem 0.6rem 2.5rem;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.search-box input:focus {
  outline: none;
  border-color: #005eff;
  box-shadow: 0 0 0 2px rgba(0, 94, 255, 0.2);
}

.btn-add {
  background-color: #005eff;
  color: white;
  padding: 0.6rem 1.2rem;
  border: none;
  gap : 0.5rem;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center; 
  transition: background-color 0.3s;
  white-space: nowrap;
}

.btn-add:hover {
  background-color: #0044b9;
}

/* Filter Section Styles */
.filter-section {
  display: flex;
  align-items: flex-end;
  gap: 1rem;
  margin-bottom: 2rem;
}

.dropdown-levels {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  flex-grow: 1;
}

.level-select {
  width: 180px;
}

.level-label {
  display: block;
  margin-bottom: 0.3rem;
  font-size: 0.85rem;
  font-weight: 500;
  color: #555;
}

.level-dropdown {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #005eff;
  font-size: 0.9rem;
  color: #ffffff;
  transition: border-color 0.3s;
  height: 38px;
}

.level-dropdown:focus {
  border-color: #005eff;
  outline: none;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
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

/* Table Styles */
.table-responsive {
  overflow-x: auto;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  text-align: left;
  border: 1px solid #ddd;
}

.modern-table th,
.modern-table td {
  border-right: 1px solid #eee;
}

.modern-table th:last-child,
.modern-table td:last-child {
  border-right: none;
}

.modern-table th {
  background-color: #005eff;
  color: white;
  text-align: center;
  font-size: 20px;
  padding: 1rem;
  font-weight: 500;
}

.modern-table td {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  color: #333;
}

.modern-table tr:hover {
  background-color: #f5f5f5;
}

.aturan-column {
  width: 50%;
}

.remark-column {
  width: 50%;
}

.no-data {
  text-align: center;
  color: #777;
  padding: 2rem;
}

.clickable-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.clickable-row:hover {
  background-color: #e6f0ff !important;
}

@media (max-width: 768px) {
  .produk-hukum-container {
    padding: 5rem 1rem;
  }
  
  .header-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .header-actions {
    flex-direction: column;
    gap: 1rem;
  }
  
  .search-box {
    max-width: 100%;
    margin-left: auto;
    margin-right: auto;
    display: flex;
    justify-content: center;
  }
  .filter-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .dropdown-levels {
    width: 100%;
  }
  
  .level-select {
    width: 100%;
  }
  
  .btn-reset {
    width: 100%;
    margin-top: 0.5rem;
  }

  .aturan-column {
  width: 50%;
}

.remark-column {
  width: 50%;
}
}
</style>