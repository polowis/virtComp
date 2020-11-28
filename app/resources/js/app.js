import Vue from 'vue'


Vue.component('login-component', require('./components/auth/LoginComponent.vue').default)
Vue.component('register-component', require('./components/auth/RegisterComponent.vue').default)

const app = new Vue({
    el: '#app',
});