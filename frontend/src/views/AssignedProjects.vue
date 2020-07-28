<template>
    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4">
        <div class="col mb-3" v-for="project in projects" :key="project.id">
            <div class="card">
                <img class="card-img-top" alt="..." src="../assets/images/coding-amico.png">
                <div class="card-body">
                    <h5 class="card-title">{{ project.name }}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">{{ project.description }}</h6>
                    <p class="card-text">{{ project.full_description }}</p>
                    <a class="card-link" v-bind:href="'/a/projects/' + project.id">Annotate</a>
                    <a class="card-link" v-bind:href="'/a/projects/' + project.id + '/documents'">View</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import config from "../config";

    export default {
        name: 'AnnotateProjects',
        data() {
            return {
                loading: true,
                offset: 1,
                limit: 5,
                num_pages: 1,
                pages: 1,
                projects: [],
            }
        },
        methods: {
            retrieveProjects: function () {
                this.projects = [];
                axios.get(config.$api_url + '/annotate/projects?limit=' + this.limit + '&offset=' + this.offset)
                    .then(response => {
                        let payload = response.data;
                        if (payload.status === 'success') {
                            // noinspection JSUnresolvedVariable
                            let pagination = payload.data.pagination;
                            this.pages = pagination.pages;
                            this.projects = pagination.items;
                        }
                    });
            }
        },
        mounted() {
            this.retrieveProjects();
            this.loading = false;
        },
        computed: {
            isAuthenticated: function () {
                return this.$store.getters.isAuthenticated;
            }
        },
        delimiters: ['{(', ')}']
    }
</script>