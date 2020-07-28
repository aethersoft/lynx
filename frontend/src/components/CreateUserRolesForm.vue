<template>
    <div>
        <form id="editRoleForm" class="needs-validation" :class="{ 'was-validated' : validated.user_role }"
              v-on:submit.prevent="submit" novalidate>
            <div class="form-row">
                <div class="col mb-3">
                    <label for="usernameInput">Username</label>
                    <input id="usernameInput" type="search" name="name" class="form-control"
                           :style="[(user_list !== null && user_list.length > 0) ? {'border-bottom-left-radius': 0, 'border-bottom-right-radius': 0} : {}]"
                           minlength="3" maxlength="30"
                           v-model="user_role.username" autocomplete="off" spellcheck="false"
                           v-on:keyup="inputUsernameKeyUp" required>
                    <div id="userSearchResults" class="position-absolute w-100" style="padding-right:10px;">
                        <div class="list-group">
                            <button type="button" class="list-group-item list-group-item-action border-top-0"
                                    v-for="(user, i) in user_list" :key="i" v-on:click="setUsername(user.username)">
                                {{ user.username }}
                            </button>
                        </div>
                    </div>
                    <div class="invalid-feedback"
                         v-if="user_role.username === null || user_role.username.length === 0">
                        Please provide a valid username.
                    </div>
                    <div class="invalid-feedback"
                         v-else-if="user_role.username.length <= 3 || user_role.username.length > 30">
                        Please provide a username with length between 3 and 30.
                    </div>
                </div>
                <div class="col mb-3">
                    <label for="inputGroupSelect">Role</label>
                    <select id="inputGroupSelect" class="custom-select" v-model="user_role.role" required>
                        <option :value="name" v-for="(value, name) in user_roles" :key="name">
                            {{ value }}
                        </option>
                    </select>
                    <div class="invalid-feedback">
                        Please provide a valid role.
                    </div>
                </div>
                <div class="col-auto mb-3" style="padding-top: 32px">
                    <div class="d-flex flex-column align-items-center">
                        <button type="submit" class="btn btn-primary mb-2">
                            <span class="oi oi-plus" title="plus" aria-hidden="true"></span>
                        </button>
                    </div>
                </div>
            </div>
        </form>
        <table class="table table-bordered" v-if="!loading">
            <thead>
            <tr>
                <th scope="col">Username</th>
                <th scope="col">First Name</th>
                <th scope="col">Last Name</th>
                <th scope="col">Role</th>
                <th scope="col" class="text-center">Actions</th>
            </tr>
            </thead>
            <tbody>
            <tr v-if="user_role_list.length === 0">
                <td colspan="5" class="text-center">
                    <h4 class="display-5">No User Roles Found</h4>
                    <p class="text-muted mb-0">Try creating a new user role</p>
                </td>
            </tr>
            <tr v-else v-for="(u, i) in user_role_list" :key="i">
                <th scope="row">{{ u.user.username }}</th>
                <td>{{ u.user.first_name }}</td>
                <td>{{ u.user.last_name }}</td>
                <td>{{ user_roles[u.role] }}</td>
                <td>
                    <div class="d-flex flex-column align-items-center">
                        <a type="button" class="btn btn-primary" href="javascript:void(0)"
                           v-on:click.stop="deleteAssignedRole(u.user.username, u.role)">
                            <span class="oi oi-trash" title="trash" aria-hidden="true"></span>
                        </a>
                    </div>
                </td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import $ from 'jquery';
    import axios from 'axios';
    import config from "../config";

    export default {
        name: 'CreateProjectUserRolesForm',
        data() {
            return {
                user_role_list: null,
                user_list: [],
                user_role: {
                    username: null,
                    role: null,
                },
                user_roles: {
                    admin: 'Administer',
                    contributor: 'Contributor',
                },
                validated: {
                    user_role: false,
                },
            }
        },
        methods: {
            retrieveRoles: function () {
                let user_roles_url = config.$api_url + '/projects/' + this.$route.params.projectId + '/users';
                axios.get(user_roles_url)
                    .then(response => {
                        let payload = response.data;
                        if (payload.status === 'success') {
                            this.user_role_list = payload.data;
                        }
                    });
            },
            deleteAssignedRole: function (username, role) {
                let user_roles_url = config.$api_url + '/projects/' + this.$route.params.projectId + '/users';
                axios.delete(user_roles_url, {data: {username, role}})
                    .then(response => {
                        let payload = response.data;
                        if (payload.status === 'success') {
                            this.$store.dispatch('success', {
                                title: 'User Role',
                                body: 'User role delete success.'
                            });
                            this.retrieveRoles();
                        }
                    });
            },
            retrieveUsers: function () {
                let user_roles_url = config.$api_url + '/users';
                if (this.user_role.username !== null && this.user_role.username !== '') {
                    user_roles_url += '?q=' + this.user_role.username;
                } else {
                    user_roles_url += '?q=$null'
                }
                axios.get(user_roles_url)
                    .then(response => {
                        let payload = response.data;
                        this.user_list = payload.data;
                        this.retrieveRoles();
                    });
            },
            setUsername(username) {
                this.user_role.username = username;
                this.user_list = [];
            },
            inputUsernameKeyUp: function () {
                this.retrieveUsers();
            },
            documentOnClick() {
                this.user_list = [];
            },
            submit: function () {
                let user_roles_url = config.$api_url + '/projects/' + this.$route.params.projectId + '/users';
                axios.post(user_roles_url, this.user_role)
                    .then(response => {
                        let payload = response.data;
                        if (payload.status === 'success') {
                            this.validated.user_role = true;
                            this.$store.dispatch('success', {
                                title: 'User Role',
                                body: 'User role update success.'
                            });
                        }
                        this.retrieveRoles();
                    });
            },
        },
        mounted() {
            this.retrieveRoles();
            $(document).on('click', this.documentOnClick);
        },
        computed: {
            loading: function () {
                return this.user_role_list === null;
            },
        },
    }
</script>