//Frontend/src/app.vue

<template>
  <router-view />
  <FooterComponent />
</template>

<script>
import FooterComponent from './components/Footer.vue';

export default {
  name: 'App',
  components: {
    FooterComponent
  }
};

</script>