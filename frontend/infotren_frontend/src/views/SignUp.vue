<template>
    <div class="row">
      <div class="col-md-6 offset-md-3">
        <div>
          <div>
            <h3>Sign Up</h3>
            <hr />
          </div>
          <form @submit.prevent="register">
            <div class="form-group">
              <label>First Name</label>
              <input v-model="first_name" type="text" class="form-control" />
            </div>
            <div class="form-group">
              <label>Last Name</label>
              <input v-model="last_name" type="text" class="form-control" />
            </div>
            <div class="form-group">
              <label>Username</label>
              <input v-model="username" type="text" class="form-control" />
            </div>
            <div class="form-group">
              <label>Email</label>
              <input v-model="email" type="text" class="form-control" />
            </div>
            <div class="form-group">
              <label>Phone</label>
              <input v-model="phone" type="text" class="form-control" />
            </div>
            <div class="form-group">
              <label>Password</label>
              <input v-model="password" type="password" class="form-control" />
            </div>
            <div class="form-group">
              <label>Confirm Password</label>
              <input v-model="confirm_password" type="password" class="form-control" />
            </div>
            <div class="my-3">
              <button type="submit" class="btn btn-primary">Sign Up</button>
            </div>
          </form>
          <div v-if="error" class="alert alert-danger">{{ error }}</div>
          <div v-if="success" class="alert alert-success">User registered successfully!</div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import  variables  from '../api/variables';
  
  export default {
    data() {
      return {
        first_name: '',
        last_name: '',
        username: '',
        email: '',
        phone: '',
        password: '',
        confirm_password: '',
        error: null,
        success: false
      };
    },
    methods: {
      async register() {
        this.error = null;
        this.success = false;
  
        // Basic client-side validation
        if (!this.first_name || !this.last_name || !this.username || !this.email || !this.phone || !this.password || !this.confirm_password) {
          this.error = 'All fields are required.';
          return;
        }
        if (this.password !== this.confirm_password) {
          this.error = 'Passwords do not match.';
          return;
        }
  
        try {
                  const response = await axios.post(`${variables.API_URL}register`, {
            Username: this.username,
            password: this.password,
            confirm_password: this.confirm_password,
            Firstname: this.first_name,
            Lastname: this.last_name,
            Phone: this.phone,
            Email: this.email
            });

          this.success = true;
          this.error = null;
          console.log("User registered successfully!");
          this.resetForm();
        } catch (error) {
          if (error.response && error.response.data) {
            this.error = error.response.data.non_field_errors || 'Registration failed';
          } else {
            this.error = 'An error occurred. Please try again.';
          }
          console.error(error);
        }
      },
      resetForm() {
        this.first_name = '';
        this.last_name = '';
        this.username = '';
        this.email = '';
        this.phone = '';
        this.password = '';
        this.confirm_password = '';
      }
    }
  };
  </script>
  
  <style scoped>
  /* Optional: Add your styles here */
  </style>
  