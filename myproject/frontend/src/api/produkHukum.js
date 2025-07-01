// frontend/src/api/produkHukum.js
import axios from '@/api/axios'

const API_URL = '/api/produk-hukum/'

export default {
  getAll() {
    return axios.get(API_URL)
  },
  get(id) {
    return axios.get(`${API_URL}${id}/`)
  },
  create(data) {
    return axios.post(API_URL, data)
  },
  update(id, data) {
    return axios.put(`${API_URL}${id}/`, data)
  },
  delete(id) {
    return axios.delete(`${API_URL}${id}/`)
  }
}