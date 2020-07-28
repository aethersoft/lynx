<template>
    <div class="container p-3">
        <div class="table-responsive">
            <div class="btn-toolbar justify-content-between mb-3" role="toolbar"
                 aria-label="Toolbar">
                <div class="input-group">
                    <div class="input-group-prepend">
                        <span class="input-group-text bg-white" id="viewLimitPrepend">Show</span>
                    </div>
                    <select class="custom-select" v-model="limit" v-on:change="offset=1;retrieveDocuments()">
                        <option v-for="index in 5" :key="index" v-bind:value="index * 5"
                                v-bind:class="{active:(limit === index * 5)}">
                            {{ index * 5 }}
                        </option>
                    </select>
                </div>
                <div class="col"></div>
                <div class="input-group mr-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text bg-white" id="statusNoneFilterSelectorPrepend">
                            <span class="oi oi-flag" title="flag" aria-hidden="true"></span>
                        </span>
                    </div>
                    <select class="custom-select" id="statusNoneFilterSelector"
                            v-model="filters.flagged" v-on:change="retrieveDocuments()">
                        <option value="none">None</option>
                        <option value="true">Flagged</option>
                        <option value="false">Not Flagged</option>
                    </select>
                </div>
                <div class="input-group">
                    <div class="input-group-prepend">
                            <span class="input-group-text bg-white" id="validationTooltipUsernamePrepend">
                                <span class="oi oi-circle-check" title="flag" aria-hidden="true"></span>
                            </span>
                    </div>
                    <select class="custom-select" id="statusFilterSelector"
                            v-model="filters.status" v-on:change="retrieveDocuments()">
                        <option value="none">None</option>
                        <option value="completed">Completed</option>
                        <option value="skipped">Skipped</option>
                        <option value="active">Active</option>
                    </select>
                </div>
            </div>
            <table class="table table-bordered">
                <thead>
                <tr>
                    <th scope="col">Text</th>
                    <th scope="col" class="text-center">Status</th>
                    <th scope="col" class="text-center">Actions</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(d, index) in documents" :key="index">
                    <td>
                        <p class="lead">{{ d.text }}</p>
                    </td>
                    <td>
                            <span class="badge badge-pill badge-primary mr-1">
                                <span class="oi oi-flag" title="flag" aria-hidden="true"
                                      v-if="d.annotation_set.flagged">
                                </span>
                            </span>
                        <span class="badge badge-pill badge-primary mr-1">
                                <span class="oi oi-media-skip-forward" title="media-skip-forward"
                                      aria-hidden="true" v-if="d.annotation_set.skipped">
                                </span>
                            </span>
                        <span class="badge badge-pill badge-primary mr-1">
                                <span class="oi oi-check" title="check" aria-hidden="true"
                                      v-if="d.annotation_set.completed">
                                </span>
                            </span>
                    </td>
                    <td>
                        <div class="d-flex flex-column align-items-center">
                            <router-link type="button" class="btn btn-primary"
                                         :to="{name:'AnnotateDocument', params: {projectId:$route.params.projectId, documentId:d.id}}">
                                <span class="oi oi-tag" title="tag" aria-hidden="true"></span>
                            </router-link>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
            <nav class="d-flex justify-content-center" aria-label="Pages">
                <ul class="pagination">
                    <li class="page-item">
                        <a class="page-link" href="javascript:void(0)" aria-label="First"
                           v-on:click.stop="offset=1;retrieveDocuments()">
                            <span aria-hidden="true">&laquo;</span>
                            <span class="sr-only">First</span>
                        </a>
                    </li>
                    <li class="page-item" v-for="i in 5" :key="i"
                        v-bind:class="{ active : (i === 3) }">
                        <a class="page-link" href="javascript:void(0)"
                           v-on:click.stop="offset=offset + (i - 3);retrieveDocuments()"
                           v-if="offset+(i-3)>0 && offset+(i-3)<=pages">
                            {{ offset+(i-3) }}
                        </a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="javascript:void(0)" aria-label="Last"
                           v-on:click.stop="offset=pages;retrieveDocuments()">
                            <span aria-hidden="true">&raquo;</span>
                            <span class="sr-only">Last</span>
                        </a>
                    </li>
                </ul>
            </nav>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import config from "../config";

    export default {
        name: 'AssignedDocuments',
        data() {
            return {
                offset: 1,
                limit: 10,
                pages: 1,
                filters: {
                    flagged: 'none',
                    status: 'none',
                },
                documents: [],
                errors: [],
            }
        },
        methods: {
            retrieveDocuments: function () {
                let documents_url = config.$api_url + '/annotate/projects/' + this.$route.params.projectId + '/documents?' +
                    'offset=' + this.offset +
                    '&limit=' + this.limit +
                    '&flagged=' + this.filters.flagged +
                    '&status=' + this.filters.status;
                axios.get(documents_url)
                    .then(response => {
                        let payload = response.data;
                        if (payload.status === 'success') {
                            let pagination = payload.data.pagination;
                            this.offset = pagination.page;
                            this.pages = pagination.pages;
                            this.documents = pagination.items;
                        } else {
                            console.error(payload);
                        }
                    });
            },
        },
        mounted() {
            this.retrieveDocuments()
        },
        computed: {
            loading: function () {
                return this.documents === null;
            },
        },
    }
</script>