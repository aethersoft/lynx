import axios from "axios";
import config from "../config";

export default {
    state: {
        status: '',
        token: '',
        user: {},
        error: {},
    },
    mutations: {
        AUTH_REQUEST(state) {
            state.status = 'loading';
        },
        AUTH_SUCCESS(state, {token, user}) {
            localStorage.setItem('auth-token', token);
            localStorage.setItem('auth-user', JSON.stringify(user));
            localStorage.removeItem('auth-error');
            state.status = 'success';
        },
        AUTH_ERROR(state, error) {
            localStorage.removeItem('auth-token');
            localStorage.removeItem('auth-user');
            localStorage.setItem('auth-error', JSON.stringify(error));
            state.status = 'error';
        },
        SIGNOUT(state) {
            localStorage.removeItem('auth-token');
            localStorage.removeItem('auth-user');
            state.status = '';
        },
        REFRESH(state) {
            state.token = localStorage.getItem('auth-token') || '';
            state.user = JSON.parse(localStorage.getItem('auth-user')) || {};
            state.error = JSON.parse(localStorage.getItem('auth-error')) || {};
        },
    },
    actions: {
        signin(context, auth) {
            return new Promise((resolve, reject) => {
                context.commit('AUTH_REQUEST');
                axios.get(config.$api_url + '/token', {auth})
                    .then(function (response) {
                        // handle success
                        let payload = response.data;
                        if (payload.status === 'success') {
                            const token = payload.data.token;
                            const user = payload.data.user;
                            // register successful login
                            context.commit('AUTH_SUCCESS', {token, user});
                            context.dispatch('refresh');
                            resolve(payload)
                        } else {
                            // handle error
                            context.commit('AUTH_ERROR', payload.data);
                            context.dispatch('refresh');
                            reject(payload);
                        }
                    })
                    .catch(function (error) {
                        console.log(error);
                        let _root = ['Please recheck your username and password then try again.'];
                        // handle error
                        context.commit('AUTH_ERROR', _root);
                        context.dispatch('refresh');
                        reject({data: {_root}});
                    });
            })
        },
        signout(context) {
            return new Promise((resolve) => {
                context.commit('SIGNOUT');
                resolve();
            })
        },
        refresh(context) {
            return new Promise((resolve) => {
                context.commit('REFRESH');
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + context.state.token;
                resolve();
            })
        },
    },
    getters: {
        isAuthenticated: (state) => !!state.token,
        getUser: (state) => state.user,
        getAuthToken: (state) => state.token,
    },
};