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

    <div class="signup-container">
      <h2>Sign Up</h2>
  
      <div>
        <label for="role">Select Role:</label>
        <select v-model="form.role_name" id="role">
          <option disabled value="">Please select one</option>
          <option value="Sponsor">Sponsor</option>
          <option value="Influencer">Influencer</option>
        </select>
      </div>
  
      <!-- Common Fields -->
      <div>
        <label for="image">Image:</label>
        <input type="file" @change="previewImage" id="image" />
        <img v-if="form.imagePreview" :src="form.imagePreview" alt="Image Preview" width="100" />
      </div>
  
      <div>
        <label for="name">Name:</label>
        <input type="text" v-model="form.name" id="name" />
      </div>
  
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="form.email" id="email" @blur="validateEmail" />
        <span v-if="emailError" style="color: red;">Invalid email address</span>
      </div>
  
      <div>
        <label for="username">Username:</label>
        <input type="text" v-model="form.username" id="username" />
      </div>
  
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="form.password1" id="password" @input="validatePasswordLength" />
        <span v-if="passwordError" style="color: red;">Password must be at least 6 characters long</span>
      </div>
  
      <div>
        <label for="passwordConfirm">Confirm Password:</label>
        <input type="password" id="passwordConfirm" v-model="password2" required />
        <span v-if="password2 && form.password1 !== password2" style="color: red;">Passwords do not match</span>
      </div>
  
      <div v-if="form.role_name === 'Sponsor'">
        <div>
          <label for="company">Company:</label>
          <input type="text" v-model="form.company" id="company" />
        </div>
        <div>
          <label for="about">About:</label>
          <textarea v-model="form.about" id="about"></textarea>
        </div>
      </div>
  
      <div v-if="form.role_name === 'Influencer'">
        <div>
          <label for="socialmedia">Social Media:</label>
          <input type="text" v-model="form.socialmedia" id="socialmedia" />
        </div>
        <div>
          <label for="reach">Reach:</label>
          <input type="text" v-model="form.reach" id="reach" />
        </div>
        <div>
          <label for="niche">Niche:</label>
          <input type="text" v-model="form.niche" id="niche" />
        </div>
        <div>
          <label for="about">About:</label>
          <textarea v-model="form.about" id="about"></textarea>
        </div>
      </div>
  
      <!-- Submit Button -->
      <button :disabled="!isFormValid" @click="submitForm">
        Sign Up
      </button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'SignUp',
    data() {
      return {
        form: {
          role_name: '',
          image: null,
          imagePreview: null,
          name: '',
          email: '',
          username: '',
          password1: '',
          company: '',
          socialmedia: '',
          reach: '',
          niche:'',
          about: '',
        },
        password2: '',
        emailError: false,
        passwordError: false,
      };
    },
    computed: {
      isFormValid() {
        const hasRole = this.form.role_name !== '';
        const hasImage = this.form.image !== null;
        const hasName = this.form.name.trim() !== '';
        const hasEmail = this.form.email.trim() !== '';
        const hasUsername = this.form.username.trim() !== '';
        const hasPassword = this.form.password1.length >= 6;
        const hasAbout = this.form.about.trim() !== '';
        const passwordMatch = this.form.password1 === this.password2;
  
        if (this.form.role_name === 'Sponsor') {
          return (
            hasRole &&
            hasImage &&
            hasName &&
            hasEmail &&
            hasUsername &&
            hasPassword &&
            this.form.company.trim() !== '' &&
            hasAbout &&
            !this.emailError &&
            !this.passwordError &&
            passwordMatch
          );
        } else if (this.form.role_name === 'Influencer') {
          return (
            hasRole &&
            hasImage &&
            hasName &&
            hasEmail &&
            hasUsername &&
            hasPassword &&
            this.form.socialmedia.trim() !== '' &&
            this.form.reach.trim() !== '' &&
            this.form.niche.trim() !== '' &&
            hasAbout &&
            !this.emailError &&
            !this.passwordError &&
            passwordMatch
          );
        }
        return false;
      },
    },
    methods: {
      validateEmail() {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        this.emailError = !emailPattern.test(this.form.email);
      },
      validatePasswordLength() {
        this.passwordError = this.form.password1.length < 6;
      },
      previewImage(event) {
        const file = event.target.files[0];
        if (file) {
          this.form.image = file;
          const reader = new FileReader();
          reader.onload = e => {
            this.form.imagePreview = e.target.result;
          };
          reader.readAsDataURL(file);
        }
      },
      async submitForm() {
        if (!this.isFormValid) {
          alert('Please fill out all required fields correctly.');
          return;
        }
        
        const formData = new FormData();
        formData.append('image', this.form.image);
        formData.append('name', this.form.name);
        formData.append('email', this.form.email);
        formData.append('username', this.form.username);
        formData.append('password1', this.form.password1);
        formData.append('password2', this.password2);
        formData.append('role_name', this.form.role_name);
        formData.append('about', this.form.about);
        
        if (this.form.role_name === 'Sponsor') {
          formData.append('company', this.form.company);
          try {
            const response = await axios.post('http://127.0.0.1:5000/sponsor_signup', formData);
            alert(response.data.message);
            this.$router.push({ name: 'Login' });
          } catch (error) {
            alert('Error during sponsor signup: ' + error.response.data.message);
          }
        } else if (this.form.role_name === 'Influencer') {
          formData.append('socialmedia', this.form.socialmedia);
          formData.append('reach', this.form.reach);
          formData.append('niche', this.form.niche);
          try {
            const response = await axios.post('http://127.0.0.1:5000/influencer_signup', formData);
            alert(response.data.message);
            this.$router.push({ name: 'Login' });
          } catch (error) {
            if (error.response) {
                  
                  alert('Error during signup: ' + (error.response.data.message || error.response.data));
                } else if (error.request) {
                  
                  alert('No response from server. Please try again later.');
                } else {
                  
                  alert('Error during signup: ' + error.message);
                }
            
          }
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .signup-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  </style>
  