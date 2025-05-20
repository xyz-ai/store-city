<template>
    <div class="page-category">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h2 class="title is-size-2 has-text-centered">{{ category.name }}</h2>
            </div>
        </div>
        <ProductBox
          v-for="product in category.products"
          v-bind:key="product.id"
          v-bind:product="product"/>
      </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { ref, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import ProductBox from '@/components/ProductBox.vue';
const route = useRoute();
const store = useStore();

const category = ref({});
const components = {
  ProductBox
};
// 定义一个函数来加载数据
const loadCategory = async () => {
  try {
    store.commit('setLoading', true);
    const response = await axios.get(`/api/v1/products/${route.params.category_slug}/`);
    category.value = response.data;
    store.commit('setCategory', response.data);
    document.title = 'Store - ' + category.value.name;
  } catch (err) {
    store.commit('setError', 'Failed to load category. Please try again.');
    console.error('Error fetching category:', err);
  } finally {
    store.commit('setLoading', false);
  }
};

// 在组件挂载时加载数据
onMounted(loadCategory);

// 监听路由参数变化
watch(() => route.params.category_slug, loadCategory);
</script>