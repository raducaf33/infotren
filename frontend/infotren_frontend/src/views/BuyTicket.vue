<template>
    <div class="row">
      <div class="col-md-6 offset-md-3">
        <h3>Buy Tickets</h3>
        <hr />
        <form @submit.prevent="searchTickets">
          <div class="form-group">
            <label>Departure Place</label>
            <input
              v-model="departurePlace"
              type="text"
              class="form-control"
              required
            />
          </div>
          <div class="form-group">
            <label>Arrival Place</label>
            <input
              v-model="arrivalPlace"
              type="text"
              class="form-control"
              required
            />
          </div>
          <div class="form-group">
            <label>Date</label>
            <input
              v-model="date"
              type="date"
              class="form-control"
              required
            />
          </div>
          <div class="my-3">
            <button type="submit" class="btn btn-primary">Search</button>
          </div>
        </form>
 <!-- Display Search Results -->
 <div v-if="searchCompleted">
        <h4>Available Routes:</h4>
        <div v-if="searchResults.routes.length">
          <div v-for="routeInfo in searchResults.routes" :key="routeInfo.route.RouteId" class="route-box">
            <p><strong>Date:</strong> {{ routeInfo.route.Date }} - From: {{ routeInfo.route.StartStation }} To: {{ routeInfo.route.EndStation }}</p>
            <p><strong>Distance:</strong> {{ routeInfo.route.Distance }} km</p>
            <p><strong>Departure Time:</strong> {{ routeInfo.route.DepartureTime }} - Arrival Time: {{ routeInfo.route.ArrivalTime }}</p>
            <h5>Trains on this Route:</h5>
            <ul>
              <li v-for="train in routeInfo.trains" :key="train.TrainId">
                Train Number: {{ train.TrainNumber }} - Company: {{ train.Company }}
                <button class="btn btn-secondary btn-sm ml-2" @click="selectTrain(train)">Select</button>
              </li>
            </ul>
          </div>
        </div>
        <div v-if="!searchResults.routes.length && message">
          <p>{{ message }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        departurePlace: '',
        arrivalPlace: '',
        date: '',
        searchResults: { routes: [], message: '' },  // To store search results
        message: '',
        searchCompleted: false, // Track if the search is completed        // To store status messages
      };
    },
    methods: {
    async searchTickets() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/search-tickets/', {
          departure_place: this.departurePlace,
          arrival_place: this.arrivalPlace,
          date: this.date,
        });

        console.log(response.data); // Debug output

          // Update the structure to match what the template expects
      if (Array.isArray(response.data)) {
        this.searchResults = { routes: response.data, message: '' };
      } else {
        this.searchResults = { routes: [], message: 'No routes found' };
      }
        this.searchCompleted = true; // Set search as completed
      } catch (error) {
        console.error('Search failed:', error);
        this.searchResults = { routes: [], message: 'Search failed. Please try again.' };
        this.searchCompleted = true; // Ensure searchCompleted is true even on error
      }
    },
  },
};
</script>
  
<style scoped>
.route-box {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  background-color: #f9f9f9;
}

.route-box p {
  margin: 0;
  padding: 4px 0;
}

.route-box ul {
  list-style-type: none;
  padding: 0;
}

.route-box li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
}

.route-box .btn {
  margin-left: 8px;
}
</style>
  