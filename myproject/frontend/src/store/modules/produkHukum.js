// frontend/src/store/modules/produkHukum.js
import ProdukHukumService from '@/api/produkHukum'

const state = {
  produkHukumList: [],
  currentProdukHukum: null
}

const mutations = {
  SET_PRODUK_HUKUM_LIST(state, list) {
    state.produkHukumList = list
  },
  SET_CURRENT_PRODUK_HUKUM(state, produk) {
    state.currentProdukHukum = produk
  }
}

const actions = {
  async fetchAll({ commit }) {
    try {
      const response = await ProdukHukumService.getAll()
      commit('SET_PRODUK_HUKUM_LIST', response.data.results || [])
    } catch (error) {
      console.error('Gagal fetch data produk hukum:', error)
    }
  },
  async fetchOne({ commit }, id) {
    const response = await ProdukHukumService.get(id)
    commit('SET_CURRENT_PRODUK_HUKUM', response.data)
  },
  async create({ dispatch }, data) {
    await ProdukHukumService.create(data)
    dispatch('fetchAll')
  },
  async update({ dispatch }, { id, data }) {
    await ProdukHukumService.update(id, data)
    dispatch('fetchAll')
  },
  async delete({ dispatch }, id) {
    await ProdukHukumService.delete(id)
    dispatch('fetchAll')
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
