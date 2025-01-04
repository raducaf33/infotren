<template>
    <div class="row">
        <div class="col-md-6 offset-md-3">
            <div>
                <h3>Login</h3>
                <hr />
            </div>
            <form @submit.prevent="login">
                <div class="form-group">
                    <label>Email</label>
                    <input v-model="email" type="text" class="form-control" required />
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input v-model="password" type="password" class="form-control" required />
                </div>
                <div class="my-3">
                    <button type="submit" class="btn btn-primary">Login</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
    data() {
        return {
            email: '',
            password: '',
        };
    },
    methods: {
        async login() {
            try {
                const response = await axios.post('http://127.0.0.1:8000/login/', {
                    email: this.email,
                    password: this.password
                });
                console.log(response.data);

                // Save the token (if applicable)
                localStorage.setItem('access_token', response.data.access);
                localStorage.setItem('refresh_token', response.data.refresh);
                localStorage.setItem('first_name', response.data.first_name);
                localStorage.setItem('last_name', response.data.last_name);

                // Redirect to a blank page or another route
                this.$router.push('/');
            } catch (error) {
                console.error('Login failed:', error);
                // Handle login error (e.g., show error message)
            }
        }
    }
};
</script>
