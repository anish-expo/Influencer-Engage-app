<template>
   <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <a @click.prevent="reloadPage" class="navbar-brand">
        <img src="../assets/logo.png" width="30" height="30" alt="Logo">
        InfluencerApp
      </a>
      <div class="navbar-nav ml-auto">
        <button @click="setActiveSection('about')" class="btn btn-primary nav-link mx-1">About Me</button>
        <button @click="fetchMyAdCampaigns(); fetchAds(); fetchcompleteAdCampaigns(); setActiveSection('work')" class="btn btn-primary nav-link mx-1">My Work</button>
        <button @click="fetchReceivedRequests(); fetchSentRequests(); setActiveSection('requests')" class="btn btn-primary nav-link mx-1">Requests</button>
        
        <button @click="fetchCampaigns(); setActiveSection('campaigns')" class="btn btn-primary nav-link mx-1">Campaigns</button>
        <button @click="logout" class="btn btn-danger nav-link mx-1">Logout</button>
      </div>
    </nav>
  </div>

    <div class="content-container">
      
      <h2>Welcome,Influencer  {{ influencerDetails.name }}, </h2>
      
      <div v-if="activeSection === 'about'">
        <img class="image" :src="getImageUrl(influencerDetails.image)" alt="Sponsor Image"/>
        <p>Email: {{ influencerDetails.email }}</p>
        <p>Socialmedia: {{ influencerDetails.socialmedia }}</p>
        <p>Niche: {{ influencerDetails.niche }}</p>
        <p>Reach: {{ influencerDetails.reach }}</p>
        <p>Date Created: {{ influencerDetails.date_created }}</p>
        <p>Last Login: {{ influencerDetails.last_login }}</p>
        <button @click="openEditDetail(influencerDetails)" class="btn btn-primary me-2">Edit Profile</button>
      </div>


       <!-- Edit User details -->
     
       <div v-if="activeSection === 'editDetails'" class="modal-overlay">
            <div class="modal-content">
              <h5>Edit Details</h5>
              <form @submit.prevent="updateDetails">
                <div class="mb-3">
                  <label for="Name" class="form-label">Name</label>
                  <input
                    id="Name"
                    v-model="selectedDetails.name"
                    type="text"
                    class="form-control"
                  />
                </div>
                <div class="mb-3">
                  <label for="Userame" class="form-label">Username</label>
                  <input
                    id="Userame"
                    v-model="selectedDetails.username"
                    type="text"
                    class="form-control"
                  />
                </div>
                <div class="mb-3">
                  <label for="Email" class="form-label">Email</label>
                  <input
                    id="Email"
                    v-model="selectedDetails.email"
                    type="text"
                    class="form-control"
                  />
                </div>
                <div class="mb-3">
                  <label for="Socialmedia" class="form-label">Socialmedia</label>
                  <input
                    id="Socialmedia"
                    v-model="selectedDetails.socialmedia"
                    type="text"
                    class="form-control"
                  />
                </div>
                <div class="mb-3">
                  <label for="Reach" class="form-label">Reach</label>
                  <input
                    id="Reach"
                    v-model="selectedDetails.reach"
                    type="text"
                    class="form-control"
                  />
                </div>
                <div class="mb-3">
                  <label for="Niche" class="form-label">Niche</label>
                  <input
                    id="Niche"
                    v-model="selectedDetails.niche"
                    type="text"
                    class="form-control"
                  />
                </div>
                <div class="mb-3">
                  <label for="About" class="form-label">About</label>
                  <textarea
                    id="About"
                    v-model="selectedDetails.about"
                    class="form-control"
                  ></textarea>
                </div>
               
                <div class="modal-footer">
                  <button type="submit" class="btn btn-success">Save Changes</button>
                  <button type="button" @click="setActiveSection('about')" class="btn btn-secondary">Cancel</button>
                </div>
              </form>
            </div>
          </div>

             <!-- Campaigns Section -->
  <div v-if="activeSection === 'campaigns'" class="container mt-4">
    <!-- <div><pre>{{ campaigns1 }}</pre> </div> -->

    <h3 class="mb-3">Search Campaigns</h3>
              <div class="mb-3 d-flex align-items-center">
        
                <select v-model="searchType" class="form-control me-2">
                  <option value="name">Name</option>
                  <option value="budget">Budget</option>
                  <option value="target">Target</option>
                </select>
                <input v-model="searchQuery" type="text" class="form-control me-2" :placeholder="'Search by ' + searchType.charAt(0).toUpperCase() + searchType.slice(1)" />
                <button @click="searchCampaigns" class="btn btn-primary">Search</button>
              </div>

              <!-- Display Search Results -->
          <div v-if="filteredCampaigns.length > 0"> 
          <div class="campaigns-info">
                <div class="campaigns-list">
                  <div v-for="campaign in filteredCampaigns" :key="campaign.id" class="campaign-card">
                    <div class="campaign-actions">
                          <button @click="applyCampaign(campaign.id)" class="btn btn-primary me-2">Apply</button>
                          
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
            <!-- No results message -->
            <div v-else>
              <p>No Campaign found matching your search.</p>
            </div>

       <h3 class="mb-3">All Campaigns</h3>
       <div class="campaigns-info">
                
                <div class="campaigns-list">
                  <div v-for="campaign in campaigns1" :key="campaign.id" class="campaign-card">
                    <div class="campaign-actions">
                          <button @click="applyCampaign(campaign.id)" class="btn btn-primary me-2">Apply AdRequest</button>
                          
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

 <!-- Requests Section -->
<div v-if="activeSection === 'requests'">
  <h3>Your Requests</h3>
  <div>
    <button @click="activeTab = 'sent'">Sent Requests</button>
    <button @click="activeTab = 'received'">Received Requests</button>
  </div>

<!-- Sent Requests Section -->
<div v-if="activeTab === 'sent'" class="table-container">
  <h4>Sent Requests</h4>
  <table class="table table-bordered">
    <thead>
      <tr>
        <th>Campaign</th>
        <th>Influencer</th>
        <th>Requirements</th>
        <th>Payment Amount</th>
        <th>Status</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="request in sentRequests" :key="request.ad_request_id">
        <td>{{ request.campaign_name }}</td>
        <td>{{ request.influencer_name }}</td>
        <td>{{ request.requirements }}</td>
        <td>{{ request.payment_amount }}</td>
        <td>{{ request.status }}</td>
        <td>
          
          <button class="btn btn-danger btn-sm" @click="deleteRequest(request.ad_request_id)">Delete</button>
          <button class="btn btn-warning btn-sm" @click="negotiateRequest(request.ad_request_id,request.campaign_name)">Negotiate</button>
        </td>
      </tr>
    </tbody>
  </table>
</div>

<!-- Received Requests Section -->
<div v-if="activeTab === 'received'" class="table-container">
  <h4>Received Requests</h4>
  <table class="table table-bordered">
    <thead>
      <tr>
        <th>Campaign</th>
        <th>Influencer</th>
        <th>Requirements</th>
        <th>Payment Amount</th>
        <th>Status</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="request in receivedRequests" :key="request.ad_request_id">
        <td>{{ request.campaign_name }}</td>
        <td>{{ request.influencer_name }}</td>
        <td>{{ request.requirements }}</td>
        <td>{{ request.payment_amount }}</td>
        <td>{{ request.status }}</td>
        <td>
          <button class="btn btn-primary btn-sm" @click="acceptRequest(request.ad_request_id)">Accept</button>
          <button class="btn btn-danger btn-sm" @click="rejectRequest(request.ad_request_id)">Reject</button>
          
          <button class="btn btn-warning btn-sm" @click="negotiateRequest(request.ad_request_id,request.campaign_name)">Negotiate</button>
        </td>
      </tr>
    </tbody>
  </table>
</div>
</div>

<!-- Chat Modal -->
<!--  -->
<div v-if="showChat" class="modal-overlay">
  <div class="modal-content">
    <h4>Negotiation Chat for {{ currentcampaignName }} Campaign</h4>
    
        <!-- <div v-for="msg in chatMessages" :key="msg.id" class="chat-message">
          <strong>{{ msg.sender_id }}:</strong> {{ msg.content }}
        </div> -->
        <div v-for="msg in chatMessages" :key="msg.id" class="chat-message">
            <div class="message-container">
              <span class="sender-name">sender {{ msg.sender_name }}</span>
              <div class="message-content">
                {{ msg.content }}
                <span class="timestamp">{{ new Date(msg.timestamp).toLocaleString() }}</span>
              </div>
              <span class="receiver-name">reciver {{ msg.receiver_name }}</span>
            </div>
          </div>
        <div class="chat-input">
        <textarea
          v-model="newMessage"
          placeholder="Type your message..."
          class="form-control"
          rows="1"
        ></textarea>
        
      </div>
      <button class="btn btn-primary btn-sm mt-2" @click="sendMessage(newMessage, currentChatAdRequestId)">Send </button>
      
      <button type="button" class="btn btn-secondary" @click="closeChat">Close</button>
    
  </div>
</div>

<!-- My Work section -->
<div v-if="activeSection === 'work'" class="container mt-4">
  <h3 class="mb-3"> Pending Campaigns</h3>
       <div class="campaigns-info">
                
                <div class="campaigns-list">
                  <div v-for="campaign in workcampaigns" :key="campaign.id" class="campaign-card">
                    <div class="campaign-actions">
                          <button @click="makeAds(campaign.ad_request_id)" class="btn btn-primary me-2">Make Ads</button>
                          
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

              <h3 class="mb-3"> Complete Campaigns</h3>
       <div class="campaigns-info">
                
                <div class="campaigns-list">
                  <div v-for="campaign in completemywork" :key="campaign.id" class="campaign-card">
                    
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





              <!-- my adds -->
    <div class="my-ads-section">
    <h3>My Ads</h3>

    <!-- Ads Table -->
    <table v-if="ads.length > 0" class="ads-table">
      <thead>
        <tr>
          <th>Ad Name</th>
          <th>Campaign Name</th>
          <th>Ad Link</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ad in ads" :key="ad.ad_id">
          <td>{{ ad.ad_name }}</td>
          <td>{{ ad.campaign_name }}</td>
          <td>{{ ad.ad_link }}</td>
          <!-- <td>
            <a :href="ad.ad_link" target="_blank" rel="noopener noreferrer">
              View Ad
            </a>
          </td> -->
        </tr>
      </tbody>
    </table>

    <!-- No Ads Found -->
    <div v-if="!loading && ads.length === 0" class="no-ads-message">
      No ads found.
    </div>
  </div>

  </div>
  <!-- make add -->
    <div v-if="activeSection === 'makeadd'" class="modal-overlay">
      <div class="modal-content">
    <h4>Make Ads</h4>
    <form @submit.prevent="submitAdd">
      <div class="form-group">
        <label for="adName">Ad Name</label>
        <input type="text"
          id="adName"
          v-model="adName"
          class="form-control"
          placeholder="Enter Ad Name"
          required
        />
      </div>
      <div class="form-group">
        <label for="adLink">Ad Link</label>
        <input
          type="text"
          id="adLink"
          v-model="adLink"
          class="form-control"
          placeholder="Enter Ad Link"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Save Changes</button>
      <button type="button" class="btn btn-secondary" @click="closeMakeAd">Cancel</button>
    </form>
  </div>
    </div>




  



   </div>
  
</template>

<script>
import axios from 'axios';
import { refreshAccessToken } from '@/Services/refresh_token';

export default{
  name : 'InfluencerDashbord',
  data() {
    return {
      influencerDetails : {},
      activeSection: '', 
      selectedDetails:{},
      campaigns1: [],
      searchType: 'name', 
      searchQuery: '',
      filteredCampaigns: [],
      activeTab: 'sent',
      sentRequests: [],
      receivedRequests: [],
      showChat: false,
      currentcampaignName: '',
      chatMessages: [],
      newMessage: "",
      workcampaigns: [],
      completemywork:[],
      addcampaign: '',
      adName: "",
      adLink: "",
      ads: [],
      pollingInterval: null,

    };

  },

  mounted() {
    this.fetchInfluencerDetails();
    this.fetchCampaigns();
    this.fetchSentRequests();
    this.fetchReceivedRequests();
    this.fetchMyAdCampaigns();
    this.fetchAds();
    this.fetchcompleteAdCampaigns();
    this.setActiveSection('about');

  },
  methods : { 
                async fetchAds() {
                  try {
                    const response = await axios.get('http://127.0.0.1:5000/my_ads', {
                      headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`, 
                      },
                    });
                    this.ads = response.data;
                  } catch (error) {
                        if (error.response && error.response.status === 401) {
                                        try {
                                          const refreshToken = localStorage.getItem('refresh_token');
                                          if (!refreshToken) {
                                            this.$router.push('/login');
                                          }
                                          await refreshAccessToken(refreshToken); 
                                          
                                          await this.fetchAds();
                                        } catch (refreshError) {
                                          this.$router.push('/login');
                                        }
                                      }
                                    }
                },
                async submitAdd() {
                try {
                  if ( !this.adName || !this.adLink) {
                    alert("Please fill in all required fields.");
                    return;
                  }
                  const payload = {
                    ad_request_id: this.addcampaign,
                    name: this.adName,
                    link: this.adLink,
                  };
                  const response = await fetch("http://127.0.0.1:5000/create_ad", {
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json",
                      Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                    },
                    body: JSON.stringify(payload),
                  });

                  const data = await response.json();

                  if (response.ok) {
                    alert(data.message);
                    this.closeMakeAd();
                  } else {
                    alert(`Failed to create ad: ${data.message || "Unknown error"}`);
                  }
                } catch (error) {
                  console.error("Error creating ad:", error);
                  alert("An error occurred while creating the ad. Please try again.");
                }
              },
                closeMakeAd() {
                  this.setActiveSection('work');
                  this.adName = "";
                  this.adLink = "";
                    },
                      makeAds(ad_request_id) {
                        // console.log('edit pressed')
                      this.addcampaign = ad_request_id ; 
                      // console.log(this.addcampaign);
                      
                      this.setActiveSection('makeadd')
                      // console.log(this.showEditModal)
                    },
                    async fetchcompleteAdCampaigns() {
                        try {
                          const response = await axios.get('http://127.0.0.1:5000/completemywork',{
                                    headers: {
                                      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                                    },});
                          if (response.data) {
                            this.completemywork = response.data;
                            // console.log(this.workcampaigns);
                          }
                        } catch (error) {
                                      if (error.response && error.response.status === 401) {
                                        try {
                                          const refreshToken = localStorage.getItem('refresh_token');
                                          if (!refreshToken) {
                                            this.$router.push('/login');
                                          }
                                          await refreshAccessToken(refreshToken); 
                                          
                                          await this.fetchMyAdCampaigns();
                                        } catch (refreshError) {
                                          this.$router.push('/login');
                                        }
                                      }
                                    }
                        
                      },   
                 async fetchMyAdCampaigns() {
                        try {
                          const response = await axios.get('http://127.0.0.1:5000/mywork',{
                                    headers: {
                                      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                                    },});
                          if (response.data) {
                            this.workcampaigns = response.data;
                            // console.log(this.workcampaigns);
                          }
                        } catch (error) {
                                      if (error.response && error.response.status === 401) {
                                        try {
                                          const refreshToken = localStorage.getItem('refresh_token');
                                          if (!refreshToken) {
                                            this.$router.push('/login');
                                          }
                                          await refreshAccessToken(refreshToken); 
                                          
                                          await this.fetchMyAdCampaigns();
                                        } catch (refreshError) {
                                          this.$router.push('/login');
                                        }
                                      }
                                    }
                        
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
                          this.$router.push('/login');
                        } else {
                          // window.location.reload();
                          
                        }
                      } catch (error) {
                    if (error.response && error.response.status === 401) {
                      try {
                        const refreshToken = localStorage.getItem('refresh_token');
                        if (!refreshToken) {
                          this.$router.push('/login');
                        }
                        await refreshAccessToken(refreshToken);
                        await this.logout();
                      } catch (refreshError) {
                        this.$router.push('/login');
                      }
                    }
                  }
                    },

                    startMessagePolling(adRequestId) {
                        this.pollingInterval = setInterval(() => {
                          this.fetchMessages(adRequestId);
                        }, 5000); 
                      },  
                  negotiateRequest(adRequestId,campaignName) {
                  this.currentChatAdRequestId = adRequestId;
                  this.currentcampaignName = campaignName;
                  // console.log(this.currentChatAdRequestId,this.currentcampaignName);
                  this.fetchMessages(adRequestId); 
                  
                  this.showChat = true;
                  this.startMessagePolling(adRequestId);
                },
                closeChat() {
                  this.showChat = false;
                  this.currentChatAdRequestId = null;
                  this.chatMessages = []; 
                  this.newMessage = "";   
                  clearInterval(this.pollingInterval);
                },


            async sendMessage(content, adRequestId) {
              try {
                if (!content.trim()) {
                  this.$toast.error("Message cannot be empty");
                  return;
                }
                
                await axios.post(
                  `http://127.0.0.1:5000/ad_request/chat/${adRequestId}/send`,
                  { content },
                  {
                    headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
                  }
                );
                
                this.newMessage = ""; 
                this.fetchMessages(adRequestId); 
                // this.setActiveSection('requests');
              } catch (error) {
                    if (error.response && error.response.status === 401) {
                      try {
                        const refreshToken = localStorage.getItem('refresh_token');
                        if (!refreshToken) {
                          this.$router.push('/admin-login');
                        }
                        await refreshAccessToken(refreshToken);
                        await this.fetchMessages(adRequestId);
                      } catch (refreshError) {
                        this.$router.push('/login');
                      }
                    }
                  }
            },

          async fetchMessages(adRequestId) {
          try {
            const response = await axios.get(
              `http://127.0.0.1:5000/ad_request/chat/${adRequestId}/messages`,
              {
                headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
              }
            );
            this.chatMessages = response.data.messages;
            // console.log('chat:',this.chatMessages)
          } catch (error) {
                    if (error.response && error.response.status === 401) {
                      try {
                        const refreshToken = localStorage.getItem('refresh_token');
                        if (!refreshToken) {
                          this.$router.push('/admin-login');
                        }
                        await refreshAccessToken(refreshToken);
                        await this.fetchMessages(adRequestId);
                      } catch (refreshError) {
                        this.$router.push('/login');
                      }
                    }
                  }
        },

                 async rejectRequest(adRequestId) {
                  try {
                    const userConfirmed = confirm("Are you sure you want to reject this request?  once rejected can't be accepted.");
                    if (!userConfirmed) {
                      return;
                    }
                    const response = await axios.put(
                      `http://127.0.0.1:5000/ad_request_reject/${adRequestId}`,
                      {},
                      {
                        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
                      }
                    );

                    alert(response.data.message);
                    this.fetchReceivedRequests();
                  } catch (error) {
              if (error.response && error.response.status === 401) {
                try {
                  const refreshToken = localStorage.getItem('refresh_token');
                  if (!refreshToken) {
                    this.$router.push('/admin-login');
                  }
                  await refreshAccessToken(refreshToken);
                  await this.fetchReceivedRequests();
                } catch (refreshError) {
                  this.$router.push('/login');
                }
              } else {
                console.error('Error deleting ad request:', error);
                this.$toast.error('Failed to delete request');
              }
            }
                },

              async acceptRequest(adRequestId) {
                try {
                  const response = await axios.put(
                    `http://127.0.0.1:5000/ad_request_accept/${adRequestId}`,
                    {},
                    {
                      headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
                    }
                  );
                  alert(response.data.message);

                  this.fetchReceivedRequests();
                } catch (error) {
              if (error.response && error.response.status === 401) {
                try {
                  const refreshToken = localStorage.getItem('refresh_token');
                  if (!refreshToken) {
                    this.$router.push('/admin-login');
                  }
                  await refreshAccessToken(refreshToken);
                  await this.fetchReceivedRequests();
                } catch (refreshError) {
                  this.$router.push('/login');
                }
              } else {
                console.error('Error deleting ad request:', error);
                this.$toast.error('Failed to delete request');
              }
            }
              },
              async deleteRequest(adRequestId) {
                      try {
                        const userConfirmed = confirm("Are you sure you want to delete this request? ");
                    if (!userConfirmed) {
                      return;
                    }
                        const response = await axios.delete(`http://127.0.0.1:5000/ad_request_dellete/${adRequestId}`, {
                          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
                        });
                        alert(response.data.message);
                        this.fetchSentRequests();
                      } catch (error) {
                        if (error.response && error.response.status === 401) {
                          try {
                            const refreshToken = localStorage.getItem('refresh_token');
                            if (!refreshToken) {
                              this.$router.push('/admin-login');
                            }
                            await refreshAccessToken(refreshToken);
                            await this.fetchSentRequests();
                          } catch (refreshError) {
                            this.$router.push('/login');
                          }
                        } else {
                          console.error('Error deleting ad request:', error);
                          this.$toast.error('Failed to delete request');
                        }
                      }
                    },
                     async fetchReceivedRequests() {
                      try {
                        const response = await axios.get('http://127.0.0.1:5000/inf_ad_requests/received', {
                          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                        });
                        this.receivedRequests = response.data;
                      } catch (error) {
                                if (error.response && error.response.status === 401) {
                                  try {
                                    const refreshToken = localStorage.getItem('refresh_token');
                                    if (!refreshToken) {
                                      this.$router.push('/admin-login');
                                    }
                                    await refreshAccessToken(refreshToken); 
                                    
                                    await this.fetchReceivedRequests();
                                  } catch (refreshError) {
                                    this.$router.push('/login');
                                  }
                                }
                              }
                    },
                     async fetchSentRequests() {
                      try {
                        const response = await axios.get('http://127.0.0.1:5000/ad_requests/sent', {
                          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                        });
                        this.sentRequests = response.data;
                        alert(this.response.data.message);
                      } catch (error) {
                                if (error.response && error.response.status === 401) {
                                  try {
                                    const refreshToken = localStorage.getItem('refresh_token');
                                    if (!refreshToken) {
                                      this.$router.push('/admin-login');
                                    }
                                    await refreshAccessToken(refreshToken); 
                                    
                                    await this.fetchSentRequests();
                                  } catch (refreshError) {
                                    this.$router.push('/login');
                                  }
                                }
                              }
                    },
                   async applyCampaign( campaignId) {
                          try {
                            const response = await axios.post('http://127.0.0.1:5000/make_ad_request', {
                              campaign_id: campaignId  
                            }, {
                              headers: {
                                'Authorization': `Bearer ${localStorage.getItem('access_token')}`  
                              }
                            });

                            if (response.data.message === 'Ad request created successfully' || response.data.message === 'Ad request already exists') {
                              alert(response.data.message);
                              this.fetchSentRequests();
                              this.setActiveSection('requests');
                            } else {
                              alert("Failed to create ad request.");
                            }
                          } catch (error) {
                                if (error.response && error.response.status === 401) {
                                  try {
                                    const refreshToken = localStorage.getItem('refresh_token');
                                    if (!refreshToken) {
                                      this.$router.push('/admin-login');
                                    }
                                    await refreshAccessToken(refreshToken); 
                                    
                                    await this.fetchCampaigns();
                                    this.setActiveSection('campaigns');
                                  } catch (refreshError) {
                                    this.$router.push('/login');
                                  }
                                }
                              }
                        },
                       searchCampaigns() {
                        const searchValue = this.searchQuery.toLowerCase(); 
                        if (this.searchQuery.trim() === '') {
                          this.filteredCampaigns = this.campaigns1;
                          return;
                        }
                        this.filteredCampaigns = this.campaigns1.filter(campaign => {
                          if (this.searchType === 'name') {
                            return campaign.name.toLowerCase().includes(searchValue);
                          } else if (this.searchType === 'budget') {
                            const campaignBudget = Number(campaign.budget);
                            const searchBudget = Number(searchValue);
                            return !isNaN(campaignBudget) && !isNaN(searchBudget) && campaignBudget.toString().includes(searchBudget.toString());
                          } else if (this.searchType === 'target') {
                            const campaignTarget = Number(campaign.target);
                            const searchTarget = Number(searchValue);
                            return !isNaN(campaignTarget) && !isNaN(searchTarget) && campaignTarget.toString().includes(searchTarget.toString());
                          }
                          return true; 
                        });
                      },
                async fetchCampaigns() {
                        try {
                          const response = await axios.get('http://127.0.0.1:5000/allcampaigns',{
                                    headers: {
                                      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                                    },});
                          if (response.data) {
                            this.campaigns1 = response.data.campaigns;
                            // console.log(this.campaigns1);
                          }
                        } catch (error) {
                                      if (error.response && error.response.status === 401) {
                                        try {
                                          const refreshToken = localStorage.getItem('refresh_token');
                                          if (!refreshToken) {
                                            this.$router.push('/login');
                                          }
                                          await refreshAccessToken(refreshToken); 
                                          
                                          await this.fetchCampaigns();
                                        } catch (refreshError) {
                                          this.$router.push('/login');
                                        }
                                      }
                                    }
                        
                      },
              async  updateDetails() {
                try {
                        await axios.put(`http://127.0.0.1:5000/updatedetail`, this.selectedDetails, {
                          headers: {
                            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                          },
                        });

                        this.fetchInfluencerDetails();
                        this.setActiveSection('about');
                      } catch (error) {
                        if (error.response && error.response.status === 401) {
                          try {
                            const refreshToken = localStorage.getItem('refresh_token');
                            if (!refreshToken) {
                              this.$router.push('/login');
                              return;
                            }
                            await this.refreshAccessToken(refreshToken);
                            await this.updateDetails(); 
                          } catch (refreshError) {
                            this.$router.push('/login');
                          }
                        } else {
                          console.error('Error updating campaign:', error);
                          alert('Failed to update campaign. Please try again.');
                        }
                      }
              },

                openEditDetail(influencerDetails) {
                      // console.log('edit pressed')
                    this.selectedDetails = { ...influencerDetails }; 
                    
                    this.setActiveSection('editDetails')
                    // console.log(this.showEditModal)
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
    setActiveSection(section) {
      this.activeSection = section;
    },

    async fetchInfluencerDetails() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/dashboard/influencer_details',{
                  headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                  },});
        if (response.data) {
          this.influencerDetails = response.data;
        }
      } catch (error) {
                    if (error.response && error.response.status === 401) {
                      try {
                        const refreshToken = localStorage.getItem('refresh_token');
                        if (!refreshToken) {
                          this.$router.push('/admin-login');
                        }
                        await refreshAccessToken(refreshToken); 
                        
                        await this.fetchInfluencerDetails();
                      } catch (refreshError) {
                        this.$router.push('/login');
                      }
                    }
                  }
    },
    reloadPage() {
      window.location.reload();
    }

  }


}

</script>

<style scoped>
.my-ads-section {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}


.ads-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}
.ads-table th,
.ads-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
.ads-table th {
  background-color: #f4f4f4;
}
.no-ads-message {
  text-align: center;
  color: gray;
  margin-top: 20px;
}
.chat-message {
  margin: 10px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.message-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.sender-name,
.receiver-name {
  width: 15%;
  font-weight: bold;
  text-align: center;
  color: #555;
}

.message-content {
  width: 70%;
  text-align: center;
  position: relative;
}

.timestamp {
  display: block;
  font-size: 0.8rem;
  color: #aaa;
  margin-top: 5px;
  text-align: right;
}

.modal-overlay {
  position: absolute; /* Adjusted to ensure it stays within the page */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Transparent background */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000; /* Ensure it appears above other elements */
}

.modal-content {
  background-color: #fff; /* White background for modal */
  padding: 20px;
  width: 90%; /* Make it responsive */
  max-width: 600px; /* Set a maximum width */
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  overflow-y: auto; /* Add scroll for overflowing content */
  max-height: 80%; /* Limit the modal's height */
}

.modal-footer {
  display: flex;
  justify-content: flex-end; /* Align buttons to the right */
  gap: 10px;
  margin-top: 20px;
}

.modal-content input,
.modal-content textarea,
.modal-content select {
  width: 100%; /* Make inputs span full width */
  margin-bottom: 15px;
}

.modal-content h5 {
  margin-bottom: 20px;
  text-align: center;
}

.campaign-actions {
  margin-top: 10px;
}

.campaign-actions .btn {
  font-size: 0.9rem;
  padding: 5px 10px;
}
.campaign-card {
  background-color: #fff;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  border: 1px solid #ddd;
}
.campaigns-info {
  width: 100%;
}

.campaigns-list {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}
.content-container {
  padding: 20px;
}

.text-center {
  text-align: center;
}

/* Flexbox container to center the about content */
.about-section {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  text-align: center;
  margin-top: 20px;
}

/* Style for the image (resize and center it) */
.image {
  width: 150px; /* Resize the image */
  height: 150px; /* Resize the image */
  border-radius: 50%;
  margin-bottom: 20px;
  object-fit: cover; /* Ensure the image fits well */
}

/* Additional styling for text content */
.about-content p {
  font-size: 16px;
  margin: 5px 0;
}
.form-group {
  margin-bottom: 15px;
}

button[type='submit'] {
  margin-top: 15px;
}
</style>