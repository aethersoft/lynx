<template>
    <div class="w-100 p-3">
        <div class="btn-toolbar justify-content-between mb-3" role="toolbar" aria-label="Table Toolbar">
            <form id="document-upload" method="post" enctype="multipart/form-data"
                  v-on:submit.prevent="submit">
                <div class="input-group">
                    <div class="custom-file">
                        <input type="file" name="file" class="custom-file-input" id="validatedDocumentUpload">
                        <label class="custom-file-label" for="validatedDocumentUpload">Choose file</label>
                    </div>
                    <div class="input-group-append">
                        <button class="btn btn-sm btn-outline-primary" type="submit">
                            <i data-feather="upload"></i> Upload
                            <div class="progress" style="height: 2px;">
                                <div class="progress-bar" role="progressbar" aria-valuenow="25"
                                     aria-valuemin="0" aria-valuemax="100"
                                     :style="{  width: upload.progress + '%' }"
                                     :class="{
                                        'bg-warning': upload.status === 'ready',
                                        'bg-success': upload.status === 'success' ,
                                        'bg-danger': upload.status === 'failed'
                                }"></div>
                            </div>
                        </button>
                    </div>
                </div>
            </form>
            <form>
                <div class="input-group">
                    <div class="input-group-prepend">
                        <span class="input-group-text bg-white" id="validationTooltipUsernamePrepend">Show</span>
                    </div>
                    <select class="custom-select" v-model="limit" v-on:change="setOffset(1)">
                        <option v-for="index in 5" :key="index"
                                :value="index * 5"
                                :class="{'active':(limit === index * 5)}">
                            {{index * 5}}
                        </option>
                    </select>
                </div>
            </form>
        </div>
        <div class="table-responsive" v-if="!loading">
            <table class="table table-bordered">
                <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Text</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="document in documents" :key="document.id">
                    <th scope="row">{{ document.id }}</th>
                    <td>{{ document.text }}</td>
                </tr>
                </tbody>
            </table>
        </div>
        <nav class="d-flex w-auto" aria-label="Pages">
            <ul class="pagination">
                <li class="page-item">
                    <a class="page-link" href="javascript:void(0)" aria-label="First"
                       v-on:click.stop="setOffset(1)">
                        <span aria-hidden="true">&laquo;</span>
                        <span class="sr-only">First</span>
                    </a>
                </li>
                <li class="page-item" v-for="i in 5" :class="{ active : (i === 3) }" :key="i">
                    <a class="page-link" href="javascript:void(0)"
                       v-on:click.stop="setOffset(offset + (i - 3))"
                       v-if="offset+(i-3)>0 && offset+(i-3)<=pages">
                        {{ offset+(i-3) }}
                    </a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="javascript:void(0)" aria-label="Last"
                       v-on:click.stop="setOffset(pages)">
                        <span aria-hidden="true">&raquo;</span>
                        <span class="sr-only">Last</span>
                    </a>
                </li>
            </ul>
        </nav>
    </div>
</template>

<script>
    import $ from 'jquery';
    import axios from 'axios';
    import config from "../config";

    export default {
        name: 'ProjectDocuments',
        data() {
            return {
                offset: 1,
                limit: 20,
                pages: 1,
                documents: null,
                upload: {
                    progress: 0,
                    status: 'ready',
                },
                errors: {},
            }
        },
        methods: {
            retrieveDocuments: function () {
                let documents_url = config.$api_url + '/projects/' + this.$route.params.projectId + '/documents?offset=' + this.offset + '&limit=' + this.limit;
                axios.get(documents_url)
                    .then(response => {
                        let payload = response.data;
                        if (payload.status === 'success') {
                            // noinspection JSUnresolvedVariable
                            this.pages = payload.data.pagination.pages;
                            // noinspection JSUnresolvedVariable
                            this.documents = payload.data.pagination.items;
                        } else {
                            console.error(payload);
                        }
                    });
            },
            submit: function () {
                const self = this;
                let form = $('#document-upload')[0];
                let formData = new FormData(form);
                let url = config.$api_url + '/projects/' + this.$route.params.projectId + '/documents';
                self.upload = {
                    progress: 0,
                    status: 'ready',
                };
                axios.post(url, formData, {
                        headers: {'Content-Type': 'multipart/form-data'},
                        onUploadProgress: function (progressEvent) {
                            self.upload.progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                        },
                    }
                ).then(function (response) {
                    let payload = response.data;
                    if (payload.status === 'success') {
                        self.upload.status = 'success';
                        self.retrieveDocuments();
                    } else {
                        self.upload.status = 'failed';
                        console.error(payload.data);
                    }
                }).catch(function (error) {
                    self.upload.status = 'failed';
                    console.error(error);
                });
            },
            setOffset(offset) {
                this.offset = offset;
                this.retrieveDocuments();
            }
        },
        mounted() {
            this.retrieveDocuments()
        },
        computed: {
            loading: function () {
                return this.documents === null;
            },
            auth_token: function () {
                return this.$store.getters.getAuthToken;
            },
        },
    }
</script>