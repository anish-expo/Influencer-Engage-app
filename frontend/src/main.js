//Frontend/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import store from './store';
import router from './router';




// import axios from 'axios';

// // Add axios interceptor globally
// axios.interceptors.request.use(
//   config => {
//     const token = localStorage.getItem('access_token');
//     if (token) {
//       config.headers['Authorization'] = `Bearer ${token}`;
//     }
//     return config;
//   },
//   error => {
//     return Promise.reject(error);
//   }
// );


createApp(App).use(store).use(router).mount('#app');
