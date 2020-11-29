import Vue from 'vue'

require('./bootstrap')

Vue.component('login-component', require('./components/auth/LoginComponent.vue').default)
Vue.component('register-component', require('./components/auth/RegisterComponent.vue').default)
Vue.component('home-component', require('./components/core/HomeComponent.vue').default)
Vue.component('company-create-component', require('./components/core/company/CompanyCreateComponent.vue').default)

const app = new Vue({
    el: '#app',
});