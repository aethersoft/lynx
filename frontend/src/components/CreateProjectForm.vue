<template>
    <form class="form-page" v-on:submit.prevent="submit" novalidate v-if="!loading">
        <div class="form-group">
            <label for="inputName">Name</label>
            <input id="inputName" type="text" name="name" class="form-control" required pattern=".{3,10}"
                   v-model="project.name" v-bind:class="{'is-invalid':(validator.project.name !== null)}">
            <div class="invalid-feedback" v-if="validator.project.name !== null">
                {{ validator.project.name }}
            </div>
        </div>
        <div class="form-group">
            <label for="inputDescription">Description</label>
            <textarea name="description" class="form-control"
                      id="inputDescription" required pattern=".{3,30}"
                      v-model="project.description"
                      v-bind:class="{'is-invalid':(validator.project.description !== null)}"></textarea>
            <div class="invalid-feedback" v-if="validator.project.description !== null">
                {{ validator.project.description }}
            </div>
        </div>
        <div class="form-group">
            <label for="inputRedundancy">Redundancy</label>
            <input id="inputRedundancy" type="number" name="redundancy" class="form-control"
                   v-model="project.redundancy" v-bind:class="{'is-invalid':(validator.project.redundancy !== null)}">
            <div class="invalid-feedback" v-if="validator.project.redundancy !== null">
                {{ validator.project.redundancy }}
            </div>
        </div>
        <div class="form-group">
            <label for="inputScheduler">Scheduler</label>
            <input name="scheduler" type="text" class="form-control"
                   id="inputScheduler" required v-model="project.scheduler"
                   v-bind:class="{'is-invalid':(validator.project.scheduler !== null)}" disabled>
            <div class="invalid-feedback" v-if="validator.project.scheduler !== null">
                {{ validator.project.scheduler }}
            </div>
        </div>
        <button type="submit" class="btn btn-primary" hidden>Submit</button>
    </form>
</template>

<script>
    import axios from 'axios';
    import config from "../config";

    export default {
        name: 'CreateProjectForm',
        data() {
            return {
                project_id: null,
                project: null,
                errors: {},
            }
        },
        methods: {
            retrieveProject: function () {
                let project_url = config.$api_url + '/projects/' + this.project_id;
                axios.get(project_url)
                    .then(response => {
                        let payload = response.data;
                        if (payload.status === 'success') {
                            this.project = payload.data;
                        } else {
                            let error = payload.data;
                            console.error(error);
                            this.errors.default.push(error);
                        }
                    }).catch((error) => {
                    console.error(error);
                    error = {
                        _root: ['Unable to serve the request. ' +
                        'Please try again later or contact admin for assistance.']
                    };
                    this.errors.default.push(error);
                });
            },
            submit: function () {
                this.errors.project = null;
                if (this.validator.project._is_valid) {
                    return new Promise((resolve, reject) => {
                        let promise;
                        if (this.project_id === null) {
                            promise = axios.post(config.$api_url + '/projects', this.project)
                        } else {
                            promise = axios.put(config.$api_url + '/projects/' + this.project_id, this.project)
                        }
                        promise.then((response) => {
                            let payload = response.data;
                            if (payload.status === 'success') {
                                resolve();
                            } else {
                                const error = payload.data;
                                this.errors.project = error;
                                reject(error);
                            }
                        }).catch((error) => {
                            error = {
                                _root: ['Unable to serve the request. ' +
                                'Please try again later or contact admin for assistance.']
                            };
                            this.errors.project = error;
                            reject(error);
                        });
                    });
                }
            },
        },
        mounted() {
            this.project_id = 'projectId' in this.$route.params ? this.$route.params.projectId : null;
            if (this.project_id !== null) {
                this.retrieveProject();
            } else {
                this.project = {
                    name: 'Untitled',
                    description: 'Default Description',
                    redundancy: 3,
                    scheduler: 'default',
                }
            }
        },
        computed: {
            loading: function () {
                return this.project === null;
            },
            validator: function () {
                let errors = {
                    project: {
                        name: null, description: null, redundancy: null, scheduler: null,
                        _root: null, _is_valid: true,
                    },
                };
                if (typeof this.errors.project !== 'undefined') {
                    for (let key in this.errors.project) {
                        if (Object.prototype.hasOwnProperty.call(this.errors.project, key)) {
                            errors.project[key] = this.errors.project[key][0];
                            errors.project._is_valid = false;
                        }
                    }
                }
                delete this.errors.project;
                if (this.project.name == null) {
                    errors.project.name = 'Name of the project is required to continue.';
                    errors.project._is_valid = false;
                } else if (this.project.name.length < 3) {
                    errors.project.name = 'Length of name should be more than three characters.';
                    errors.project._is_valid = false;
                } else if (this.project.name.length > 256) {
                    errors.project.name = 'Length of name should be less than ten characters.';
                    errors.project._is_valid = false;
                }
                if (this.project.description == null) {
                    errors.project.description = 'Description of the project is required to continue.';
                    errors.project._is_valid = false;
                } else if (this.project.description.length < 3) {
                    errors.project.description = 'Length of description should be more than three characters.';
                    errors.project._is_valid = false;
                } else if (this.project.description.length > 2048) {
                    errors.project.description = 'Length of description should be less than ten characters.';
                    errors.project._is_valid = false;
                }
                if (this.project.redundancy < 1) {
                    errors.project.redundancy = 'Project task redundancy should be greater than one.';
                    errors.project._is_valid = false;
                }
                return errors;
            },
        },
    }
</script>