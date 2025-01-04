<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">Navbar</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
  
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li v-if="!isLoggedIn" class="nav-item">
          <router-link class="nav-link" to="/">Home</router-link>
        </li>
        <li v-if="!isLoggedIn" class="nav-item">
          <router-link class="nav-link" to="/login">Login</router-link>
        </li>
        <li v-if="!isLoggedIn" class="nav-item">
          <router-link class="nav-link" to="/signup">Sign Up</router-link>
        </li>
        <li v-if="isLoggedIn" class="nav-item">
          <span class="nav-link">Hello, {{ fullName }}</span>
        </li>
        <li v-if="isLoggedIn" class="nav-item">
          <button class="btn btn-danger" @click="logout">Logout</button>
        </li>
      </ul>
      <form class="form-inline my-2 my-lg-0">
        <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
      </form>
    </div>
  </nav>
  </template>
  
  <script>
  export default {
    data() {
      return {
        firstName: '',
        lastName: ''
      };
    },
    computed: {
      isLoggedIn() {
        return !!localStorage.getItem('access_token');
      },
      fullName() {
        return `${this.firstName} ${this.lastName}`;
      }
    },
    methods: {
      updateName() {
        this.firstName = localStorage.getItem('first_name') || '';
        this.lastName = localStorage.getItem('last_name') || '';
      },
      logout() {
        // Clear all user-related data from localStorage
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('first_name');
        localStorage.removeItem('last_name');
        
        // Redirect to the login page or home page
        this.$router.push('/login');
      }
    },
    mounted() {
      if (this.isLoggedIn) {
        this.updateName();
      }
    },
    watch: {
    isLoggedIn(newValue) {
      if (newValue) {
        this.updateName();
      } else {
        // Optionally clear user info when logged out
        this.firstName = '';
        this.lastName = '';
      }
    }
  }
}
  </script>
  