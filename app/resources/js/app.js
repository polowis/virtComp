import Vue from 'vue'


Vue.component('login-component', require('./components/auth/LoginComponent.vue').default)

const app = new Vue({
    el: '#app',
});