<template>
  <div class="page-search">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="title is-size-2 has-text-centered">Search term: "{{ query }}"</h2>
      </div>
      <div v-if="loading" class="column is-12 has-text-centered">
        <p>Loading...</p>
      </div>
      <div v-else-if="error" class="column is-12 has-text-centered">
        <p class="has-text-danger">{{ error }}</p>
      </div>
      <div v-else-if="products.length === 0" class="column is-12 has-text-centered">
        <p>No products found for "{{ query }}".</p>
      </div>
      <div v-else class="column is-12">
        <ProductBox
          v-for="product in products"
          :key="product.id"
          :product="product"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import ProductBox from '@/components/ProductBox.vue';
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
const query = ref('');
const products = ref([]);
const loading = ref(true);
const error = ref(null);

document.title = 'Store - Search';

// 从 URL 获取查询参数
const url = window.location.search.substring(1);
const params = new URLSearchParams(url);
if (params.get('query')) {
  query.value = params.get('query');
}

onMounted(async () => {
  try {
      store.commit('setLoading', true);
      loading.value = true;
      const response = await axios.post('/api/v1/products/search/', { query: query.value });
      products.value = response.data.results || []; // 适配新响应格式
  } catch (err) {
      error.value = err.response?.data?.error || 'Failed to load search results. Please try again.';
      console.error('Error fetching search results:', err);
  } finally {
      store.commit('setLoading', false);
      loading.value = false;
  }
});
</script>