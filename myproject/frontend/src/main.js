// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store' 

import '@fortawesome/fontawesome-free/css/all.css'
import './assets/css/main.css'
import axios from 'axios'
axios.defaults.baseURL = process.env.VUE_APP_API_URL

createApp(App)
  .use(router)
  .use(store) 
  .mount('#app')
