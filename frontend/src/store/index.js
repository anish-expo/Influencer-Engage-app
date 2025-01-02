import { createStore } from 'vuex';
import admin from './modules/admin';

const store = createStore({
  modules: {
    admin
  }
});

export default store;