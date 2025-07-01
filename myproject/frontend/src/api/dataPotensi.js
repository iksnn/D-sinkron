import axios from '@/api/axios'

const API_URL = '/api/data-potensi/'

export default {
  getMetadata(params) {
    return axios.get(`${API_URL}metadata/`, { params })
  },
  getRincianByJenis(params) {
    return axios.get(`${API_URL}rincian_by_jenis/`, { params })
  }
}