<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <a @click.prevent="reloadPage" class="navbar-brand">
        <img src="../assets/logo.png" width="30" height="30" alt="Logo">
        InfluencerApp
      </a>
      <div class="navbar-nav ml-auto">
        <button @click="setActiveSection('about')" class="btn btn-primary nav-link mx-1">About Me</button>
        <button @click="fetchNewSponsors(); setActiveSection('newSponsor')" class="btn btn-primary nav-link mx-1">New Sponsor</button>
        <button @click="fetchSponsors(); setActiveSection('sponsors')" class="btn btn-primary nav-link mx-1">Sponsors</button>
        <button @click="fetchInfluencers(); setActiveSection('influencers')" class="btn btn-primary nav-link mx-1">Influencers</button>
        <button @click="fetchCampaigns(); setActiveSection('campaigns')" class="btn btn-primary nav-link mx-1">Campaigns</button>
        <button @click="logout" class="btn btn-danger nav-link mx-1">Admin Logout</button>
      </div>
    </nav>

    <div class="content-container">
      
      <h2>Welcome,Admin  {{ adminDetails.name }}, </h2>
      
      <div v-if="activeSection === 'about'">
        <img class="image" :src="getImageUrl(adminDetails.image)"/>
        <p>Email: {{ adminDetails.email }}</p>
        <p>Role: {{ adminDetails.role }}</p>
        <p>Date Created: {{ adminDetails.date_created }}</p>
        <p>Last Login: {{ adminDetails.last_login }}</p>
      </div>

      
      <!-- New Sponsor Section -->
<div v-if="activeSection === 'newSponsor'">
  <h3>New Sponsors</h3>

  <!-- Display message if there are no new sponsors -->
  <div v-if="newSponsor.length === 0">
    <p>No new sponsors available at the moment.</p>
  </div>

  
  <table v-else class="table table-striped">
    <thead>
      <tr>
        <th>Name</th>
        <th>Email</th>
        <th>Date Created</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="sponsor in newSponsor" :key="sponsor.id ">
      <td>{{ sponsor.name }}</td> <!-- Use optional chaining to avoid undefined errors -->
      <td>{{ sponsor.email }}</td>
      <td>{{ sponsor.date_created ? new Date(sponsor.date_created).toLocaleDateString() : '' }}</td>
      <td>
        <button @click="approveSponsor(sponsor.id)" class="btn btn-success mx-1" v-if="sponsor">Approve</button>
        <button @click="rejectSponsor(sponsor.id)" class="btn btn-danger mx-1" v-if="sponsor">Reject</button>
        <button @click="toggleDetails(sponsor.id)" class="btn btn-info mx-1" v-if="sponsor">
          {{ showDetailsFor === sponsor.id ? 'Hide Details' : 'Show Details' }}
        </button>
      </td>
    </tr>
    </tbody> 
  </table>
</div>

<!-- Modal for Sponsor Details -->
<div v-if="showDetailsFor" class="modal" tabindex="-1" role="dialog" style="display: block;">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Sponsor Details</h5>
          <button type="button" class="close" @click="showDetailsFor = null" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <p><strong>Username:</strong> {{ selectedSponsor.username || 'N/A' }}</p>
          <p><strong>Email:</strong> {{ selectedSponsor.email || 'N/A' }}</p>
          <p><strong>Company:</strong> {{ selectedSponsor.company || 'N/A' }}</p>
          <p><strong>About:</strong> {{ selectedSponsor.about || 'N/A' }}</p>
          <p><strong>Date Created:</strong> {{ selectedSponsor.date_created ? new Date(selectedSponsor.date_created).toLocaleDateString() : 'N/A' }}</p>
          <p><strong>Last Login:</strong> {{ selectedSponsor.last_login ? new Date(selectedSponsor.last_login).toLocaleDateString() : 'N/A' }}</p>
          <img v-if="selectedSponsor.image" :src="getImageUrl(selectedSponsor.image)"  alt="Sponsor Image" class="img-fluid sponsor-image" />
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="showDetailsFor = null">Close</button>
        </div>
      </div>
    </div>
  </div>




      <div v-if="activeSection === 'sponsors'">
       <!-- <div><pre>{{ sponsors }}</pre> </div> -->
        <h3>Sponsors</h3>
                <div v-if="sponsors.length === 0">
                  <p>No sponsors available at the moment.</p>
                </div>
                <table v-else class="table table-striped">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Date Created</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="sponsor in sponsors" :key="sponsor.id ">
                    <td>{{ sponsor.name }}</td> 
                    <td>{{ sponsor.email }}</td>
                    <td>{{ sponsor.date_created ? new Date(sponsor.date_created).toLocaleDateString() : '' }}</td>
                    <td>
                      <button @click="toggleSponsorDetails(sponsor.id)" class="btn btn-info mx-1" v-if="sponsor">
                        {{ showDetailsForSponsor === sponsor.id ? 'Hide Details' : 'Show Details' }}
                      </button>

                      <button @click="toggleFlag(sponsor.id)" class="btn mx-1" :class="{ 'btn-success': !sponsor.is_flagged, 'btn-danger': sponsor.is_flagged }"
                                          v-if="sponsor"> {{ sponsor.is_flagged ? 'Flagged' : 'Flag' }} </button>
                      
                    </td>
                  </tr>
                  </tbody> 
                </table> 
      </div>
      <!-- Sponsor Details Section -->
          <div v-for="sponsor in sponsors" :key="sponsor.id">
            <div v-if="showDetailsForSponsor === sponsor.id" class="sponsor-details">
              <div class="sponsor-info">
                <img v-if="sponsor.image" :src="getImageUrl(sponsor.image)" alt="Sponsor Image" class="img-fluid sponsor-image" />
                <h4>{{ sponsor.name }}</h4>
                <p>Email: {{ sponsor.email }}</p>
                <p>Company: {{ sponsor.company }}</p>
                <p>About: {{ sponsor.about }}</p>
                <p>Created: {{ sponsor.date_created ? new Date(sponsor.date_created).toLocaleDateString() : '' }}</p>
                <p>Last Login: {{ sponsor.last_login ? new Date(sponsor.last_login).toLocaleDateString() : '' }}</p>
              </div>
              <div class="campaigns-info">
                <h5>Campaigns</h5>
                <div class="campaigns-list">
                  <div v-for="campaign in sponsor.campaigns" :key="campaign.id" class="campaign-card">
                    <h6>{{ campaign.name }}</h6>
                    <p><strong>Description:</strong> {{ campaign.description }}</p>
                    <p><strong>Budget:</strong> {{ campaign.budget }}</p>
                    <p><strong>Visibility:</strong> {{ campaign.visibility }}</p>
                    <p><strong>Goals:</strong> {{ campaign.goals }}</p>
                    <p><strong>Target:</strong> {{ campaign.target }}</p>
                    <p><strong>Start Date:</strong> {{ new Date(campaign.start_date).toLocaleDateString() }}</p>
                    <p><strong>End Date:</strong> {{ new Date(campaign.end_date).toLocaleDateString() }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

      <div v-if="activeSection === 'influencers'">
        <!-- <div><pre>{{ influencers }}</pre> </div> -->
        <h3>Influencers</h3>
        <div v-if="influencers.length === 0">
                  <p>No influencers available at the moment.</p>
                </div>
                <table v-else class="table table-striped">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Date Created</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                        <tbody>
                          <tr v-for="influencer in influencers" :key="influencer.id ">
                          <td>{{ influencer.name }}</td> 
                          <td>{{ influencer.email }}</td>
                          <td>{{ influencer.date_created ? new Date(influencer.date_created).toLocaleDateString() : '' }}</td>
                          <td>
                            <button @click="toggleInfluencerDetails(influencer.id)" class="btn btn-info mx-1" v-if="influencer">
                              {{ showDetailsForInfluencer === influencer.id ? 'Hide Details' : 'Show Details' }}
                            </button>

                            <button @click="toggleFlag2(influencer.id)" class="btn mx-1" :class="{ 'btn-success': !influencer.is_flagged, 'btn-danger': influencer.is_flagged }"
                                                v-if="influencer"> {{ influencer.is_flagged ? 'Flagged' : 'Flag' }} </button>
                            
                          </td>
                        </tr>
                        </tbody> 
                      </table> 
      </div>
      <!-- Influencer Details Section -->
      <div v-for="influencer in influencers" :key="influencer.id">
            <div v-if="showDetailsForInfluencer === influencer.id" class="sponsor-details">
              <div class="sponsor-info">
                <img v-if="influencer.image" :src="getImageUrl(influencer.image)" alt="Sponsor Image" class="img-fluid sponsor-image" />
                <h4>{{ influencer.name }}</h4>
                <p>Email: {{ influencer.email }}</p>
                <p>SocialMedia: {{ influencer.socialmedia }}</p>
                <p>Niche: {{ influencer.niche }}</p>
                <p>Reach: {{ influencer.reach }}</p>
                <p>About: {{ influencer.about }}</p>
                <p>Created: {{ influencer.date_created ? new Date(influencer.date_created).toLocaleDateString() : '' }}</p>
                <p>Last Login: {{ influencer.last_login ? new Date(influencer.last_login).toLocaleDateString() : '' }}</p>
              </div>
              
            </div>
          </div>




      <div v-if="activeSection === 'campaigns'">
        <!-- {{ campaigns }} -->
        <h3 class="mb-3">Campaigns</h3>
       <div class="campaigns-info">
                
                <div class="campaigns-list">
                  <div v-for="campaign in campaigns" :key="campaign.id" class="campaign-card">
                    <div class="sponsor-info">
                      <button @click="toggleFlag3(campaign.id)" class="btn mx-1" :class="{ 'btn-success': !campaign.flag, 'btn-danger': campaign.flag }"
                      v-if="campaign"> {{ campaign.flag ? 'Flagged' : 'Flag' }} </button>
                    </div>
                    <h6><strong>Name::</strong> {{ campaign.name }}</h6>
                    <p><strong>Description:</strong> {{ campaign.description }}</p>
                    <p><strong>Budget:</strong> {{ campaign.budget }}</p>
                    <p><strong>Visibility:</strong> {{ campaign.visibility }}</p>
                    <p><strong>Goals:</strong> {{ campaign.goals }}</p>
                    <p><strong>Target:</strong> {{ campaign.target }}</p>
                    <p><strong>Completion Percentage:</strong> {{ campaign.completion_percentage }} %</p>
                    <p><strong>Start Date:</strong> {{ new Date(campaign.start_date).toLocaleDateString() }}</p>
                    <p><strong>End Date:</strong> {{ new Date(campaign.end_date).toLocaleDateString() }}</p>
                    <img class="image" :src="getImageUrl(campaign.image)" alt="Sponsor Image"/>
                  </div>
                </div>
              </div>
      </div>

      <div class="content-container">
        <table  class="table table-striped">
                  <thead>
                    <tr>
                      <th>Name</th>
                      
                      <th>Total</th>
                    </tr>
                  </thead>
                        <tbody>
                          <tr> Influencer
                          <td>{{ influencers.length }}</td> 
                        </tr>
                        <tr> Sponsor
                          <td>{{ sponsors.length }}</td> 
                        </tr>
                        <tr> Campaigns
                          <td>{{ campaigns.length }}</td> 
                        </tr>
                        <tr> AddRequests
                          <td>{{ adRequests.length }}</td> 
                        </tr>
                        
                        </tbody> 
                      </table> 
      </div>

      
    </div>
  </div>
  

</template>

<script>
import axios from 'axios';
import { mapState, mapActions } from 'vuex';
import { refreshAccessToken } from '@/Services/refresh_token';

export default{
    name: 'AdminDashboard',
    data() {
    return {
      
      showDetailsFor: null,
      showDetailsForSponsor: null,
      showDetailsForInfluencer: null,
      activeSection: '' ,
      newSponsor: [],
    };
  },

    computed: {
    ...mapState('admin', ['adminDetails', 'sponsors','influencers', 'campaigns', 'adRequests']),
    selectedSponsor() {
          return this.newSponsor.find(sponsor => sponsor.id === this.showDetailsFor) || {};
        }
    
   
  },
  methods: {
    ...mapActions('admin', ['fetchAdminDetails', 'fetchSponsors','fetchInfluencers' ,'fetchCampaigns', 'fetchAdRequests']),
    
    setActiveSection(section) {
      this.activeSection = section;
      if (section === 'newSponsor') {
            this.fetchNewSponsors();
          }
    },
            
           toggleInfluencerDetails(influencerId) {
            if (this.showDetailsForInfluencer === influencerId) {
              this.showDetailsForInfluencer = null; 
            } else {
              this.showDetailsForInfluencer = influencerId; 
            }
          },
          
           toggleSponsorDetails(sponsorId) {
            if (this.showDetailsForSponsor === sponsorId) {
              this.showDetailsForSponsor = null; 
            } else {
              this.showDetailsForSponsor = sponsorId; 
            }
          },
          async toggleFlag3(campaignid) {
            try {
              
              const response = await axios.post(`http://127.0.0.1:5000/dashboard/campaigns/${campaignid}/toggle-flag`,{}, {
                  headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                  },
                    });

              const campaign = this.campaigns.find(s => s.id === campaignid);
              if (campaign) {
                campaign.flag = response.data.flag; 
                
              }
            } catch (error) {
                    if (error.response && error.response.status === 401) {
                      try {
                        const refreshToken = localStorage.getItem('refresh_token');
                        if (!refreshToken) {
                          this.$router.push('/admin-login');
                        }
                        await refreshAccessToken(refreshToken); 
                        
                        await this.toggleFlag3(campaignid);
                      } catch (refreshError) {
                        this.$router.push('/admin-login');
                      }
                    }
                  }
          },
          async toggleFlag(sponsorId) {
            try {
              // const accessToken = localStorage.getItem('access_token');
              // console.log("Access Token:", accessToken);
              const response = await axios.post(`http://127.0.0.1:5000/dashboard/users/${sponsorId}/toggle-flag`, {},{
                  headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                  },
                    });

              const sponsor = this.sponsors.find(s => s.id === sponsorId);
              if (sponsor) {
                sponsor.is_flagged = response.data.is_flagged; 
              }
            } catch (error) {
                    if (error.response && error.response.status === 401) {
                      try {
                        const refreshToken = localStorage.getItem('refresh_token');
                        if (!refreshToken) {
                          this.$router.push('/admin-login');
                        }
                        await refreshAccessToken(refreshToken); 
                        
                        await this.toggleFlag(sponsorId);
                      } catch (refreshError) {
                        this.$router.push('/admin-login');
                      }
                    }
                  }
          },
          async toggleFlag2(influencerId) {
            try {
              
              const response = await axios.post(`http://127.0.0.1:5000/dashboard/users/${influencerId}/toggle-flag`,{}, {
                  headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                  },
                    });

              const influencer = this.influencers.find(s => s.id === influencerId);
              if (influencer) {
                influencer.is_flagged = response.data.is_flagged; 
              }
            } catch (error) {
                    if (error.response && error.response.status === 401) {
                      try {
                        const refreshToken = localStorage.getItem('refresh_token');
                        if (!refreshToken) {
                          this.$router.push('/admin-login');
                        }
                        await refreshAccessToken(refreshToken); 
                        
                        await this.toggleFlag2(influencerId);
                      } catch (refreshError) {
                        this.$router.push('/admin-login');
                      }
                    }
                  }
          },
        toggleDetails(sponsorId) {
          console.log('Toggling details for sponsor with ID:', sponsorId);
          this.showDetailsFor = this.showDetailsFor === sponsorId ? null : sponsorId;
        },

    async fetchNewSponsors() {
              try {
                const response = await axios.get('http://127.0.0.1:5000/dashboard/new_sponsors', {
                  headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                  },
                });
                this.newSponsor = response.data;
                console.log('newSponsor:', this.newSponsor); 
              } catch (error) {
                    if (error.response && error.response.status === 401) {
                      try {
                        const refreshToken = localStorage.getItem('refresh_token');
                        if (!refreshToken) {
                          this.$router.push('/admin-login');
                        }
                        await refreshAccessToken(refreshToken); 
                        
                        await this.fetchNewSponsors();
                      } catch (refreshError) {
                        this.$router.push('/admin-login');
                      }
                    }
                  }
            },
  async approveSponsor(userId) {
  try {
    const response = await axios.post(`http://127.0.0.1:5000/approve_sponsor/${userId}`, null, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    });
    console.log(response.data.message);
    // Refresh the new sponsors list
    this.fetchNewSponsors();
  } catch (error) {
    console.error('Error approving sponsor:', error);
  }
},

async rejectSponsor(userId) {
  try {
    const response = await axios.post(`http://127.0.0.1:5000/reject_sponsor/${userId}`, null, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    });
    console.log(response.data.message);
    // Refresh the new sponsors list
    this.fetchNewSponsors();
  } catch (error) {
    console.error('Error rejecting sponsor:', error);
  }
},


    getImageUrl(filename) {
      if (!filename) {
        return '';
      }
      
      // const correctedFilename = filename.replace(/\\/g, '/');
      // console.log(filename)
      const extractedFilename = filename.split('\\').pop();
      // console.log(extractedFilename)
      const imageUrl = `http://127.0.0.1:5000/show/${extractedFilename}`;
      // console.log(imageUrl)
    
      return imageUrl;
    },
    async logout() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/logout', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        console.log(response.data)

        if (response.data.message === "Logout successful") {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('username');
          this.$router.push('/admin-login');
        } else {
          // window.location.reload();
          
        }
      } catch (error) {
        console.error("An error occurred during logout:", error);
      }
    },
    reloadPage() {
      window.location.reload();
    }
  },
  created() {
    this.fetchAdminDetails();
    this.fetchSponsors();
    this.fetchInfluencers();
    this.fetchCampaigns();
    this.fetchAdRequests();
    
    
  }
};


</script>

<style scoped>
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;
  }
  .content-container {
  padding-top: 70px; /* To prevent content from being hidden behind the navbar */
  margin-left: 30px;
}
.nav-link {
  margin-right: 10px; /* Adds space between buttons */
}
.image {
    width: 100px;
      height: 100px; /* Maintain the aspect ratio */
  }
  .sponsor-details {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  padding: 20px;
  margin: 20px auto;
  background-color: #f9f9f9;
  border-radius: 10px;
  width: 80%; /* Adjust this width as needed */
  max-width: 1200px; /* Ensure it doesn't stretch too wide */
}

.sponsor-info {
  text-align: center;
  margin-bottom: 20px;
}

.sponsor-image {
  max-width: 250px; /* Resize the image */
  width: 100%;
  height: auto;
  border-radius: 8px;
  margin-bottom: 20px;
}

.campaigns-info {
  width: 100%;
}

.campaigns-list {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.campaign-card {
  background-color: #fff;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  border: 1px solid #ddd;
}

.campaign-card h6 {
  margin-top: 0;
  font-size: 1.1rem;
  color: #333;
}

</style>