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
          <div v-for="routeInfo in searchResults.routes" :key="routeInfo.route.RouteId">
            <p>Date: {{ routeInfo.route.Date }} - From: {{ routeInfo.route.StartStation }} To: {{ routeInfo.route.EndStation }}</p>
            <p>Distance: {{ routeInfo.route.Distance }} km</p>
            <p>Departure Time: {{ routeInfo.route.DepartureTime }} - Arrival Time: {{ routeInfo.route.ArrivalTime }}</p>
            <h5>Trains on this Route:</h5>
            <ul>
              <li v-for="train in routeInfo.trains" :key="train.TrainId">
                Train Number: {{ train.TrainNumber }} - Company: {{ train.Company }}
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
  /* Add custom styles if needed */
  </style>
  