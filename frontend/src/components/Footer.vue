//Frontend/src/components/Fooder.vue

<template>
    <footer class="footer">
      &copy; {{ currentYear }} InfluencerApp. All rights reserved.
    </footer>
  </template>
  
  <script>
  export default {
    name: 'FooterComponent',
    data() {
      return {
        currentYear: new Date().getFullYear(),
      };
    },
  };
  </script>

<style scoped>
 .footer {
  color: rgb(254, 4, 4);

 }
</style>