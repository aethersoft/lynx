<template>
    <div class="container p-3">
        <!-- Create Project Modal -->
        <div class="modal fade" id="createProjectModal" tabindex="-1" role="dialog"
             aria-labelledby="createProjectModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="createProjectModalLabel">Create Project</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <CreateProjectForm ref="createProjectForm"></CreateProjectForm>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" v-on:click="createProject">Save
                            changes
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div class="btn-toolbar justify-content-between mb-3" role="toolbar" aria-label="Table Toolbar">
            <div class="btn-group mr-2" role="group" aria-label="First group">
                <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#createProjectModal">
                    <span class="oi oi-plus" title="plus" aria-hidden="true"></span>
                </button>
                <button type="button" class="btn btn-primary" v-on:click.stop="deleteSelectedProjects">
                    <span class="oi oi-trash" title="trash" aria-hidden="true"></span>
                </button>
            </div>
            <div>
                <div class="input-group">
                    <div class="input-group-prepend">
                        <span id="validationTooltipUsernamePrepend" class="input-group-text bg-white">Show</span>
                    </div>
                    <select class="custom-select" v-model="limit" v-on:change="setOffset(1)">
                        <option v-for="index in 5" :key="index" v-bind:value="index * 5"
                                v-bind:class="{active:(limit==index * 5)}">{{ index * 5 }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="col"></div>
        </div>
        <div class="table-responsive">
            <table class="table table-hover table-bordered">
                <colgroup>
                    <col style="width: 2em;">
                    <col style="width: 10em;">
                    <col>
                    <col style="width: 5em;">
                </colgroup>
                <thead>
                <tr>
                    <th scope="col" style="width: 3em">
                        <input type="checkbox" aria-label="Select All Projects Checkbox" @click="selectAll"
                               v-model="allSelected">
                    </th>
                    <th scope="col">Project</th>
                    <th scope="col">Description</th>
                    <th scope="col" class="text-center">Actions</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(project, i) in projects" :key="i">
                    <th scope="row">
                        <input type="checkbox" aria-label="Select Project Checkbox" v-model="project.selected">
                    </th>
                    <td>{{ project.name }}</td>
                    <td>{{ project.description }}</td>
                    <td>
                        <div class="d-flex flex-column align-items-center">
                            <div class="btn-group btn-group-sm" role="group" aria-label="First group">
                                <a type="button" class="btn btn-primary"
                                   v-bind:href="'/a/projects/' + project.id">
                                    <span class="oi oi-tag" title="tag" aria-hidden="true"></span>
                                </a>
                                <a type="button" class="btn btn-primary"
                                   v-bind:href="'/projects/' + project.id">
                                    <span class="oi oi-pencil" title="pencil" aria-hidden="true"></span>
                                </a>
                                <a type="button" class="btn btn-primary" href="javascript:void(0)"
                                   v-on:click.stop="deleteProject(project.id)">
                                    <span class="oi oi-trash" title="trash" aria-hidden="true"></span>
                                </a>
                            </div>
                        </div>
                    </td>
                </tr>
                <td colspan="5" class="text-center" v-if="projects.length === 0">
                    <h4 class="display-5">No Projects Found</h4>
                    <p class="text-muted mb-0">Try creating a new project</p>
                </td>
                </tbody>
            </table>
            <nav class="d-flex justify-content-center" aria-label="Pages">
                <ul class="pagination">
                    <li class="page-item">
                        <a class="page-link" href="javascript:void(0)" aria-label="First"
                           v-on:click.stop="setOffset(1)">
                            <span aria-hidden="true">&laquo;</span>
                            <span class="sr-only">First</span>
                        </a>
                    </li>
                    <li class="page-item" v-for="i in 5" v-bind:class="{ active : (i === 3) }" :key="i">
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
    </div>
</template>

<!--suppress NpmUsedModulesInstalled -->
<script>
    import $ from 'jquery';
    import axios from 'axios';
    import config from "../config";
    import CreateProjectForm from "@/components/CreateProjectForm";

    export default {
        name: 'Projects',
        components: {CreateProjectForm},
        data() {
            return {
                offset: 1,
                limit: 5,
                num_pages: 1,
                pages: 1,
                projects: [],
                allSelected: false,
            }
        },
        methods: {
            selectAll: function () {
                this.projects.forEach(p => {
                    p.selected = !this.allSelected;
                });
            },
            deleteProject: function (pid) {
                axios.delete(config.$api_url + '/projects/' + pid)
                    .then(response => {
                        let payload = response.data;
                        if (payload.status !== 'success') {
                            console.error(payload);
                        } else {
                            this.retrieveProjects();
                        }
                    });
            },
            deleteSelectedProjects: function () {
                this.projects.filter(p => p.selected).forEach(p => {
                    this.deleteProject(p.id);
                });
            },
            retrieveProjects: function () {
                this.projects = [];
                axios.get(config.$api_url + '/projects?limit=' + this.limit + '&offset=' + this.offset)
                    .then(response => {
                        let payload = response.data;
                        if (payload.status === 'success') {
                            let pagination = payload.data.pagination;
                            this.pages = pagination.pages;
                            this.projects = pagination.items;
                        }
                    })
            },
            createProject: function () {
                this.$refs.createProjectForm.submit().then(() => {
                    this.retrieveProjects();
                    $('#createProjectModal .close').click();
                })
            },
            setOffset: function (offset) {
                this.offset = offset;
                this.retrieveProjects();
            },
        },
        mounted() {
            this.retrieveProjects();
        },
        computed: {
            loading: function () {
                return this.projects !== null;
            },
        },
    }
</script>