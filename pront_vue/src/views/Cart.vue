<template>
    <div class="page-cart">
        <div class="column is-multiline">
            <div class="column is-12">
                <h1 class="title">Cart</h1>
            </div>
            <div class="column is-12 box">
                <table class="table is-fullwidth" v-if="cartTotalLength">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th>Total</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <CartItem
                            v-for="item in cartItems"
                            :key="item.product.id"
                            :initialItem="item"
                            @updateQuantity="updateQuantity"
                            @deleteItem="deleteItem"
                        />
                    </tbody>
                </table>
                <p v-else>You don't have any products in your cart...</p>
            </div>

            <div style="height: 20px;"></div>
            
            <div class = "column is-12 box">
                <h2 class="subtitle">Summary</h2>

                <strong>${{ carTotalPrice.toFixed(2) }}</strong>, {{ cartTotalLength }} items

                <hr>

                <router-link to="/cart/checkout" class="button is-dark">Proceed to checkout</router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import CartItem from '@/components/CartItem.vue';
import { computed, onMounted, ref } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
const cart = ref({
    items: [],
});

// 确保 cartItems 始终是数组
const cartItems = computed(() => {
    return cart.value && Array.isArray(cart.value.items) ? cart.value.items : [];
});

// 更新商品数量
function updateQuantity({ item, change }) {
    const cartItem = cart.value.items.find((i) => i.product.id === item.product.id);
    if (cartItem) {
        cartItem.quantity += change;
        if (cartItem.quantity < 1) {
            cartItem.quantity = 1; // 防止数量小于 1
        }
    }
    // 同步更新 Vuex Store 和 localStorage
    store.commit('setCart', { ...cart.value });
    localStorage.setItem('cart', JSON.stringify(cart.value));
}

// 删除商品
function deleteItem(item) {
    // 从前端购物车中移除商品
    cart.value.items = cart.value.items.filter((i) => i.product.id !== item.product.id);

    // 同步更新 Vuex Store 和 localStorage
    store.commit('setCart', { ...cart.value });
    localStorage.setItem('cart', JSON.stringify(cart.value));
}

onMounted(() => {
    try {
        store.commit('setLoading', true);
        // 从 localStorage 或 Vuex store 获取 cart 数据
        const savedCart = localStorage.getItem('cart');
        const cartData = savedCart ? JSON.parse(savedCart) : store.state.cart || { items: [] };
        cart.value.items = Array.isArray(cartData.items) ? cartData.items : [];
    } catch (err) {
        console.error('Error loading cart:', err);
    } finally {
        store.commit('setLoading', false);
    }
});

// 计算购物车总数量
const cartTotalLength = computed(() => {
    return cartItems.value.reduce((acc, curVal) => acc + (curVal.quantity || 0), 0);
});

// 计算购物车总价格
const carTotalPrice = computed(() => {
    return cartItems.value.reduce((acc, curVal) => acc + (curVal.quantity * curVal.product.price || 0), 0);
});
</script>