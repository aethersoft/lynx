import Vue from 'vue';
import Vuex from 'vuex';
import token from './token';
import toast from './toast';

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        token: token,
        toast: toast,
    },
});