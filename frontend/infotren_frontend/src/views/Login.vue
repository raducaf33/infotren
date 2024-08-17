<template>
    <div class="row">
        <div class="col-md-6 offset-md-3">
            <div>
                <h3>Login</h3>
                <hr />
            </div>
            <form @submit.prevent="login">
                <div class="form-group">
                    <label>Username</label>
                    <input v-model="username" type="text" class="form-control" required />
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
            username: '',
            password: '',
        };
    },
    methods: {
        async login() {
            try {
                const response = await axios.post('http://127.0.0.1:8000/login/', {
                    username: this.username,
                    password: this.password
                });

                // Save the token (if applicable)
                localStorage.setItem('token', response.data.access);

                // Redirect to a blank page or another route
                this.$router.push('/blank-page');
            } catch (error) {
                console.error('Login failed:', error);
                // Handle login error (e.g., show error message)
            }
        }
    }
};
</script>
