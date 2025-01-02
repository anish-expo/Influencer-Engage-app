<template>
   <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <a @click.prevent="reloadPage" class="navbar-brand">
        <img src="../assets/logo.png" width="30" height="30" alt="Logo">
        InfluencerApp
      </a>
      <div class="navbar-nav ml-auto">
        <button @click="setActiveSection('about')" class="btn btn-primary nav-link mx-1">About Me</button>
        <button @click="setActiveSection('create_campaigns')" class="btn btn-primary nav-link mx-1">Create Campaigns</button>
        <button @click="fetchCampaigns(); setActiveSection('campaigns') " class="btn btn-primary nav-link mx-1">Campaigns</button>
        <button @click="fetchFlagCampaigns(); setActiveSection('flagcampaign')" class="btn btn-primary nav-link mx-1">Flagged Campaigns</button>
        <button @click="fetchSentRequests(); fetchReceivedRequests(); setActiveSection('requests')" class="btn btn-primary nav-link mx-1">Requests</button>
        <button @click="fetchInfluencer(); setActiveSection('addinf')" class="btn btn-primary nav-link mx-1">Add Influencer</button>
        <button @click="logout" class="btn btn-danger nav-link mx-1">Logout</button>
      </div>
    </nav>

    <div class="content-container">
      
      <h2>Welcome,Sponsor  {{ sponsorDetails.name }}, </h2>
      
      <div v-if="activeSection === 'about'">
        <img class="image" :src="getImageUrl(sponsorDetails.image)" alt="Sponsor Image"/>
        <p>Email: {{ sponsorDetails.email }}</p>
        <p>Role: {{ sponsorDetails.role }}</p>
        <p>Date Created: {{ sponsorDetails.date_created }}</p>
        <p>Last Login: {{ sponsorDetails.last_login }}</p>
        <button @click="exportCampaigns">Export Campaigns as CSV</button>
      </div>
    

      <!-- Create Campaign Section -->
                <div v-if="activeSection === 'create_campaigns'" >
                <h3>Create New Campaign</h3>

                <form @submit.prevent="submitCampaignForm" enctype="multipart/form-data">
                    <!-- Campaign Name -->
                    <div class="form-group">
                    <label for="name">Campaign Name</label>
                    <input type="text" id="name" v-model="campaign.name" class="form-control" required />
                    </div>

                    <!-- Description -->
                    <div class="form-group">
                    <label for="description">Description</label>
                    <textarea id="description" v-model="campaign.description" class="form-control" rows="4" required></textarea>
                    </div>

                    <!-- Start Date -->
                    <div class="form-group">
                    <label for="start_date">Start Date</label>
                    <input type="date" id="start_date" v-model="campaign.start_date" class="form-control" required />
                    </div>

                    <!-- End Date -->
                    <div class="form-group">
                    <label for="end_date">End Date</label>
                    <input type="date" id="end_date" v-model="campaign.end_date" class="form-control" required />
                    </div>

                    <!-- Budget -->
                    <div class="form-group">
                    <label for="budget">Budget</label>
                    <input type="number" id="budget" v-model="campaign.budget" class="form-control" required />
                    </div>

                    <!-- Visibility -->
                    <div class="form-group">
                    <label for="visibility">Visibility</label>
                    <select id="visibility" v-model="campaign.visibility" class="form-control" required>
                        <option value="public">Public</option>
                        <option value="private">Private</option>
                    </select>
                    </div>

                    <!-- Goals -->
                    <div class="form-group">
                    <label for="goals">Goals</label>
                    <textarea id="goals" v-model="campaign.goals" class="form-control" rows="3"></textarea>
                    </div>

                    <!-- Target -->
                    <div class="form-group">
                    <label for="target">Target</label>
                    <input type="number" id="target" v-model="campaign.target" class="form-control" required />
                    </div>

                    <!-- Image Upload -->
                    <div class="form-group">
                    <label for="file">Upload Campaign Image</label>
                    <input type="file" id="file" @change="previewImage" class="form-control" />
                    <img v-if="imagePreview" :src="imagePreview" alt="Image Preview" width="100" />
                    </div>

                    <!-- Submit Button -->
                    <button type="submit" class="btn btn-primary">Create Campaign</button>
                </form>
                </div>

                
      <!-- Campaigns Section -->
  <div v-if="activeSection === 'campaigns'" class="container mt-4">
    <!-- <div><pre>{{ campaigns1 }}</pre> </div> -->
       <h3 class="mb-3">Your Campaigns</h3>
       <div class="campaigns-info">
                
                <div class="campaigns-list">
                  <div v-for="campaign in campaigns1" :key="campaign.id" class="campaign-card">
                    <div class="campaign-actions">
                          <button @click="openEditCampaign(campaign)" class="btn btn-primary me-2">Edit</button>
                          <button @click="deleteCampaign(campaign.id)" class="btn btn-danger">Delete</button>
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

     <!-- Flag Campaigns Section -->
  <div v-if="activeSection === 'flagcampaign'" class="container mt-4">
    <!-- <div><pre>{{ campaigns1 }}</pre> </div> -->
       <h3 class="mb-3">Flagged Campaigns</h3>
       <div class="campaigns-info">
                
                <div class="campaigns-list">
                  <div v-for="campaign in flagcampaigns" :key="campaign.id" class="campaign-card">
                    <div class="campaign-actions">
                          <button @click="openEditCampaign(campaign)" class="btn btn-primary me-2">Edit</button>
                          <button @click="deleteCampaign(campaign.id)" class="btn btn-danger">Delete</button>
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
          
    <!-- Edit Campaign -->
     
              <div v-if="activeSection === 'editcampaigns'" class="modal-overlay">
            <div class="modal-content">
              <h5>Edit Campaign</h5>
              <form @submit.prevent="updateCampaign">
                <div class="mb-3">
                  <label for="campaignName" class="form-label">Name</label>
                  <input
                    id="campaignName"
                    v-model="selectedCampaign.name"
                    type="text"
                    class="form-control"
                  />
                </div>
                <div class="mb-3">
                  <label for="campaignDescription" class="form-label">Description</label>
                  <textarea
                    id="campaignDescription"
                    v-model="selectedCampaign.description"
                    class="form-control"
                  ></textarea>
                </div>
                <div class="mb-3">
                  <label for="campaignBudget" class="form-label">Budget</label>
                  <input
                    id="campaignBudget"
                    v-model="selectedCampaign.budget"
                    type="number"
                    class="form-control"
                  />
                </div>
                <div class="mb-3">
                  <label for="campaignGoals" class="form-label">Goals</label>
                  <input
                    id="campaignGoals"
                    v-model="selectedCampaign.goals"
                    type="text"
                    class="form-control"
                  />
                </div>
                <div class="mb-3">
                  <label for="campaignStartDate" class="form-label">Start Date</label>
                  <input
                    id="campaignStartDate"
                    v-model="selectedCampaign.start_date"
                    type="date"
                    class="form-control"
                  />
                </div>
                <div class="mb-3">
                  <label for="campaignEndDate" class="form-label">End Date</label>
                  <input
                    id="campaignEndDate"
                    v-model="selectedCampaign.end_date"
                    type="date"
                    class="form-control"
                  />
                </div>
                <div class="mb-3">
                  <label for="campaignVisibility" class="form-label">Visibility</label>
                  <select
                    id="campaignVisibility"
                    v-model="selectedCampaign.visibility"
                    class="form-control"
                  >
                    <option value="public">Public</option>
                    <option value="private">Private</option>
                  </select>
                </div>
                <div class="mb-3">
                  <label for="campaignTarget" class="form-label">Target</label>
                  <input
                    id="campaignTarget"
                    v-model="selectedCampaign.target"
                    type="number"
                    class="form-control"
                  />
                </div>
                 <!-- Image Upload -->
                 <div class="mb-3">
                    <label for="file" class="form-label">Upload Campaign Image</label>
                    <input type="file" id="file"   @change="previewImagedit" class="form-control" />
                    <img v-if="imagePreviewedit" :src="imagePreviewedit" alt="Image Preview" width="100" />
                    </div>
                <div class="modal-footer">
                  <button type="submit" class="btn btn-success">Save Changes</button>
                  <button type="button" @click="setActiveSection('campaigns')" class="btn btn-secondary">Cancel</button>
                </div>
              </form>
            </div>
          </div>




      
        <!-- addinfluencer Section -->
        <div v-if="activeSection === 'addinf'" class="container mt-4">
          <h3 class="mb-3">Search Influencers</h3>
  
              <div class="mb-3 d-flex align-items-center">
        
                <select v-model="searchType" class="form-control me-2">
                  <option value="name">Name</option>
                  <option value="reach">Reach</option>
                  <option value="niche">Niche</option>
                </select>
                <input v-model="searchQuery" type="text" class="form-control me-2" :placeholder="'Search by ' + searchType.charAt(0).toUpperCase() + searchType.slice(1)" />
                <button @click="searchInfluencers" class="btn btn-primary">Search</button>
              </div>


          <!-- Display Search Results -->
          <div v-if="filteredInfluencers.length > 0"> 
          <div class="campaigns-info">
                <div class="campaigns-list">
                  <div v-for="influencer in filteredInfluencers" :key="influencer.id" class="campaign-card">
                    <div class="campaign-selection">
                              <label for="campaign">Select Campaign</label>
                              <select v-model="selectedCampaigns[influencer.id]" class="form-control mb-2">
                                <option value="" disabled selected>Select a campaign</option>
                                <option v-for="campaign in campaigns1" :key="campaign.id" :value="campaign.id">
                                  {{ campaign.name }}
                                </option>
                              </select>
                              <button @click="submitAdRequest(influencer.id, selectedCampaigns[influencer.id])" class="btn btn-success mt-2" :disabled="!selectedCampaigns[influencer.id]">
                                Send Ad Request
                              </button>
                            </div>
                    <h6><strong>Name::</strong> {{ influencer.name }}</h6>
                    <p><strong>Email:</strong> {{ influencer.email }}</p>
                    <p><strong>Reach:</strong> {{ influencer.reach }}</p>
                    <p><strong>Niche:</strong> {{ influencer.niche }}</p>
                    <p><strong>SocialMedia:</strong> {{ influencer.socialmedia }}</p>
                    <p><strong>About:</strong> {{ influencer.about }}</p>
                   
                    <p>Created: {{ influencer.date_created ? new Date(influencer.date_created).toLocaleDateString() : '' }}</p>
                    <p>Last Login: {{ influencer.last_login ? new Date(influencer.last_login).toLocaleDateString() : '' }}</p>
                    <img class="image" :src="getImageUrl(influencer.image)" alt="Sponsor Image"/>
                  </div>
                </div>
              </div>
            </div>
            <!-- No results message -->
            <div v-else>
              <p>No influencers found matching your search.</p>
            </div>
                
       <h3 class="mb-3">Avalable Influencers</h3>
       <div class="campaigns-info">
                
                <div class="campaigns-list">
                  <div v-for="influencer in influencers" :key="influencer.id" class="campaign-card">
                    
                            <div class="campaign-selection">
                              <label for="campaign">Select Campaign</label>
                              <select v-model="selectedCampaigns[influencer.id]" class="form-control mb-2">
                                <option value="" disabled selected>Select a campaign</option>
                                <option v-for="campaign in campaigns1" :key="campaign.id" :value="campaign.id">
                                  {{ campaign.name }}
                                </option>
                                
                              </select>
                              <button @click="submitAdRequest(influencer.id, selectedCampaigns[influencer.id])" class="btn btn-success mt-2" :disabled="!selectedCampaigns[influencer.id]">
                                Send Ad Request
                              </button>
                            </div>
                    <h6><strong>Name::</strong> {{ influencer.name }}</h6>
                    <p><strong>Email:</strong> {{ influencer.email }}</p>
                    <p><strong>Reach:</strong> {{ influencer.reach }}</p>
                    <p><strong>Niche:</strong> {{ influencer.niche }}</p>
                    <p><strong>SocialMedia:</strong> {{ influencer.socialmedia }}</p>
                    <p><strong>About:</strong> {{ influencer.about }}</p>
                   
                    <p>Created: {{ influencer.date_created ? new Date(influencer.date_created).toLocaleDateString() : '' }}</p>
                    <p>Last Login: {{ influencer.last_login ? new Date(influencer.last_login).toLocaleDateString() : '' }}</p>
                    <img class="image" :src="getImageUrl(influencer.image)" alt="Sponsor Image"/>
                  </div>
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
          <button class="btn btn-primary btn-sm" @click="editRequest(request)">Edit</button>
          <button class="btn btn-danger btn-sm" @click="deleteRequest(request.ad_request_id)">Delete</button>
          <button class="btn btn-warning btn-sm" @click="negotiateRequest(request.ad_request_id,request.campaign_name)">Negotiate</button>
          <!-- <button class="btn btn-warning btn-sm" @click="openNegotiationChat(request.ad_request_id)">
                                              Negotiate
                                              <span v-if="unreadMessages[request.ad_request_id] > 0" class="badge badge-danger">
                                                {{ unreadMessages[request.ad_request_id] }}
                                              </span>
          </button> -->

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
          <button class="btn btn-primary btn-sm" @click="editRequest(request)">Edit</button>
          <button class="btn btn-warning btn-sm" @click="negotiateRequest(request.ad_request_id,request.campaign_name)">Negotiate</button>
          <!-- <button class="btn btn-warning btn-sm" @click="openNegotiationChat(request.ad_request_id)">
                                              Negotiate
                                              <span v-if="unreadMessages[request.ad_request_id] > 0" class="badge badge-danger">
                                                {{ unreadMessages[request.ad_request_id] }}
                                              </span>
          </button> -->

        </td>
      </tr>
    </tbody>
  </table>
</div>
</div>
<!-- Edit for Requirements and Payment Amount -->

<div v-if="showEditModal" class="modal-overlay">
  <div class="modal-content">
    <h4>Edit Request</h4>
    <form @submit.prevent="submitEditRequest">
      <div class="form-group">
        <label for="requirements">Requirements</label>
        <input type="text" v-model="editRequestData.requirements" id="requirements" class="form-control" required>
      </div>
      <div class="form-group">
        <label for="payment_amount">Payment Amount</label>
        <input type="number" v-model="editRequestData.payment_amount" id="payment_amount" class="form-control" required>
      </div>
      <button type="submit" class="btn btn-primary">Save Changes</button>
      <button type="button" class="btn btn-secondary" @click="closeEditModal">Cancel</button>
    </form>
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

  </div>
</template>

<script>
import axios from 'axios';
import { refreshAccessToken } from '@/Services/refresh_token';

export default{
    name: 'SponsorDashboard',
    data() {
    return {
        campaign: {
        name: '',
        description: '',
        start_date: '',
        end_date: '',
        budget: '',
        visibility: 'public',
        goals: '',
        target: '',
        file: null,
        
         },
         searchType: 'name', 
         searchQuery: '',
      
        activeSection: '', 
      sponsorDetails: {},
      campaigns1: [],
      flagcampaigns:[], 
      influencers:[],
      filteredInfluencers: [],
      selectedCampaigns:{},
      activeTab: 'sent',
      sentRequests: [],
      receivedRequests: [],
      editRequestData: {
              requirements: '',
              payment_amount: null,
            },
    selectedRequestId: null,
    showEditModal: false,
    showChat: false,

    currentChatAdRequestId: null,
    currentcampaignName: '',
    chatMessages: [],            
    newMessage: "", 
    imagePreview: null,
    imagePreviewedit: null,
    image: null,
    selectedFile: null,
    pollingInterval: null,
    
    };
  },
  mounted() {
    this.fetchSponsorDetails();
    this.fetchCampaigns();
    this.fetchInfluencer();
    this.fetchSentRequests();
    this.fetchReceivedRequests();
    this.fetchFlagCampaigns();
    this.setActiveSection('campaigns');


  },
  methods : {
    previewImagedit(event) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.imagePreviewedit = URL.createObjectURL(file);
    } else {
      this.selectedFile = null;
      this.imagePreviewedit = null;
    }
  },
    previewImage(event) {
    const file = event.target.files[0];
    if (file) {
        this.campaign.file = file; 
        const reader = new FileReader();
        reader.onload = (e) => {
            this.imagePreview = e.target.result; 
        };
        reader.readAsDataURL(file);
    }
},
            async exportCampaigns() {
              try {
                const response = await fetch('http://127.0.0.1:5000/export_campaigns', {
                  method: 'POST',
                  headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                    'Content-Type': 'application/json'
                  },
                });

                if (response.ok) {
                  // Create a download link for the CSV file
                  const blob = await response.blob();
                  const link = document.createElement('a');
                  link.href = URL.createObjectURL(blob);
                  link.download = 'campaigns.csv';
                  link.click();
                } else {
                  console.error('Failed to export campaigns');
                }
              } catch (error) {
                console.error('Error exporting campaigns:', error);
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
                    this.$router.push('/admin-login');
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
                    const userConfirmed = confirm("Are you sure you want to delete this reject request? once rejected can't be accepted ");
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
              const response = await axios.delete(`http://127.0.0.1:5000/ad_request/${adRequestId}`, {
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
          async submitEditRequest() {
            try {
              const response = await axios.put(`http://127.0.0.1:5000/ad_request/${this.selectedRequestId}`, this.editRequestData, {
                headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
              });

              alert(response.data.message);
              this.fetchSentRequests(); 
              this.fetchReceivedRequests();
              this.closeEditModal(); 
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
                
                console.error('Error updating ad request:', error);
                this.$toast.error('Failed to update request');
              }
            }
          },
                      closeEditModal() {
                      this.showEditModal = false;
                      this.editRequestData = { requirements: '', payment_amount: null }; 
                    },

                   editRequest(request) {
                      this.selectedRequestId = request.ad_request_id;
                      this.editRequestData.requirements = request.requirements;
                      this.editRequestData.payment_amount = request.payment_amount;
                      this.showEditModal = true;
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

                    async fetchReceivedRequests() {
                      try {
                        const response = await axios.get('http://127.0.0.1:5000/ad_requests/received', {
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

                          async submitAdRequest(influencerId, campaignId) {
                            // console.log(campaignId)
                          if (!campaignId) {
                            alert("Please select a campaign.");
                            return;
                          }
                          try {
                            const response = await axios.post('http://127.0.0.1:5000/ad_request', {
                              campaign_id: campaignId,  
                              influencer_id: influencerId  
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
                                    
                                    await this.fetchInfluencer();
                                    this.setActiveSection('addinf');
                                  } catch (refreshError) {
                                    this.$router.push('/login');
                                  }
                                }
                              }
                        },


                        searchInfluencers() {
                        const searchValue = this.searchQuery.toLowerCase(); 
                        if (this.searchQuery.trim() === '') {
                          this.filteredInfluencers = this.influencers;
                          return;
                        }
                        this.filteredInfluencers = this.influencers.filter(influencer => {
                          if (this.searchType === 'name') {
                            return influencer.name.toLowerCase().includes(searchValue);
                          } else if (this.searchType === 'reach') {
                            return influencer.reach.toLowerCase().includes(searchValue);
                          } else if (this.searchType === 'niche') {
                            return influencer.niche.toLowerCase().includes(searchValue);
                          }
                          return true; 
                        });
                      },
          async fetchInfluencer() {
                  try {
                    const response = await axios.get('http://127.0.0.1:5000/influencers',{
                              headers: {
                                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                              },});
                    if (response.data) {
                      this.influencers = response.data;
                      // console.log(this.influencers);
                    }
                  } catch (error) {
                                if (error.response && error.response.status === 401) {
                                  try {
                                    const refreshToken = localStorage.getItem('refresh_token');
                                    if (!refreshToken) {
                                      this.$router.push('/admin-login');
                                    }
                                    await refreshAccessToken(refreshToken); 
                                    
                                    await this.fetchInfluencer();
                                  } catch (refreshError) {
                                    this.$router.push('/login');
                                  }
                                }
                              }
                  
                },
              async  updateCampaign() {
                const formData = new FormData();
                    Object.keys(this.selectedCampaign).forEach((key) => {
                      formData.append(key, this.selectedCampaign[key]);
                    });

                    // Append the selected file if it exists
                    if (this.selectedFile) {
                      formData.append('image', this.selectedFile);
                    }
                try {
                        await axios.put(`http://127.0.0.1:5000/campaign/${this.selectedCampaign.id}`, formData, {
                          headers: {
                            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                          },
                        });

                        this.fetchCampaigns();
                        this.setActiveSection('campaigns');
                      } catch (error) {
                        if (error.response && error.response.status === 401) {
                          try {
                            const refreshToken = localStorage.getItem('refresh_token');
                            if (!refreshToken) {
                              this.$router.push('/admin-login');
                              return;
                            }
                            await this.refreshAccessToken(refreshToken);
                            await this.updateCampaign(); 
                          } catch (refreshError) {
                            this.$router.push('/login');
                          }
                        } else {
                          console.error('Error updating campaign:', error);
                          alert('Failed to update campaign. Please try again.');
                        }
                      }
              },

              async deleteCampaign(campaignId) {
                const userConfirmed = confirm("Are you sure you want to delete this campaign? ");
                    if (!userConfirmed) {
                      return;
                    }
                  try {
                    const response = await axios.delete(`http://127.0.0.1:5000/campaign/${campaignId}`, {
                      headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                      },
                    });
                    alert(response.data.message || "Campaign deleted successfully");
                    
                    await this.fetchCampaigns();
                    this.setActiveSection('campaigns');
                  } catch (error) {
                          if (error.response && error.response.status === 401) {
                            try {
                              const refreshToken = localStorage.getItem('refresh_token');
                              if (!refreshToken) {
                                this.$router.push('/admin-login');
                              }
                              await refreshAccessToken(refreshToken); 
                              
                              await this.deleteCampaign(campaignId);
                            } catch (refreshError) {
                              this.$router.push('/login');
                            }
                          }
                        }
                },

              openEditCampaign(campaign) {
                // console.log('edit pressed')
              this.selectedCampaign = { ...campaign }; 
              this.imagePreviewedit = campaign.image
                    ? this.getImageUrl(campaign.image)
                    : null;

              this.setActiveSection('editcampaigns')
              // console.log(this.showEditModal)
            },
            async fetchFlagCampaigns() {
            try {
              const response = await axios.get('http://127.0.0.1:5000/flagcampaigns',{
                        headers: {
                          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                        },});
              if (response.data) {
                this.flagcampaigns = response.data.campaigns;
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
          async fetchCampaigns() {
            try {
              const response = await axios.get('http://127.0.0.1:5000/campaigns',{
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
      async submitCampaignForm() {
        const formData = new FormData();
        
       
        formData.append('name', this.campaign.name);
        formData.append('description', this.campaign.description);
        formData.append('start_date', this.campaign.start_date);
        formData.append('end_date', this.campaign.end_date);
        formData.append('budget', this.campaign.budget);
        formData.append('visibility', this.campaign.visibility);
        formData.append('goals', this.campaign.goals);
        formData.append('target', this.campaign.target);

        
        if (this.campaign.file) {
          formData.append('image', this.campaign.file);
        }

        try {
          
          const response = await axios.post('http://127.0.0.1:5000/create_campaign', formData, {
      headers: { 
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${localStorage.getItem('access_token')}` 
      },
    });

          if (response.data.message === 'Campaign created successfully') {
            alert('Campaign created successfully!');
            await this.fetchCampaigns();
            window.location.reload();
           
            
            // window.location.reload();
            // this.setActiveSection('campaigns');

            
            // this.resetForm();
          } else {
            alert('Error creating campaign!');
          }
        } catch (error) {
                    if (error.response && error.response.status === 401) {
                      try {
                        const refreshToken = localStorage.getItem('refresh_token');
                        if (!refreshToken) {
                          this.$router.push('/admin-login');
                        }
                        await refreshAccessToken(refreshToken); 
                        
                        await this.submitCampaignForm();
                      } catch (refreshError) {
                        this.$router.push('/login');
                      }
                    }
                  }
      },

    // onFileChange(event) {
    //   this.campaign.file = event.target.files[0];
    // },
    async fetchSponsorDetails() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/dashboard/sponsor_details',{
                  headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                  },});
        if (response.data) {
          this.sponsorDetails = response.data;
        }
      } catch (error) {
                    if (error.response && error.response.status === 401) {
                      try {
                        const refreshToken = localStorage.getItem('refresh_token');
                        if (!refreshToken) {
                          this.$router.push('/admin-login');
                        }
                        await refreshAccessToken(refreshToken); 
                        
                        await this.fetchSponsorDetails();
                      } catch (refreshError) {
                        this.$router.push('/login');
                      }
                    }
                  }
    },
    setActiveSection(section) {
      this.activeSection = section;
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
    reloadPage() {
      window.location.reload();
    }

  },
    
}

</script>

<style scoped>
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