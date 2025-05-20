<template>
    <tr>
        <td>
            <router-link :to="initialItem.product.get_absolute_url" class="product-name">
                {{ initialItem.product.name }}
            </router-link>
        </td>
        <td>${{ initialItem.product.price }}</td>
        <td>
            <button class="button is-small" @click="decreaseQuantity">-</button>
            <span class="mx-2">{{ initialItem.quantity }}</span>
            <button class="button is-small" @click="increaseQuantity">+</button>
        </td>
        <td>${{ getItemTotal(initialItem).toFixed(2) }}</td>
        <td>
            <button class="delete" @click="deleteItem"></button>
        </td>
    </tr>
</template>

<script setup>
import { SassColor } from 'sass';



// 接收父组件传递的 props
const props = defineProps({
    initialItem: Object
});

// 定义事件，用于通知父组件
const emit = defineEmits(['updateQuantity', 'deleteItem']);

// 计算商品总价
function getItemTotal(item) {
    return item.quantity * item.product.price;
}

// 增加商品数量
function increaseQuantity() {
    emit('updateQuantity', { item: props.initialItem, change: 1 });
}

// 减少商品数量
function decreaseQuantity() {
    if (props.initialItem.quantity > 1) {
        emit('updateQuantity', { item: props.initialItem, change: -1 });
    }
}

// 删除商品
function deleteItem() {
    emit('deleteItem', props.initialItem);
}
</script>

<style scoped>
.product-name {
    color: black; /* 设置字体颜色为黑色 */
    font-weight: bold; /* 可选：设置字体加粗 */
}
</style>