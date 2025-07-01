<template>
  <div>
    <header>
      <a href="/"><img class="logo-djpk" src="@/assets/images/Logo_DJPK_New.png" alt="Logo PDRD" /></a>
      <a href="/"><img class="logo-image" src="@/assets/images/logo-pdrd.png" alt="Logo PDRD" /></a>
      <div class="bx bx-menu" id="menu-icon" @click="toggleMenu"></div>
      <div class="inner-main-nav" id="main-nav" :class="{ 'open': isMenuOpen }">
        <ul>
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/produk-hukum">Produk Hukum</router-link></li>
          <li><router-link to="/produk-hukum/create">Tambah Peraturan</router-link></li>
          <li><router-link to="/data-potensi">Data PDRD</router-link></li>
          <li><router-link to="/log-update">Monitoring Perubahan</router-link></li>
        </ul>
      </div>
    </header>
  </div>
</template>

<script>
import { toggleMenu } from '@/assets/javascript/navbar.js';
export default {
  name: 'Navbar',
  methods: {
    toggleMenu() {
      toggleMenu();
    },
  },
};
</script>