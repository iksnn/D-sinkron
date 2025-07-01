<template>
  <div class="home">
    <Navbar />
    <div>
      
    <Hero />
    </div>
    <Footer />
  </div>
</template>

<script>
// @ is an alias to /src
import Navbar from '@/components/Navbar.vue'
import Hero from '@/components/Hero.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'HomeView',
  components: {
    // eslint-disable-next-line vue/no-unused-components
    Navbar,
    Hero,
    Footer
  }
}
</script>
