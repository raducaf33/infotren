<template>
  <div class="row">
    <div class="col-md-6 offset-md-3">
      <h3>Buy Tickets</h3>
      <hr />
      <div v-if="!trainSelected">
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
            <div
              v-for="routeInfo in searchResults.routes"
              :key="routeInfo.route.RouteId"
              class="route-box"
            >
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

      <!-- Ticket Selection Component -->
      <div v-if="trainSelected && !seatSelectionStarted">
        <h4>Select Ticket Type</h4>
        <div v-for="(count, type) in ticketTypes" :key="type" class="ticket-type-box">
          <p>{{ type }}: {{ count }}</p>
          <button class="btn btn-success btn-sm" @click="incrementTicket(type)">+</button>
          <button class="btn btn-danger btn-sm" @click="decrementTicket(type)" :disabled="count === 0">-</button>
        </div>
        <div class="my-3">
          <button class="btn btn-primary" @click="proceedWithBooking">Proceed with Booking</button>
        </div>
      </div>

      <div v-if="seatSelectionStarted && availableSeats.length > 0">
        <h4>Select Your Seats</h4>
        <div class="seat-grid">
          <div
            v-for="seat in availableSeats"
            :key="seat.SeatId"
            class="seat"
            :class="{ booked: seat.IsBooked, selected: selectedSeats.includes(seat.SeatId) }"
            @click="selectSeat(seat)"
            :disabled="seat.IsBooked"
          >
            {{ seat.SeatNumber }}
          </div>
        </div>
        <div class="my-3">
          <button class="btn btn-primary" @click="confirmBooking">Confirm Booking</button>
        </div>
      </div>

      <!-- Payment Component -->
      <Payment
        v-if="paymentStep"
        :paymentInfo="paymentInfo"
        @payment-processed="handlePaymentProcessed"
      />

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Payment from './Payment.vue'; // Importă componenta Payment

export default {
  components: {
    Payment, // Include componenta Payment
  },
  data() {
    return {
      departurePlace: '',
      arrivalPlace: '',
      date: '',
      searchResults: { routes: [], message: '' },
      message: '',
      searchCompleted: false,
      trainSelected: false,
      ticketTypes: {
        Adult: 0,
        Student: 0,
        Pupil: 0,
        Senior: 0,
      },
      selectedTrain: null,
      availableSeats: [],
      seatSelectionStarted: false,
      selectedSeats: [],
      
      paymentStep: false, // New property to control visibility of the payment section
      paymentInfo: { // Store payment details
        cardNumber: '',
        expiryDate: '',
        cvv: ''
      },
      tickets: [],
      paymentMessage: '' // Mesajul pentru succesul sau eșecul plății
    };
  },
  methods: {
    async searchTickets() {
      
      try {
        const accessToken = localStorage.getItem('access_token'); // Ensure you have the access token
        if (!accessToken) {
           console.error("Access token is missing. Please log in.");
           this.searchResults = { routes: [], message: "You need to log in." };
           return;
        }
        const response = await axios.post('http://127.0.0.1:8000/search-tickets/', {
          departure_place: this.departurePlace,
          arrival_place: this.arrivalPlace,
          date: this.date,
          
        },{
            headers: {
                'Authorization': `Bearer ${accessToken}`, // Attach the access token
                'Content-Type': 'application/json'
            }
      });

        console.log(response.data);

        if (Array.isArray(response.data)) {
          this.searchResults = { routes: response.data, message: '' };
        } else {
          this.searchResults = { routes: [], message: 'No routes found' };
        }
        this.searchCompleted = true;
      } catch (error) {
        console.error('Search failed:', error);
        this.searchResults = { routes: [], message: 'Search failed. Please try again.' };
        this.searchCompleted = true;
      }
    },
    selectTrain(train) {
      this.selectedTrain = train;
      this.trainSelected = true;
    },
    incrementTicket(type) {
      this.ticketTypes[type]++;
    },
    decrementTicket(type) {
      if (this.ticketTypes[type] > 0) {
        this.ticketTypes[type]--;
      }
    },
    async proceedWithBooking() {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/seats?trainId=${this.selectedTrain.TrainId}`);
        this.availableSeats = response.data;
        this.seatSelectionStarted = true;
      } catch (error) {
        console.error("Error fetching seats:", error);
        alert("Could not load available seats. Please try again.");
      }
    },
    selectSeat(seat) {
      const totalTickets = this.ticketTypes.Adult + this.ticketTypes.Student + this.ticketTypes.Pupil + this.ticketTypes.Senior;

      if (this.selectedSeats.includes(seat.SeatId)) {
        this.selectedSeats = this.selectedSeats.filter(id => id !== seat.SeatId);
      } else {
        if (this.selectedSeats.length < totalTickets) {
          this.selectedSeats.push(seat.SeatId);
        } else {
          alert(`You can only select ${totalTickets} seats based on your ticket selection.`);
        }
      }
    },
    async confirmBooking() {
  // Verificați dacă utilizatorul este autentificat
  const accessToken = localStorage.getItem('access_token'); // Asigurați-vă că aveți acces token-ul
  if (!accessToken) {
    alert("You must be logged in to confirm a booking.");
    return; // Prevenirea execuției ulterioare dacă nu este autentificat
  }

  // Pregătirea detaliilor de rezervare
  const bookingDetails = {
    train_id: this.selectedTrain.TrainId, // Asigurați-vă că folosiți cheia corectă
    seat_ids: this.selectedSeats, // Asigurați-vă că seat_ids este corect
    ticket_types: this.ticketTypes // Asigurați-vă că ticket_types este în formatul corect
  };

  try {
    // Trimiterea cererii pentru a confirma rezervarea
    const response = await axios.post('http://127.0.0.1:8000/confirm-booking/', bookingDetails, {
      headers: {
        'Authorization': `Bearer ${accessToken}`, // Adăugați token-ul de acces
        'Content-Type': 'application/json' // Opțional, dar recomandat
      },
    });

    // Gestionarea răspunsului de la backend
    if (response.data.success) {
      // Afișează secțiunea de plată dacă rezervarea este confirmată
      this.paymentStep = true; // Setează paymentStep la true pentru a continua
    } else {
      // Dacă rezervarea nu reușește, afișează mesajul corespunzător
      alert(response.data.message || 'Failed to confirm booking. Please try again.');
    }
  } catch (error) {
    // Capturează orice eroare care apare în timpul procesului de rezervare
    console.error('Booking confirmation failed:', error);
    alert('Failed to confirm booking. Please try again.');
  }
},

  handlePaymentProcessed(paymentResult) {
      if (paymentResult.success) {
        alert('Payment successful! Your tickets are confirmed.');
      } else {
        alert('Payment failed: ' + paymentResult.message);
      }
      this.paymentStep = false; // Hide the payment form after processing
    },
  },
};
</script>

<style scoped>
.seat-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 5px;
}

.seat {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}

.seat.booked {
  background-color: #ffcccc;
  cursor: not-allowed;
}

.seat.selected {
  background-color: #99ff99;
}
</style>
