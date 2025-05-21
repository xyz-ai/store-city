import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

axios.defaults.baseURL = import.env.VITE_API_BASE_URL
createApp(App).use(store).use(router, axios).mount('#app')
store.dispatch('initializeCart');
