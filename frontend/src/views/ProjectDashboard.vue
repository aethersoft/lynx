<template>
    <div class="p-3 w-100">
        <div class="jumbotron jumbotron-fluid">
            <div class="container">
                <h1 class="display-4">{{ project.name }}</h1>
                <p class="lead">{{ project.description }}</p>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import config from "../config";

    export default {
        name: 'ProjectDashboard',
        data() {
            return {
                project: {},
            }
        },
        mounted() {
            let project_url = config.$api_url + '/projects/' + this.$route.params.projectId;
            axios.get(project_url)
                .then(response => {
                    let payload = response.data;
                    this.project = payload.data;
                });
        },
    }
</script>