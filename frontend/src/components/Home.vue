//Frontend/src/components/Home.vue

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
          <router-link to="/signup" class="nav-link">Register</router-link>
        </div>
      </nav>
      <div class="custombtn col-md-4" >
            <h3>For Influencers</h3>
            <p>Browse campaigns, accept/reject ad requests, and negotiate terms.</p>
            <router-link to="/signup" class="custombtn">Register as Influencer</router-link>
          </div>
      <section class="welcome text-center my-5">
        <h2>Welcome to the Influencer Engagement & Sponsorship Coordination Platform</h2>
        <p>Connecting Sponsors with Influencers for seamless advertising and collaborations.</p>
        <router-link to="/signup" class="btn btn-primary">Get Started</router-link>
      </section>
  
      <section class="roles text-center my-5">
        <h2>Our Users</h2>
        <div class="row">
          <div class="col-md-4">
            <h3>For Sponsors</h3>
            <p>Create campaigns, find influencers, and manage ad requests.</p>
            <router-link to="/signup" class="btn btn-secondary">Register as Sponsor</router-link>
          </div>
          <div class="col-md-4">
            <h3>For Influencers</h3>
            <p>Browse campaigns, accept/reject ad requests, and negotiate terms.</p>
            <router-link to="/signup" class="custombtn">Register as Influencer</router-link>
          </div>
          <div class="col-md-4">
            <h3>For Admin</h3>
            <p>Monitor users, campaigns, and statistics. Flag inappropriate content.</p>
            <router-link to="/admin-login" class="btn btn-secondary">Admin Login</router-link>
          </div>
        </div>
      </section>
  
      <section class="features text-center my-5">
        <h2>Key Features</h2>
        <ul class="list-unstyled">
          <li>Campaign Management</li>
          <li>Ad Request Management</li>
          <li>Search for Influencers and Campaigns</li>
          <li>Daily and Monthly Reports</li>
          <li>Performance and Caching</li>
        </ul>
      </section>
  
      <section class="testimonials text-center my-5">
        <h2>Success Stories</h2>
        <p>Read about successful collaborations and user testimonials.</p>
      </section>
  
     
    </div>
  </template>
  
  <script>

  
  export default {
    name: 'HomePage',
    
  };
  </script>
  
  <style scoped>
  
  .navbar {
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;
  }
  
  .welcome, .roles, .features, .testimonials {
    padding: 20px;
  }
  
  .roles .col-md-4 {
    margin-bottom: 20px;
  }
  
  .btn {
    margin-top: 10px;
  }
  .custombtn{
    color: blue;
    margin-top: 1px;
    margin-right: 1px;
  }
  </style>
  