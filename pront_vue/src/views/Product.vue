<template>
    <div class="page product-page">
      <div v-if="loading" class="has-text-centered">
        <p>Loading...</p>
      </div>
      <div v-else-if="error" class="has-text-centered">
        <p class="has-text-danger">{{ error }}</p>
      </div>
      <div v-else class="column is-multiline">
        <div class="column is-9">
          <figure class="image mb-6">
            <img :src="product.get_image" alt="Product image" v-if="product.get_image" />
          </figure>
          <h1 class="title">{{ product.name }}</h1>
          <p>{{ product.description }}</p>
        </div>
        <div class="column is-3">
          <h2 class="subtitle">Information</h2>
          <p><strong>Price:</strong> ${{ product.price }}</p>
          <div class="field has-addons mt-6">
            <div class="control">
              <input type="number" class="input" min="1" v-model="quantity" />
            </div>
            <div class="control">
              <a class="button is-dark" @click="addToCart">Add to cart</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import axios from 'axios';
  import { ref, onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { useStore } from 'vuex';
  import { toast } from 'bulma-toast';
  
  const store = useStore();
  const route = useRoute();
  const router = useRouter();
  const quantity = ref(1);
  const product = ref({});
  const loading = ref(true);
  const error = ref(null);
  
  onMounted(async () => {
    try {
      store.commit('setLoading', true);
      const response = await axios.get(`/api/v1/products/${route.params.category_slug}/${route.params.product_slug}/`);
      product.value = response.data;
      document.title = 'Store - ' + product.value.name;
      if (!product.value) {
        error.value = 'Product not found';
        return;
      }
    } catch (err) {
      error.value = 'Failed to load product. Please try again.';
      console.error('Error fetching product:', err);
    } finally {
      store.commit('setLoading', false);
      loading.value = false;
    }
  });
  
  const addToCart = () => {
    if (isNaN(quantity.value) || quantity.value < 1) {
      quantity.value = 1;
    }
    const item = {
      product: product.value,
      quantity: quantity.value,
    };
    store.commit('addToCart', item);
    toast({
      message: `${product.value.name} has been added to your cart`,
      type: 'is-success',
      duration: 3000,
      position: 'top-center',
      closeOnClick: true,
      pauseOnHover: true,
    });
  };
  </script>