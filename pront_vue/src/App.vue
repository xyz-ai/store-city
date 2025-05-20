<template>
  <div id="store_app">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item">
          <strong>Store</strong>
        </router-link>
        <a
          class="navbar-burger burger"
          role="button"
          aria-label="menu"
          :aria-expanded="showmobilemenu"
          @click="toggleMobileMenu"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div
        class="navbar-menu"
        id="navbar-menu"
        :class="{ 'is-active': showmobilemenu }"
      >
        <div class="navbar-start">
          <div class="navbar-item">
            <form method="get" action="/search">
              <div class="field has-addons">
                <div class="control">
                  <input
                    class="input"
                    type="text"
                    name="query"
                    placeholder="Search for products"
                    required
                  />
                </div>
                <div class="control">
                  <button type="submit " class="button is-success">
                    <span class="icon">
                      <i class="fas fa-search"></i>
                    </span>
                </button>
                </div>
              </div>
            </form>
          </div>
        </div>
        <div class="navbar-end">
          <router-link to="/summer" class="navbar-item">Summer</router-link>
          <router-link to="/winter" class="navbar-item">Winter</router-link>
          <div class="navbar-item">
            <div class="buttons">
              <template v-if="$store.state.isAuthenticated">
                <router-link to="/my-account" class="button is-light">My account</router-link>
              </template>

              <template v-else>
              <router-link to="/log-in" class="button is-light">Log In</router-link>
              <router-link to="/sign-up" class="button is-light">Sign Up</router-link>
            </template>
            
              <router-link to="/cart" class="button is-primary">
                <span class="icon">
                  <i class="fas fa-shopping-cart"></i>
                </span>
                <span>Cart ({{ cartTotalLength }})</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>

      <div
      class="is-loading-bar has-text-centered"
      v-if="isLoading" 
    >
      <div class="lds-dual-ring"></div>
    </div>
    <section class="section">
      <router-view />
    </section>
    <footer class="footer">
      <p class="has-text-centered">
        <strong>Store_Copyright (c) 2025</strong>
      </p>
    </footer>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
const showmobilemenu = ref(false);

const toggleMobileMenu = () => {
  showmobilemenu.value = !showmobilemenu.value;
};
const isLoading = computed(() => store.state.isLoading);
const token = computed(() => store.state.token);
import { watch } from 'vue';

watch(token, (newToken) => {
  if (newToken) {
    axios.defaults.headers.common['Authorization'] = "Token " + newToken;
  } else {
    axios.defaults.headers.common['Authorization'] = "";
  }
});
const cartTotalLength = computed(() => {
  const cartItems = store.state.cart.items;
  return cartItems.reduce((total, item) => total + (item.quantity || 0), 0);
});
</script>

<style lang="scss">
@import '../node_modules/bulma/bulma.scss';

.lds-dual-ring {
  display: inline-block;

  &:after {
    content: ' ';
    display: block;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 8px solid #3498db;
    border-color: #3498db transparent #3498db transparent;
    animation: lds-dual-ring 1.2s linear infinite;
  }
}

@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.is-loading-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background-color: #3498db;
  z-index: 9999;
}
</style>