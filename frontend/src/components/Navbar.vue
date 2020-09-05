<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm"
         v-if="typeof $route.meta.navbar !== 'undefined'">
        <a id="menu-toggle" class="navbar-brand text-center" href="javascript:void(0)">
            <img src="../assets/images/logo.svg" height="30px" class="d-inline-block align-top"
                 alt="Lynx">
            Lynx
        </a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto" v-if="!isAuthenticated">
                <li class="nav-item" v-bind:class="{'active':($route.meta.navbar.active==='home')}">
                    <a class="nav-link" href="/"> Home
                        <span v-if="$route.meta.navbar.active==='home'" class="sr-only">(current)</span>
                    </a>
                </li>
                <li class="nav-item" v-bind:class="{'active':($route.meta.navbar.active==='about')}">
                    <a class="nav-link" href="/about"> About
                        <span v-if="$route.meta.navbar.active==='about'" class="sr-only">(current)</span>
                    </a>
                </li>
            </ul>
            <ul class="navbar-nav mr-auto pl-3" v-else>
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb m-0 p-1 pl-3 pr-3">
                        <li class="breadcrumb-item" v-if="$route.path.startsWith('/projects/')">
                            <a href="/projects">Home</a>
                        </li>
                        <li class="breadcrumb-item" v-else-if="$route.path==='/' || $route.path==='/projects'">
                            Home
                        </li>
                        <li class="breadcrumb-item" v-else>
                            <a href="/">Home</a>
                        </li>
                        <li class="breadcrumb-item"
                            v-if="$route.path.startsWith('/projects/') && $route.path!=='/projects' && $route.path.endsWith('dashboard')">
                            Edit
                        </li>
                        <li class="breadcrumb-item"
                            v-else-if="$route.path.startsWith('/projects/') && $route.path!=='/projects'">
                            <router-link :to="{name: 'ProjectDashboard', params: { projectId: projectId }}">Edit</router-link>
                        </li>
                        <li class="breadcrumb-item"
                            v-if="$route.path.startsWith('/a/projects/') && $route.path.endsWith('documents')">
                            Documents
                        </li>
                        <li class="breadcrumb-item" v-else-if="$route.path.startsWith('/a/') && $route.path!=='/'">
                            Annotate
                        </li>
                        <li class="breadcrumb-item" v-if="$route.path.startsWith('/projects/') && $route.path.endsWith('documents')">
                            Documents
                        </li>
                        <li class="breadcrumb-item" v-else-if="$route.path.startsWith('/projects/') && $route.path.endsWith('reports')">
                            Reports
                        </li>
                        <li class="breadcrumb-item" v-else-if="$route.path.startsWith('/projects/') && $route.path.endsWith('tasks')">
                            Tasks
                        </li>
                        <li class="breadcrumb-item" v-else-if="$route.path.startsWith('/projects/') && $route.path.endsWith('presenter')">
                            Presenter
                        </li>
                        <li class="breadcrumb-item" v-else-if="$route.path.startsWith('/projects/') && $route.path.endsWith('settings')">
                            Settings
                        </li>
                    </ol>
                </nav>
            </ul>
            <ul class="navbar-nav">
                <li class="nav-item dropdown">
                    <a class="nav-link" href="javascript:void(0)" id="navbarDropdown" role="button"
                       data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"
                       :class="{'text-primary':isAuthenticated}">
                        <!-- <span class="oi oi-person" title="user" aria-hidden="true"></span>-->
                        <svg class="bi bi-person-circle" width="1.5em" height="1.5em" viewBox="0 0 16 16"
                             fill="currentColor"
                             xmlns="http://www.w3.org/2000/svg">
                            <path d="M13.468 12.37C12.758 11.226 11.195 10 8 10s-4.757 1.225-5.468 2.37A6.987 6.987 0 0 0 8 15a6.987 6.987 0 0 0 5.468-2.63z"/>
                            <path fill-rule="evenodd" d="M8 9a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                            <path fill-rule="evenodd"
                                  d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zM0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8z"/>
                        </svg>
                    </a>
                    <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdown">
                        <Avatar/>
                        <template v-if="isAuthenticated">
                            <div class="btn-group btn-group-sm p-3">
                                <a class="btn btn-primary"
                                   v-bind:class="{'active':($route.meta.navbar.active==='home')}"
                                   href="/">Contributor</a>
                                <a class="btn btn-primary"
                                   v-bind:class="{'active':($route.meta.navbar.active==='projects')}" href="/projects">Administer</a>
                            </div>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="javascript:void(0)" @click="signout">Sign Out</a>
                        </template>
                        <template v-else>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="/signin">Sign in</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="/signup">sign Up</a>
                        </template>
                    </div>
                </li>
            </ul>
        </div>
    </nav>
</template>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    nav {
        z-index: 1;
    }

    .navbar-brand {
        min-width: 168px;
    }
</style>

<!--suppress NpmUsedModulesInstalled -->
<script>
    import Avatar from '@/components/Avatar.vue'

    export default {
        name: 'Navbar',
        components: {
            Avatar
        },
        methods: {
            signout: function () {
                let self = this;
                this.$store.dispatch('signout').then(function () {
                    self.$router.push({name: 'Home'}).then(() => {
                        location.reload();
                    }).catch((error) => {
                        console.error(error);
                        location.reload();
                    });
                });
            }
        },
        computed: {
            isAuthenticated: function () {
                return this.$store.getters.isAuthenticated;
            },
            projectId: function () {
                return this.$route.params.projectId;
            },
        },
    }
</script>