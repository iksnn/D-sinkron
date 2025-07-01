import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ProdukHukumIndex from '@/views/ProdukHukum/ProdukHukumIndex.vue'
import ProdukHukumShow from '@/views/ProdukHukum/ProdukHukumShow.vue'
import ProdukHukumCreate from '@/views/ProdukHukum/ProdukHukumCreate.vue'
import LogUpdates from '@/views/LogUpdates.vue'
import DataPotensi from '@/views/DataPotensi.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/produk-hukum', name: 'ProdukHukum', component: ProdukHukumIndex },
  { path: '/produk-hukum/create', name: 'ProdukHukumCreate', component: ProdukHukumCreate },
  {
    path: '/produk-hukum/:id',
    name: 'ProdukHukumShow',
    component: ProdukHukumShow,
    props: true
  },
  {
    path: '/log-update',
    name: 'LogUpdates',
    component: LogUpdates
  },
  { path: '/data-potensi', name: 'DataPotensi', component: DataPotensi },
  { path: '/:pathMatch(.*)*', redirect: '/' } // wildcard ke HomeView
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router