<template>
    <div class="page-log-in">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Log In</h1>

                <div style="height: 20px;"></div>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Username</label>
                        <div class="control">
                            <input type="text" class="input" v-model="username">
                        </div>
                    </div>

                    <div style="height: 10px;"></div>

                    <div class="field">
                        <label>Password</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password">
                        </div>
                    </div>

                    <div style="height: 10px;"></div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>

                    <div style="height: 10px;"></div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-dark">Log in</button>
                        </div>
                    </div>

                    <div style="height: 20px;"></div>

                    Or <router-link to="/sign-up">click here</router-link> to sign up!
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from  'vue';
import { useStore } from 'vuex';
import { useRoute, useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const errors = ref([]);
const store = useStore();
const route = useRoute();
const router = useRouter();

document.title = 'store - log in';

async function submitForm(){
    axios.defaults.headers.common['Authorization'] = ""

    localStorage.removeItem('token')

    const formData = {
        username: username.value,
        password: password.value,
    }
    await axios
        .post("/api/v1/token/login/", formData)
        .then(response => {
                const token = response.data.auth_token;
                
                store.commit('setToken',token);

                axios.defaults.headers.common['Authorization'] = 'Token' + token;

                localStorage.setItem("token", token);
                localStorage.setItem('authToken', token);
                const toPath = route.query.to || '/cart'

                router.push(toPath)
            })
            .catch(error => {
                if (error.response) {
                    for (const property in error.response.data) {
                        errors.value.push(`${property}: ${error.response.data[property]}`);
                    }
                    console.log(JSON.stringify(error.response.data));
                } else if (error.message) {
                    errors.value.push('Something went wrong, Please try again');
                    console.log(JSON.stringify(error));
                }
            }); 
}
</script>