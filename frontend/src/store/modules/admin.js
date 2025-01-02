import axios from 'axios';
import { refreshAccessToken } from '@/Services/refresh_token';
import router from '@/router';

const state = {
  adminDetails: {},
  sponsors: [],
  influencers: [],
  campaigns: [],
  adRequests: [],
  
 
};

const mutations = {
  SET_ADMIN_DETAILS(state, details) {
    state.adminDetails = details;
  },
  SET_SPONSORS(state, sponsors) {
    state.sponsors = sponsors;
  },
  SET_INFLUENCER(state, influencers) {
    state.influencers = influencers;
  },
  SET_CAMPAIGNS(state, campaigns) {
    state.campaigns = campaigns;
  },
  SET_AD_REQUESTS(state, adRequests) {
    state.adRequests = adRequests;
  }
};

const actions = {
  async fetchAdminDetails({ commit, dispatch }) {
    try {
      const response = await axios.get('http://127.0.0.1:5000/dashboard/admin_details', {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });
      commit('SET_ADMIN_DETAILS', response.data);
    } catch (error) {
      if (error.response && error.response.status === 401) {
        try {
          const refreshToken = localStorage.getItem('refresh_token');
          if (!refreshToken) {
            router.push('/admin-login');
          }
          await refreshAccessToken(refreshToken); 
          
          await dispatch('fetchAdminDetails')
        } catch (refreshError) {
          router.push('/admin-login');
        }
      }
    }
  },
  async fetchSponsors({ commit, dispatch }) {
    try {
      const response = await axios.get('http://127.0.0.1:5000/dashboard/sponsors', {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });
      commit('SET_SPONSORS', response.data);
    } catch (error) {
      if (error.response && error.response.status === 401) {
        try {
          const refreshToken = localStorage.getItem('refresh_token');
          if (!refreshToken) {
            router.push('/admin-login');
          }
          await refreshAccessToken(refreshToken); 
          
          await dispatch('fetchSponsors')
        } catch (refreshError) {
          router.push('/admin-login');
        }
      }
    }
  },
  async fetchInfluencers({ commit, dispatch }) {
    try {
      const response = await axios.get('http://127.0.0.1:5000/dashboard/influencers', {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });
      commit('SET_INFLUENCER', response.data); 
    } catch (error) {
      if (error.response && error.response.status === 401) {
        try {
          const refreshToken = localStorage.getItem('refresh_token');
          if (!refreshToken) {
            router.push('/admin-login');
          }
          await refreshAccessToken(refreshToken); 
          
          await dispatch('fetchInfluencers')
        } catch (refreshError) {
          router.push('/admin-login');
        }
      }
    }
  },
  async fetchCampaigns({ commit, dispatch }) {
    try {
      const response = await axios.get('http://127.0.0.1:5000/dashboard/campaigns', {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });
      commit('SET_CAMPAIGNS', response.data);
    } catch (error) {
      if (error.response && error.response.status === 401) {
        try {
          const refreshToken = localStorage.getItem('refresh_token');
          if (!refreshToken) {
            router.push('/admin-login');
          }
          await refreshAccessToken(refreshToken); 
          
          await dispatch('fetchCampaigns')
        } catch (refreshError) {
          router.push('/admin-login');
        }
      }
    }
  },
  async fetchAdRequests({ commit, dispatch }) {
    try {
      const response = await axios.get('http://127.0.0.1:5000/dashboard/ad_requests', {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });
      commit('SET_AD_REQUESTS', response.data);
    } catch (error) {
      if (error.response && error.response.status === 401) {
        try {
          const refreshToken = localStorage.getItem('refresh_token');
          if (!refreshToken) {
            router.push('/admin-login');
          }
          await refreshAccessToken(refreshToken); 
          
          await dispatch('fetchAdRequests')
        } catch (refreshError) {
          router.push('/admin-login');
        }
      }
    }
  }
};

const getters = {
  adminDetails: state => state.adminDetails,
  sponsors: state => state.sponsors,
  influencers: state => state.influencers,
  campaigns: state => state.campaigns,
  adRequests: state => state.adRequests,
 
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};




// import axios from 'axios';

// const state = {
//   adminDetails: {},
//   sponsors: [],
//   influencers: [],
//   campaigns: [],
//   adRequests: [],
  
//   accessToken: localStorage.getItem('access_token') || '',
//   refreshToken: localStorage.getItem('refresh_token') || ''
// };

// const mutations = {
//   SET_ADMIN_DETAILS(state, details) {
//     state.adminDetails = details;
//   },
//   SET_SPONSORS(state,sponsors){
//     state.sponsors = sponsors;
//   },
//   SET_INFLUENCER(state, influencers) {
//     state.influencers = influencers;
//   },
//   SET_CAMPAIGNS(state, campaigns) {
//     state.campaigns = campaigns;
//   },
//   SET_AD_REQUESTS(state, adRequests) {
//     state.adRequests = adRequests;
//   },
  
//   SET_ACCESS_TOKEN(state, token) {
//     state.accessToken = token;
//     localStorage.setItem('access_token', token);
//   },
//   SET_REFRESH_TOKEN(state, token) {
//     state.refreshToken = token;
//     localStorage.setItem('refresh_token', token);
//   },
//   CLEAR_TOKENS(state) {
//     state.accessToken = '';
//     state.refreshToken = '';
//     localStorage.removeItem('access_token');
//     localStorage.removeItem('refresh_token');
//   }
// };

// const actions = {
//   async fetchAdminDetails({ commit, dispatch }) {
//     try {
//       const response = await axios.get('http://127.0.0.1:5000/dashboard/admin_details', {
//         headers: { Authorization: `Bearer ${state.accessToken}` }
//       });
//       commit('SET_ADMIN_DETAILS', response.data);
//     } catch (error) {
//       if (error.response && error.response.status === 401) {
//         await dispatch('refreshToken');
//         await dispatch('fetchAdminDetails');
//       }
//     }
//   },
//   async fetchSponsors({ commit, dispatch }) {
//     try {
//       const response = await axios.get('http://127.0.0.1:5000/dashboard/sponsors', {
//         headers: { Authorization: `Bearer ${state.accessToken}` }
//       });
//       commit('SET_SPONSORS', response.data);
//     } catch (error) {
//       if (error.response && error.response.status === 401) {
//         await dispatch('refreshToken');
//         await dispatch('fetchSponsors');
//       }
//     }
//   },
//   async fetchInfluencers({ commit, dispatch }) {
//     try {
//       const response = await axios.get('http://127.0.0.1:5000/dashboard/influencers', {
//         headers: { Authorization: `Bearer ${state.accessToken}` }
//       });
//       commit('SET_INFLUENCER', response.data); 
//     } catch (error) {
//       if (error.response && error.response.status === 401) {
//         await dispatch('refreshToken');
//         await dispatch('fetchInfluencers');
//       }
//     }
//   },    
//   async fetchCampaigns({ commit, dispatch }) {
//     try {
//       const response = await axios.get('http://127.0.0.1:5000/dashboard/campaigns', {
//         headers: { Authorization: `Bearer ${state.accessToken}` }
//       });
//       commit('SET_CAMPAIGNS', response.data);
//     } catch (error) {
//       if (error.response && error.response.status === 401) {
//         await dispatch('refreshToken');
//         await dispatch('fetchCampaigns');
//       }
//     }
//   },
//   async fetchAdRequests({ commit, dispatch }) {
//     try {
//       const response = await axios.get('http://127.0.0.1:5000/dashboard/ad_requests', {
//         headers: { Authorization: `Bearer ${state.accessToken}` }
//       });
//       commit('SET_AD_REQUESTS', response.data);
//     } catch (error) {
//       if (error.response && error.response.status === 401) {
//         await dispatch('refreshToken');
//         await dispatch('fetchAdRequests');
//       }
//     }
//   },
//   async refreshToken({ commit }) {
//     try {
//       const response = await axios.post('http://127.0.0.1:5000/refresh-token', 
//         { refresh_token: state.refreshToken },
//         { headers: { Authorization: `Bearer ${state.refreshToken}`} } 
//     );
//       commit('SET_ACCESS_TOKEN', response.data.access_token);
//     } catch (error) {
//       commit('CLEAR_TOKENS');
//       this.$router.push('/admin-login');
//     }
//   }
// };

// const getters = {
//   adminDetails: state => state.adminDetails,
//   sponsors: state => state.sponsors,
//   influencers: state => state.influencers,
//   campaigns: state => state.campaigns,
//   adRequests: state => state.adRequests,
//   newSponsors: state => state.newSponsors,
//   isAuthenticated: state => !!state.accessToken
// };

// export default {
//   namespaced: true,
//   state,
//   mutations,
//   actions,
//   getters
// };
