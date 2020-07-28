export default {
    state: {
        toasts: [],
    },
    mutations: {
        LOG_ERROR(state, message) {
            state.toasts.push({type: 'Error', message});
        },
        LOG_SUCCESS(state, message) {
            state.toasts.push({type: 'Success', message});
        },
    },
    actions: {
        error(context, message) {
            return new Promise((resolve) => {
                context.commit('LOG_ERROR', message);
                resolve();
            })
        },
        success(context, message) {
            return new Promise((resolve) => {
                context.commit('LOG_SUCCESS', message);
                resolve();
            })
        },
    },
    getters: {
        getToast: (state) => {
            return state.toasts[state.toasts.length - 1];
        },
    },
};