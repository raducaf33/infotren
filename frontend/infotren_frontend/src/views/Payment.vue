<template>
    <div class="payment-form">
      <h3>Finalizează Plata</h3>
      <form @submit.prevent="submitPayment">
        <div class="form-group">
          <label for="cardNumber">Număr Card</label>
          <input v-model="cardNumber" id="cardNumber" type="text" class="form-control" required />
        </div>
        <div class="form-group">
          <label for="expiryDate">Data Expirării</label>
          <input v-model="expiryDate" id="expiryDate" type="text" class="form-control" placeholder="MM/YY" required />
        </div>
        <div class="form-group">
          <label for="cvv">CVV</label>
          <input v-model="cvv" id="cvv" type="text" class="form-control" required />
        </div>
        <div class="my-3">
          <button type="submit" class="btn btn-primary">Plătește</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        cardNumber: '',
        expiryDate: '',
        cvv: ''
      };
    },
    methods: {
      async submitPayment() {
        // Simulăm plata
        try {
          const response = await axios.post('http://127.0.0.1:8000/fake-payment/', {
            card_number: this.cardNumber,
            expiry_date: this.expiryDate,
            cvv: this.cvv
          });
  
          if (response.data.success) {
            alert('Plata a fost efectuată cu succes!');
            // Redirect după succes
            this.$router.push('/booking-confirmation');
          } else {
            alert('Plata a eșuat. Încercați din nou.');
          }
        } catch (error) {
          console.error("Eroare la efectuarea plății:", error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* Adaugă stiluri pentru formularul de plată aici dacă este necesar */
  </style>
  