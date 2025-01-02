// src/components/About.vue 
<template>
    <div>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <router-link to="/" class="navbar-brand">
          <img src="../assets/logo.png" width="30" height="30" alt="Logo">
          InfluencerApp
        </router-link>
  
        <div class="navbar-nav ml-auto">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/about" class="nav-link">About</router-link>
          <router-link to="/admin-login" class="nav-link">Admin Login</router-link>
          <router-link to="/login" class="nav-link">Login</router-link>
          <router-link to="/register" class="nav-link">Register</router-link>
        </div>
      </nav>
    </div>
    
    <div class="about">
      <h1>About Us</h1>
      <p>Welcome to the Influencer Engagement & Sponsorship Coordination Platform!</p>
      <p>This platform connects Sponsors with Influencers to facilitate seamless advertising collaborations. Our goal is to help sponsors find the perfect influencers to promote their products or services, while giving influencers opportunities to monetize their reach and content.</p>
      <p>Whether you are a sponsor looking to create impactful campaigns or an influencer seeking exciting opportunities, our platform is here to support your journey.</p>
      <h2>Our Mission</h2>
      <p>To bridge the gap between sponsors and influencers, fostering successful collaborations that benefit both parties.</p>
      <h2>Our Vision</h2>
      <p>To become the leading platform for influencer marketing, known for its ease of use, comprehensive features, and exceptional support.</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AboutPage'
  };
  </script>
  
  <style scoped>
  .navbar {
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;
  }
  .about {
    margin-top:10px;
    padding: 20px;
  }
  
  .about h1,
  .about h2 {
    margin-top: 20px;
  }
  
  .about p {
    margin-bottom: 10px;
  }
  </style>
  