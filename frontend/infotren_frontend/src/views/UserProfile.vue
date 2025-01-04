<template>

<div class="user-profile">
    <h3>User Profile</h3>
    <div v-if="user">
        <div v-if="!isEditing">
      <p><strong>Name:</strong> {{ user.first_name }} {{ user.last_name }}</p>
      <p><strong>Username:</strong> {{ user.username }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>Phone:</strong> {{ user.phone }}</p>
      <button @click="isEditing = true" class="btn btn-primary">Edit Profile</button>
      </div>
      <div v-else>
        <form @submit.prevent="updateProfile">
          <div class="form-group">
            <label for="first_name">First Name</label>
            <input id="first_name" v-model="editData.first_name" class="form-control" />
          </div>
          <div class="form-group">
            <label for="last_name">Last Name</label>
            <input id="last_name" v-model="editData.last_name" class="form-control" />
          </div>
          <div class="form-group">
            <label for="username">Username</label>
            <input id="username" v-model="editData.username" class="form-control" />
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input id="email" v-model="editData.email" class="form-control" />
          </div>
          <div class="form-group">
            <label for="phone">Phone</label>
            <input id="phone" v-model="editData.phone" class="form-control" />
          </div>
          <button type="submit" class="btn btn-success">Save Changes</button>
          <button type="button" @click="isEditing = false" class="btn btn-secondary">Cancel</button>
        </form>
      </div>
      <button @click="deleteAccount" class="btn btn-danger mt-3">Delete Account</button>
    </div>
    <p v-else>Loading user data...</p>
  </div>

    <div class="tickets-list">
            <h3>Purchased Tickets:</h3>
            <ul v-if="tickets.length">
            <li v-for="ticket in tickets" :key="ticket.TicketId" class="ticket-item">
            <p><strong>Train:</strong> {{ ticket.TrainId }}</p>
            <p><strong>Category:</strong> {{ ticket.TicketCategory }}</p>
            <p><strong>Price:</strong> {{ ticket.Price }} RON</p>
            <p><strong>Booking Time:</strong> {{ new Date(ticket.BookingTime).toLocaleString() }}</p>
            <button @click="deleteTicket(ticket.TicketId)" class="btn btn-danger">Delete</button>
            </li>
            </ul>
            <p v-else>No tickets purchased yet.</p>
</div>

<h3>Travel History:</h3>
        <ul v-if="history.length">
            <li v-for="ticket in history" :key="ticket.TicketId" class="ticket-item">
                <p><strong>Train:</strong> {{ ticket.TrainId }}</p>
                <p><strong>Category:</strong> {{ ticket.TicketCategory }}</p>
                <p><strong>Price:</strong> {{ ticket.Price }} RON</p>
                <p><strong>Booking Time:</strong> {{ new Date(ticket.BookingTime).toLocaleString() }}</p>
            </li>
        </ul>
        <p v-else>No travel history available yet.</p>

        
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            tickets: [], // Active tickets
            history: [], // Travel history
            user: null,
            isEditing: false,
            editData: {
        first_name: "",
        last_name: "",
        username: "",
        email: "",
        phone: "",
      },
        };
    },
    methods: {
        async fetchTickets() {
            try {
                const accessToken = localStorage.getItem('access_token');
                if (!accessToken) {
                    console.error("Access token is missing. Please log in.");
                    return;
                }

                // Call the tickets-history API endpoint
                const response = await axios.get('http://127.0.0.1:8000/tickets-history/', {
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                    },
                });

                if (response.data.success) {
                    this.tickets = response.data.active;
                    this.history = response.data.history;
                } else {
                    alert('Failed to fetch travel history.');
                }
            } catch (error) {
                console.error('Error fetching travel history:', error);
                alert('Could not load travel history. Please try again later.');
            }
        },
        async fetchUserProfile() {
        try {
            const accessToken = localStorage.getItem('access_token');
            if (!accessToken) {
                console.error("Access token is missing. Please log in.");
                return;
            }

            const response = await axios.get('http://127.0.0.1:8000/user-information/', {
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            });

            if (response.data.success) {
                this.user = response.data.user;
                this.editData= { ...this.user};
            } else {
                console.error("Failed to fetch user profile:", response.data.message);
            }
        } catch (error) {
            console.error("Error fetching user profile:", error);
        }
    },async updateProfile() {
      try {
        const accessToken = localStorage.getItem("access_token");
        const response = await axios.put(
          "http://127.0.0.1:8000/update-user-information/",
          this.editData,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        if (response.data.success) {
          this.user = { ...this.editData }; // Update displayed user data
          this.isEditing = false;
          alert("Profile updated successfully!");
        } else {
          alert("Failed to update profile.");
        }
      } catch (error) {
        console.error("Error updating profile:", error);
        alert("An error occurred while updating your profile.");
      }
    },
    async deleteAccount() {
      if (confirm("Are you sure you want to delete your account? This action cannot be undone.")) {
        try {
          const accessToken = localStorage.getItem("access_token");
          await axios.delete("http://127.0.0.1:8000/delete-account/", {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
          alert("Account deleted successfully.");
          localStorage.clear();
          this.$router.push("/signup"); // Redirect to signup page
        } catch (error) {
          console.error("Error deleting account:", error);
          alert("An error occurred while deleting your account.");
        }
      }
    },
    async deleteTicket(ticketId) {
      try {
        const accessToken = localStorage.getItem('access_token'); // Ensure you have the access token
        if (!accessToken) {
           console.error("Access token is missing. Please log in.");
           this.searchResults = { routes: [], message: "You need to log in." };
           return;
        }
        // Trimitere cerere DELETE pentru ștergerea biletului
        const response = await axios.delete(`http://127.0.0.1:8000/delete-tickets/${ticketId}/`,{
            headers:{
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
        });
        
        // Verifică dacă răspunsul a fost OK
        if (response.status === 200) {
          // Șterge biletul din lista locală
          this.tickets = this.tickets.filter(ticket => ticket.id !== ticketId);
          alert('Biletul a fost șters cu succes!');
        }
      } catch (error) {
        console.error('Error deleting ticket:', error);
        alert('A apărut o eroare la ștergerea biletului.');
      }
    }
  

    },
    mounted(){
        this.fetchTickets();
        this.fetchUserProfile();
        
    },

};

</script>

<style>
.tickets-list{

    margin:20px;
}
.ticket-item{

    padding:10px;
    border: 1px solid #ccc;
    
}
</style>