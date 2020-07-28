import Vue from 'vue';
import App from './App.vue';
import config from './config';
import router from './router';
import store from './store/index';
import axios from "axios";

import 'bootstrap';
import 'typeface-inter';

import './assets/scss/bootstrap.scss';
import './assets/scss/open-iconic.scss';

config.$api_url = process.env.VUE_APP_API_URL || config.$api_url;

Vue.prototype.appConfig = config;

Vue.config.productionTip = false;

new Vue({
    router,
    store,
    beforeCreate() {
        axios.interceptors.response.use(function (response) {
            return response;
        }, function (error) {
            if (error.response.status === 401) {
                store.dispatch('signout').then(router.push('/signin').then)
            }
            return Promise.reject(error);
        });
        store.dispatch('refresh').then();
    },
    render: h => h(App)
}).$mount('#app');
