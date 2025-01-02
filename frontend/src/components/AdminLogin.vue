<!-- src/components/AdminLogin.vue -->
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
    </div>
 
    <div class="login-container">
      <h3 style="color: #007bff;">Admin Login </h3>
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="form.username" />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <div class="password-input">
            <input :type="showPassword ? 'text' : 'password'" id="password" v-model="form.password" />
            <button type="button" @click="togglePasswordVisibility">
              {{ showPassword ? 'Hide' : 'Show' }} Password
            </button>
          </div>
        </div>
        <button type="submit">Login</button>
      </form>
      <span>{{ errorMessage }}</span>
    </div>
  </template>


<script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export default {
  name: 'AdminLogin',
  data() {
      return {
        form: {
          username: '',
          password: ''
        },
        showPassword: false,
        errorMessage: '' 
      };
    },
  methods: {
    async login() {
    axios.post('http://127.0.0.1:5000/admin_login', this.form)
      .then(response => {
        // console.log('Login response:', response); 
        if (response && response.data) {
          // console.log('Response data:', response.data);
          const { access_token, refresh_token, username } = response.data;
          
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
          localStorage.setItem('username', username);
          this.redirectBasedOnRole(access_token);
        } else {
          console.error('Login error: Response data is undefined');
        }
      })
      .catch(error => {
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.message;
          
          
        } else {
          this.errorMessage = 'An error occurred during login. Please try again later.';
          
        }
      });
  },
    redirectBasedOnRole(access_token) {
      // Decode the access token to extract user role
      const decodedToken = jwtDecode(access_token);
      // console.log(decodedToken)
      const userRole = decodedToken.role;

      // Redirect based on user role
      if (userRole === 'Admin') {
        const username = localStorage.getItem('username');
        this.$router.push({ name: 'AdminDashboard', params: { username } });
      } else {
        this.$router.push('/admin-login');
      }
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.login-container h2 {
  text-align: center;
  margin-bottom: 20px;
}

.login-container .form-group {
  margin-bottom: 15px;
}

.login-container .form-control {
  width: 100%;
}

.password-container {
  position: relative;
}

.password-container .form-control {
  padding-right: 40px; /* Space for the toggle button */
}

.password-container .btn {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: #007bff;
}

.password-container .btn i {
  font-size: 18px;
}

.btn-primary {
  width: 100%;
}
</style>