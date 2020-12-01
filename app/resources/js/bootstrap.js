window._ = require('lodash');


try {
    window.Popper = require('popper.js').default;

} catch (e) {}


window.axios = require('axios');


window.axios.defaults.xsrfHeaderName = "X-CSRFToken"
window.axios.defaults.xsrfCookieName = 'csrftoken'
window.axios.defaults.withCredentials = true
window.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

let token = document.head.querySelector('meta[name="csrf-token"]');

if (token) {
    //window.axios.defaults.headers.common['X-CSRFToken'] = token.content;
} else {
    //console.error('CSRF token not found');
}