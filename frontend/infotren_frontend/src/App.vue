<template>
  <div class="app-container">
    <!-- Fixed Navbar -->
    <Navbar class="navbar-fixed" />

    <!-- Main content area, with padding to avoid overlap with navbar and footer -->
    <div class="main-content">
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <router-view></router-view>
          </div>
        </div>
      </div>
    </div>

    <!-- Fixed Footer -->
    <Footer class="footer-fixed" />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import { reactive, watch, onMounted, provide } from 'vue';

export default {
  name: 'App',
  components: { Navbar, Footer },
  setup() {
    const authState = reactive({
      isLoggedIn: !!localStorage.getItem('access_token'),
      firstName: localStorage.getItem('first_name') || '',
      lastName: localStorage.getItem('last_name') || ''
    });

    // Watch for changes in localStorage and update reactive state
    watch(() => localStorage.getItem('access_token'), (newValue) => {
      authState.isLoggedIn = !!newValue;
    });

    watch(() => localStorage.getItem('first_name'), (newValue) => {
      authState.firstName = newValue;
    });

    watch(() => localStorage.getItem('last_name'), (newValue) => {
      authState.lastName = newValue;
    });

    // Provide authState so that child components can access it
    provide('authState', authState);

    return { authState };
  }
};
</script>

<style>
/* Structure layout with Flexbox so that the content doesn't overlap */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* Ensure the app takes up the full viewport height */
}

/* Navbar should be fixed at the top */
.navbar-fixed {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000; /* Ensure it stays above other content */
  height: 70px; /* Adjust height based on your navbar */
  background-color: white; /* Optional: ensure background color matches */
}

/* Footer should be fixed at the bottom */
.footer-fixed {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 20px; /* Adjust height based on your footer */
  background-color: white; /* Optional: ensure background color matches */
  z-index: 1000;
}

/* Main content should be below the navbar and above the footer */
.main-content {
  flex-grow: 1; /* Allows the content to grow between navbar and footer */
  padding-top: 70px; /* Match this to the navbar height */
  padding-bottom: 50px; /* Match this to the footer height */
  margin-top: 70px; /* Offset by the navbar height */
  margin-bottom: 50px; /* Offset by the footer height */
  overflow-y: auto; /* Allows scrolling if content is taller than the viewport */
}
</style>
