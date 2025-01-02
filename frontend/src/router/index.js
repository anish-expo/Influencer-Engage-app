//src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/Home.vue';
import AboutPage from '../components/About.vue';
import AdminLogin from '../components/AdminLogin.vue';
import AdminDashboard from '../components/AdminDashbord.vue';
import SignUp from '../components/Signup.vue';
import LogIn from '../components/OtherLogin.vue';
import InfluencerDashboard from '../components/InfluencerDashbord.vue';
import SponsorDashboard from '../components/SponsorDashbord.vue';




const routes = [
    {
      path: '/',
      name: 'Home',
      component: HomePage
    },
    {
        path: '/about',
        name: 'About',
        component: AboutPage
    },
    {
        path: '/admin-login',
        name: 'AdminLogin',
        component: AdminLogin
    },
    {
      path: '/admin-dashboard/:username',
      name: 'AdminDashboard',
      component: AdminDashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/signup',
      name: 'SignUp' ,
      component: SignUp
    },
    {
      path: '/login',
      name: 'Login' ,
      component: LogIn
    },
    {
      path: '/influencer-dashboard/:username',
      name: 'InfluencerDashboard',
      component: InfluencerDashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/sponsor-dashboard/:username',
      name: 'SponsorDashboard',
      component: SponsorDashboard,
      meta: { requiresAuth: true }
    },
];



const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
  });
  
  router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('access_token') !== null;
  
    if (to.matched.some(record => record.meta.requiresAuth)) {
      // Check if route requires authentication
      if (!isAuthenticated) {
        // Redirect to login page if not authenticated
        next('/admin-login');
      } else {
        next(); // Proceed to the route
      }
    } else {
      next(); // Proceed to the route
    }
  });
  
  export default router;
  

