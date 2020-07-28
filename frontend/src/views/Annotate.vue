<template>
    <div class="container p-3">
        <template v-if="loading">
            <div class="d-flex justify-content-center">
                <div class="spinner-border" role="status">
                    <span class="sr-only">Loading...</span>
                </div>
            </div>
        </template>
        <template v-if="completed">
            <div class="d-flex w-100 justify-content-center">
                <div class="jumbotron jumbotron-fluid bg-transparent">
                    <div class="container">
                        <div class="empty-icon text-center pb-3">
                            <span class="oi oi-document text-gray" style="font-size: 5em;" title="document"
                                  aria-hidden="true"></span>
                        </div>
                        <h4 class="lead text-center pb-1">We could't find any documents for you to contribute.</h4>
                        <p class="text-center">Please check this project later for any updates.</p>
                    </div>
                </div>
            </div>
        </template>
        <template v-if="!(loading || completed)">
            <div class="nav nav-pills mb-3">
                <template v-if="document_id === null">
                    <a class="nav-link bg-light mr-1" role="button"
                       v-bind:class="{'text-danger':annotation_set.flagged}" v-on:click.stop="flag()">
                        <span class="oi oi-flag" title="flag" aria-hidden="true"></span>
                    </a>
                    <a class="nav-link bg-light mr-auto" role="button" v-on:click.stop="skip()">
                        <span class="oi oi-media-skip-forward" title="skip" aria-hidden="true"></span>
                    </a>
                    <a class="nav-link bg-primary text-light" role="button" v-on:click.stop="next()">
                        <span class="oi oi-chevron-right" title="check" aria-hidden="true"></span>
                    </a>
                </template>
                <template v-else>
                    <a class="nav-link bg-light mr-1" role="button"
                       v-bind:class="{'text-danger':annotation_set.flagged}" v-on:click.stop="flag()">
                        <span class="oi oi-flag" title="flag" aria-hidden="true"></span>
                    </a>
                    <a role="button" class="nav-link bg-light mr-auto" v-on:click.stop="back()" data-toggle="tooltip"
                       data-placement="bottom" title="Cancel">
                        <span class="oi oi-x" title="check" aria-hidden="true"></span>
                    </a>
                    <a role="button" class="nav-link bg-light" v-on:click.stop="upload()" data-toggle="tooltip"
                       data-placement="bottom" title="Save">
                        <span class="oi oi-cloud-upload" title="check" aria-hidden="true"></span>
                    </a>
                </template>
            </div>
            <Presenter ref="presenter"></Presenter>
        </template>
    </div>
</template>

<!--suppress NpmUsedModulesInstalled -->
<script>
    import axios from 'axios';
    import config from "../config";

    import Presenter from '@/components/Presenter.vue';

    export default {
        name: 'Annotate',
        components: {Presenter},
        data() {
            return {
                completed: false,
                annotation_set: null,
                document: null,
                tasks: [],
                annotations: {},
                document_id: null, // for editing only
                presenter: '',
            }
        },
        methods: {
            flag() {
                axios.post(config.$api_url + '/annotate', {
                    operation: 'flag',
                    data: {
                        document_id: this.document.id,
                    }
                }).then((response) => {
                    let payload = response.data;
                    if (payload.status === 'success') {
                        this.annotation_set = payload.data;
                    } else {
                        const error = payload.data;
                        console.error(error);
                    }
                }).catch((error) => {
                    console.error(error);
                });
            },
            skip() {
                axios.post(config.$api_url + '/annotate', {
                    operation: 'skip',
                    data: {
                        document_id: this.document.id,
                    }
                }).then((response) => {
                    if (response.data.status !== 'success') {
                        const error = response.data.data;
                        console.error(error);
                    }
                    location.reload();
                }).catch((error) => {
                    console.error(error);
                });
            },
            save() {
                return new Promise((resolve, reject) => {
                    axios.post(config.$api_url + '/annotate', {
                        operation: 'save', data: {
                            document_id: this.document.id,
                            annotations: this.$refs.presenter.getAnnotations(),
                        }
                    }).then((response) => {
                        if (response.data.status !== 'success') {
                            const error = response.data;
                            console.error(error);
                            reject(error);
                        }
                        resolve(response);
                    }).catch((error) => {
                        console.error(error);
                        reject(error);
                    });
                });
            },
            next(event) {
                this.save(event).then((response) => {
                    const payload = response.data;
                    // Secondary check - not required!
                    if (payload.status === 'success') {
                        location.reload();
                    } else {
                        const error = response.data;
                        console.error(error);
                    }
                }).catch((error) => {
                    console.error(error);
                });
            },
            upload() {
                let params = {projectId: this.$route.params.projectId};
                this.save().then(() => this.$router.push({'name': 'AssignedDocuments', params}));
            },
            back() {
                let params = {projectId: this.$route.params.projectId};
                this.$router.push({'name': 'AssignedDocuments', params})
            },
            update() {
                if ('presenter' in this.$refs) {
                    this.$refs.presenter.update({
                        document: this.document,
                        tasks: this.tasks,
                        annotations: this.annotations,
                        template: this.presenter,
                    });
                }
            },
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
                        _root: ['Unable to serve the request. Please try again later or contact admin for assistance.']
                    };
                    this.errors.default.push(error);
                });
            },
        },
        mounted() {
            this.document_id = 'documentId' in this.$route.params ? this.$route.params.documentId : null;
            if (this.document_id === null) {
                axios.get(config.$api_url + '/annotate/projects/' + this.$route.params.projectId)
                    .then(response => {
                        let payload = response.data;
                        if (payload.data !== null) {
                            this.document = payload.data.document;
                            this.annotation_set = payload.data.annotation_set;
                            this.tasks = this.document.project.tasks;
                            this.presenter = this.document.project.presenter;
                            this.tasks.forEach(task => {
                                if (!(task.id in this.annotations)) {
                                    if (task.type === 'sequence_tagging') {
                                        this.annotations[task.id] = [];
                                    } else {
                                        this.annotations[task.id] = {}
                                    }
                                }
                            });
                            this.completed = false;
                        } else {
                            this.completed = true;
                        }
                        this.$nextTick().then(this.update);
                    });
            } else {
                axios.get(config.$api_url + '/annotate/projects/' + this.$route.params.projectId + '/documents/' + this.document_id)
                    .then(response => {
                        let payload = response.data;
                        if (payload.data !== null) {
                            this.document = payload.data.document;
                            this.annotation_set = payload.data.annotation_set;
                            this.tasks = this.document.project.tasks;
                            this.presenter = this.document.project.presenter;
                            this.tasks.forEach(task => {
                                if (!(task.id in this.annotations)) {
                                    if (task.type === 'sequence_tagging') {
                                        this.annotations[task.id] = [];
                                    } else {
                                        this.annotations[task.id] = {}
                                    }
                                }
                            });
                            this.annotation_set.annotations.forEach(annotation => {
                                let annotations = this.annotations[annotation.task_id];
                                if (Array.isArray(annotations)) {
                                    annotations.push({
                                        id: annotation.id,
                                        label: annotation.label_id,
                                        span: {
                                            start: annotation.span.start,
                                            length: annotation.span.length,
                                        },
                                    });
                                } else {
                                    if (annotation.label_id !== null) {
                                        annotations[annotation.label_id] = true
                                    } else if (annotation.text !== null) {
                                        annotations.text = annotation.text;
                                    }
                                }
                            });
                            this.completed = false;
                        } else {
                            this.completed = true;
                        }
                        this.$nextTick().then(this.update);
                    });
            }
        },
        computed: {
            loading: function () {
                return this.document === null && this.completed === false;
            },
        },
    }
</script>