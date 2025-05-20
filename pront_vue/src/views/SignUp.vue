<template>
    <div class="page-sing-up">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Sign Up</h1>

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

                    <div class="field">
                        <label>Repeat Password</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password2">
                        </div>
                    </div>

                    <div style="height: 10px;"></div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>

                    <div style="height: 10px;"></div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-dark">Sign up</button>
                        </div>
                    </div>

                    <div style="height: 20px;"></div>

                    Or <router-link to="/log-in">click here</router-link> to log in!
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { toast } from 'bulma-toast';
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';

const store = useStore();
const username = ref('');
const password = ref('');
const password2 = ref('');
const errors = ref([]);
const router = useRouter();

document.title = 'store - sign up';

function submitForm() {
    errors.value = [];
    if (username.value === '') {
        errors.value.push('The username is missing');
    }

    if (password.value === '') {
        errors.value.push('The password is too short');
    }

    if (password.value !== password2.value) {
        errors.value.push('The passwords don\'t match');
    }

    if (!errors.value.length) {
        const formData = {
            username: username.value,
            password: password.value
        };

        axios
            .post("/api/v1/users/", formData)
            .then(response => {
                toast({
                    message: 'Account created, please log in!',
                    type: 'is-success',
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: 'bottom-right',
                });

                router.push('/log-in');
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
}

onMounted(() => {
    store.commit('setLoading', true); // 开始加载
    setTimeout(() => {
        store.commit('setLoading', false); // 确保加载状态被关闭
    }, 100); // 模拟异步操作
});
</script>