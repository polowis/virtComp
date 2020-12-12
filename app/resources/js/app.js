import Vue from 'vue'

require('./bootstrap')

Vue.component('login-component', require('./components/auth/LoginComponent.vue').default)
Vue.component('register-component', require('./components/auth/RegisterComponent.vue').default)
Vue.component('home-component', require('./components/core/HomeComponent.vue').default)
Vue.component('company-create-component', require('./components/core/company/CompanyCreateComponent.vue').default)
Vue.component('corporation-all-view', require('./components/core/corperation/AllView.vue').default)
Vue.component('land-all-component', require('./components/core/land/LandAll.vue').default)
Vue.component('homev2-component', require('./components/core/HomeV2Component.vue').default)
Vue.component('land-view-component', require('./components/core/land/LandView.vue').default)

const app = new Vue({
    el: '#app',
});