<template>
  <div class="home">
    <section class="hero is-medium is-dark mb-6">
      <div class="hero-body has-text-centered">
          <p class="title mb-6">
            Welcome to the Store
          </p>
          <p class="subtitle">
            Your one-stop shop for all your needs
          </p>
        </div>
      </section>

      <div class ="columns is-multiline">
        <div class ="column is-12">
          <h2 class ="title is-size-2 has-text-centered">Latest Products</h2>
        </div>
        <ProductBox
          v-for="product in latestProducts"
          v-bind:key="product.id"
          v-bind:product="product"/>
      </div>
  </div>
</template>


<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import ProductBox from '@/components/ProductBox.vue';
import OrderSummary from '@/components/OrderSummary.vue';

const components = {
  ProductBox
};
const store = useStore();
const latestProducts = ref([]);
onMounted(async () => {
  try {
    store.commit('setLoading', true);
    const response = await axios.get('/api/v1/latest-products/');
    latestProducts.value = response.data;
    document.title = 'Store - Latest Products';
    if (!latestProducts.value) {
      throw new Error('No latest products found');
    }
  } catch (error) {
    console.error('Error fetching latest products:', error);
  }
  finally {
      store.commit('setLoading', false);
    }
});
</script>
