<template>
    <div class="d-flex flex-column justify-content-center min-vh-100 w-100"
         style="margin-top: -57px; padding-top: 57px">
        <div class="d-flex justify-content-center align-self-center w-100">
            <div class="card m-3">
                <div class="card-header">
                    <h4>Sign Up</h4>
                    <small class="form-text text-muted">Please fill in the form to create account.</small>
                </div>
                <div class="card-body">
                    <form v-on:submit.prevent="submitCreateUser" novalidate>
                        <div class="form-group">
                            <label for="inputUsername">Username</label>
                            <input type="text" class="form-control" id="inputUsername"
                                   v-model="user.username"
                                   v-bind:class="{'is-invalid':(validator.user.username !== null)}">
                            <div class="invalid-feedback" v-if="validator.user.username !== null">
                                {{ validator.user.username }}
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="col-md-6 mb-3">
                                <label for="inputFirstName">First name</label>
                                <input type="text" class="form-control" id="inputFirstName"
                                       v-model="user.first_name"
                                       v-bind:class="{'is-invalid':(validator.user.first_name !== null)}">
                                <div class="invalid-feedback" v-if="validator.user.first_name !== null">
                                    {{ validator.user.first_name }}
                                </div>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="inputLastName">Last name</label>
                                <input type="text" class="form-control" id="inputLastName"
                                       v-model="user.last_name"
                                       v-bind:class="{'is-invalid':(validator.user.last_name !== null)}">
                                <div class="invalid-feedback" v-if="validator.user.last_name !== null">
                                    {{ validator.user.last_name }}
                                </div>
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="inputEmail">Email address</label>
                            <input type="email" class="form-control" id="inputEmail"
                                   v-model="user.email"
                                   v-bind:class="{'is-invalid':(validator.user.email !== null)}">
                            <div class="invalid-feedback" v-if="validator.user.email !== null">
                                {{ validator.user.email }}
                            </div>
                            <small id="emailHelp" class="form-text text-muted">
                                We'll never share your email with anyone else.
                            </small>
                        </div>
                        <div class="form-group">
                            <label for="inputPassword">Password</label>
                            <input type="password" class="form-control" id="inputPassword"
                                   v-model="user.password"
                                   v-bind:class="{'is-invalid':(validator.user.password !== null)}">
                            <div class="invalid-feedback" v-if="validator.user.password !== null">
                                {{ validator.user.password }}
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="inputPasswordConfirmation">Confirm Password</label>
                            <input type="password" class="form-control" id="inputPasswordConfirmation"
                                   v-model="user.password_confirmation"
                                   v-bind:class="{'is-invalid':(validator.user.password_confirmation !== null)}"
                                   required>
                            <div class="invalid-feedback" v-if="validator.user.password_confirmation !== null">
                                {{ validator.user.password_confirmation }}
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary">Sign Up</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import config from "../config";

    export default {
        name: 'SignUp',
        data() {
            return {
                user: {
                    username: null,
                    first_name: null,
                    last_name: null,
                    email: null,
                    password: null,
                    password_confirmation: null,
                },
                errors: {
                    user: null,
                    _root: null,
                },
            }
        },
        methods: {
            submitCreateUser() {
                if (this.validator.user._is_valid) {
                    let create_user_url = config.$api_url + '/users';
                    let data = {};
                    for (let key in this.user) {
                        if (key !== 'password_confirmation') {
                            data[key] = this.user[key];
                        }
                    }
                    axios.post(create_user_url, data)
                        .then(response => {
                            let payload = response.data;
                            if (payload.status === 'success') {
                                this.$router.push('/');
                            } else {
                                this.errors.user = payload.data;
                                if ('_root' in payload.data) {
                                    this.$store.dispatch('error', {
                                        title: 'Authentication',
                                        body: payload.data['_root'][0],
                                    });
                                }
                            }
                        });
                }
            },
        },
        computed: {
            loading: function () {
                return false;
            },
            validator: function () {
                const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                let errors = {
                    user: {
                        username: null,
                        first_name: null,
                        last_name: null,
                        email: null,
                        password: null,
                        password_confirmation: null,
                        _is_valid: true,
                    },
                };
                if (this.errors.user !== null) {
                    for (let key in this.errors.user) {
                        errors.user[key] = this.errors.user[key][0];
                    }
                }
                if (this.user.username === null || this.user.username.length === 0) {
                    errors.user.username = 'Please provide a valid username.';
                    errors.user._is_valid = false;
                }
                if (this.user.email !== null && this.user.email.length !== 0) {
                    if (!re.test(this.user.email)) {
                        errors.user.email = 'Please provide a valid email address.';
                        errors.user._is_valid = false;
                    }
                }
                if (this.user.password === null || this.user.password.length === 0) {
                    errors.user.password = 'Please provide a valid password.';
                    errors.user._is_valid = false;
                } else if (this.user.password.length < 8) {
                    errors.user.password = 'Length of password should be grater than 8.';
                    errors.user._is_valid = false;
                }
                if (this.user.password !== this.user.password_confirmation) {
                    errors.user.password_confirmation = 'Password does not match with the password confirmation.';
                    errors.user._is_valid = false;
                } else if (this.user.password_confirmation === null || this.user.password_confirmation.length === 0) {
                    errors.user.password_confirmation = 'Please provide the password confirmation.';
                    errors.user._is_valid = false;
                }
                return errors;
            },
        },
    }
</script>
