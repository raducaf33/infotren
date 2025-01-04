<template>
  <div class="payment-form">
    <h3>Finalizează Plata</h3>
    <form @submit.prevent="submitPayment">
      <div class="form-group">
        <label for="cardNumber">Număr Card</label>
        <input v-model="paymentInfo.cardNumber" id="cardNumber" type="text" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="expiryDate">Data Expirării</label>
        <input v-model="paymentInfo.expiryDate" id="expiryDate" type="date" class="form-control" placeholder="MM/YY" required />
      </div>
      <div class="form-group">
        <label for="cvv">CVV</label>
        <input v-model="paymentInfo.cvv" id="cvv" type="text" class="form-control" required />
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
  props: {
    paymentInfo: Object// Accept paymentInfo as a prop from the parent
  },
  methods: {
    async submitPayment() {
      try {
        // Trimitem datele de plată împreună cu biletele
        const paymentResponse = await axios.post('http://127.0.0.1:8000/fake-payment/', {
          card_number: this.paymentInfo.cardNumber,
          expiry_date: this.paymentInfo.expiryDate,
          cvv: this.paymentInfo.cvv
        }, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json',
          },
        });

        if (paymentResponse.data.success) {
          alert('Plata a fost procesată cu succes și biletele au fost rezervate!');
          // Poți reseta formularul sau redirecționa utilizatorul
        } else {
          alert('Plata a eșuat: ' + paymentResponse.data.message);
        }
      } catch (error) {
        console.error("Error processing payment:", error);
        alert('A apărut o eroare la procesarea plății.');
      }
    },
  },
};
</script>
