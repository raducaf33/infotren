<template>
  <nav class="navbar navbar-expand-lg fixed-top navbar-scroll navbar-light bg-white">
    <div class="container-fluid">
      <!-- Navbar brand -->
      <a class="navbar-brand">
        <strong >InfoTrain</strong>
      </a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
      <i class="fas fa-bars"></i>
    </button>
  
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link class="nav-link" to="/">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/about">About</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/contact">Contact</router-link>
        </li>
        <li v-if="!authState.isLoggedIn" class="nav-item">
          <router-link class="nav-link" to="/login">Login</router-link>
        </li>
        <li v-if="!authState.isLoggedIn" class="nav-item">
          <router-link class="nav-link" to="/signup">Sign Up</router-link>
        </li>
        <li v-if="authState.isLoggedIn" class="nav-item dropdown">
            <a
              href="#"
              class="nav-link dropdown-toggle"
              id="userDropdown"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Hello, {{ authState.firstName }} {{ authState.lastName }}
            </a>
            <ul class="dropdown-menu" aria-labelledby="userDropdown">
              <li>
                <router-link class="dropdown-item" to="/user-profile">My Profile</router-link>
              </li>
              <li>
                <a class="dropdown-item" href="#" @click="logout">Logout</a>
              </li>

            </ul>
      </li>
      <li class="nav-item">
          <router-link class="nav-link" to="/settings">Settings</router-link>
        </li>
      </ul>
    </div>
  </div>
  </nav>



  </template>
  
  <script>
  import { inject } from 'vue';
  
  export default {
    setup() {
      const authState = inject('authState'); // This comes from the parent (App.vue)
  
      const logout = () => {
        // Clear the localStorage and update the authState
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('first_name');
        localStorage.removeItem('last_name');
        authState.isLoggedIn = false;
        authState.firstName = '';
        authState.lastName = '';
        this.$router.push('/login');
      };
  
      return { authState, logout };
    }
  };
  </script>

  <style>
@media (max-width: 991px) {
  .navbar-scroll {
    background-color: #fff;
  }
     
        
}
.navbar ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 1rem;
}
.navbar .dropdown {
  position: relative;
}
.navbar .dropdown-menu {
  display: none;
  position: absolute;
  top: 100%;
  background-color: white;
  border: 1px solid #ccc;
  list-style: none;
  padding: 0.5rem 0;
}
.navbar .dropdown:hover .dropdown-menu {
  display: block;
}

.navbar-brand {
  letter-spacing: 3px;
  font-size: 2rem;
  font-weight: 500;
}

.navbar-brand strong{
  color: black;
}


.navbar-scroll .navbar-brand,
.navbar-scroll .nav-link,
.navbar-scroll .fa-bars {
  color: #fff;
}

.navbar-scroll {
  box-shadow: none;
}

.navbar-scrolled {
  box-shadow: 0 10px 20px 0 rgba(0, 0, 0, 0.05);
}

.navbar-scrolled .navbar-brand,
.navbar-scrolled .nav-link,
.navbar-scrolled .fa-bars {
  color: #4f4f4f;
}

.navbar-scrolled {
  background-color: #fff;
}

@media (max-width: 450px) {
  #intro {
    height: 950px !important;
  }
}

@media (min-width: 550px) and (max-width: 750px) {
  #intro {
    height: 1100px !important;
  }
}

@media (min-width: 800px) and (max-width: 990px) {
  #intro {
    height: 600px !important;
  }
}

.display-1 {
  font-weight: 500 !important;
  letter-spacing: 40px;
}

@media (min-width: 1600px) {
  .display-1 {
    font-size: 10rem;
  }
}
  </style>
  