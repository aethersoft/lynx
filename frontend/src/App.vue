<template>
    <div id="app" class="h-100 w-100">
        <Navbar></Navbar>
        <div style="position: absolute; top: 56px; right: 0; min-width: 250px; z-index: 10;" class="m-3">
            <div class="toast" role="alert" aria-live="assertive" aria-atomic="true"
                 v-for="(toast, index) in toasts" :key="index">
                <div class="toast-header">
                    <strong class="mr-auto"
                            :class="{'text-success':toast.type==='Success', 'text-danger':toast.type==='Error' }">
                        {{ toast.type }}
                    </strong>
                    <small class="text-muted">{{ toast.message.title }}</small>
                    <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="toast-body text-dark">
                    {{ toast.message.body }}
                </div>
            </div>
        </div>
        <div id="wrapper" class="d-flex" v-if="$route.meta.sidebar!==null">
            <Sidebar></Sidebar>
            <router-view/>
        </div>
        <template v-else>
            <router-view/>
        </template>
    </div>
</template>

<style type="scss">
    /*
    * Page Style
    */
    html {
        min-height: 100%;
    }

    body {
        height: 100vh;
        width: 100%;
        overflow-x: hidden;
    }
</style>

<!--suppress NpmUsedModulesInstalled -->
<script>
    import Navbar from '@/components/Navbar.vue';
    import Sidebar from "@/components/Sidebar.vue";
    import $ from 'jquery';

    export default {
        name: 'Home',
        components: {
            Sidebar,
            Navbar
        },
        data: function () {
            return {
                toasts: [],
            }
        },
        mounted() {
            document.title = 'Lynx';
        },
        computed: {
            isAuthenticated: function () {
                return this.$store.getters.isAuthenticated;
            },
            toast: function () {
                return this.$store.getters.getToast;
            }
        },
        watch: {
            toast: function (item) {
                if (this.toasts.length >= 5)
                    this.toasts.pop();
                this.toasts.push(item);
                this.$nextTick(() => {
                    $('.toast').toast({autohide: false}).toast('show');
                });
                const self = this;
                setTimeout(function () {
                    self.toasts.pop();
                }, 3000);
            },
        }
    }
</script>