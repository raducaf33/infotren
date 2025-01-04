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
              <label>Username</label>
              <input v-model="username" type="text" class="form-control" />
            </div>
            <div class="form-group">
              <label>First Name</label>
              <input v-model="first_name" type="text" class="form-control" />
            </div>
            <div class="form-group">
              <label>Last Name</label>
              <input v-model="last_name" type="text" class="form-control" />
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
        username: '',  
        first_name: '',
        last_name: '',
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
        if (!this.username || !this.first_name || !this.last_name || !this.email || !this.phone || !this.password || !this.confirm_password) {
          this.error = 'All fields are required.';
          return;
        }

        // Check if username and email are unique
         await this.checkUsernameAndEmail();

        if (this.usernameTaken) {
          this.error = 'Username is already taken.';
          return;
        }

        if (this.emailTaken) {
          this.error = 'Email is already taken.';
          return;
        }

        if (this.phone.length < 13) {
          this.error = 'Phone cannot be less than 13 characters';
          return;
        }
        
        if(this.password.length < 6 ){
          this.error ='Password should be at least 6 characters long.'
          return;
        }

        let hasUpperCase = false;
        let hasNumber = false;
        let hasSymbol = false;
        const symbols = "@$!%*?&";

        for (let char of this.password) {
          if (char >= 'A' && char <= 'Z') {
              hasUpperCase = true;
          } else if (char >= '0' && char <= '9') {
              hasNumber = true;
          } else if (symbols.includes(char)) {
              hasSymbol = true;
          }
        }

        if (!hasUpperCase) {
            this.error = 'Password must contain at least one uppercase letter.';
            return;
        }

        if (!hasNumber) {
            this.error = 'Password must contain at least one number.';
            return;
        }

        if (!hasSymbol) {
            this.error = 'Password must contain at least one special symbol (@, $, !, %, *, ?, &).';
            return;
        }



        if (this.password !== this.confirm_password) {
          this.error = 'Passwords do not match.';
          return;
        }
        
  
        try {
          const response = await axios.post(`${variables.API_URL}register`, {
            username: this.username,
            first_name: this.first_name,
            last_name: this.last_name,
            email: this.email,
            phone: this.phone,
            password: this.password,
            confirm_password: this.confirm_password
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
      async checkUsernameAndEmail() {
      try {
        const usernameResponse = await axios.get(`${variables.API_URL}check-username/`, {
          params: { username: this.username }
        });
        this.usernameTaken = usernameResponse.data.taken;
        
        const emailResponse = await axios.get(`${variables.API_URL}check-email/`, {
          params: { email: this.email }
        });
        this.emailTaken = emailResponse.data.taken;
      } catch (error) {
        console.error("Error checking username and email:", error);
      }
    },
      resetForm() {
        this.username = '';
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
  