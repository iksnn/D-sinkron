// frontend/src/store/index.js
import { createStore } from 'vuex'
import produkHukum from './modules/produkHukum'

const store = createStore({
  modules: {
    produkHukum
  }
})

export default store