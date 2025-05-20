import { createStore } from 'vuex';

export default createStore({
  state: {
    cart: {
      items: [],
    },
    isAuthenticated: false,
    token: '',
    isLoading: false, // 初始状态为 false
  },
  getters: {
    cartTotalLength(state) {
      return state.cart.items.reduce((total, item) => total + (item.quantity || 0), 0);
    },
  },
  mutations: {
    setCart(state, cart) {
      state.cart = cart;
    },
    initializeStore(state) {
      if (localStorage.getItem('cart')) {
        state.cart = JSON.parse(localStorage.getItem('cart'));
      } else {
        localStorage.setItem('cart', JSON.stringify(state.cart));
      }

      if (localStorage.getItem('token')){
          state.token = localStorage.getItem('token')
          state.isAuthenticated = true
      } else {
        state.token=''
        state.isAuthenticated = false
      }
    },
    addToCart(state, item) {
      const exists = state.cart.items.find(i => i.product.id === item.product.id);
      if (exists) {
        exists.quantity = parseInt(exists.quantity) + parseInt(item.quantity);
      } else {
        state.cart.items.push(item);
      }
      localStorage.setItem('cart', JSON.stringify(state.cart));
    },
    setLoading(state, isLoading) {
      state.isLoading = isLoading;
    },
    setToken(state,token){
      state.token = token
      state.isAuthenticated = true
    },
    removeToken(state){
      state.token = ''
      state.isAuthenticated = false
    },
    clearCart(state){
      state.cart = { items: [] }
      localStorage.setItem('cart', JSON.stringify(state.cart))
    },
  },
  actions: {
    initializeCart({ commit }) {
      const cart = {
        items: [],
      };
      commit('setCart', cart);
      commit('initializeStore');
    },
    initializeApp({ commit }) {
      // 模拟初始化操作
      setTimeout(() => {
        commit('setLoading', false); // 页面加载完成后设置为 false
      }, 1000); // 1 秒后隐藏加载栏
    },
  },
  modules: {},
});