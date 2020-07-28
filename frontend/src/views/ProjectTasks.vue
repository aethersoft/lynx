<template>
    <div class="w-100 p-3">
        <div class="btn-toolbar justify-content-between mb-3" role="toolbar" aria-label="Table Toolbar">
            <div class="btn-group mr-2" role="group" aria-label="First group">
                <button type="button" class="btn btn-primary" v-on:click="showCreateTaskForm()">
                    <span class="oi oi-plus" title="plus" aria-hidden="true"></span>
                </button>
            </div>
            <!-- Create Project Modal -->
            <div class="modal fade" id="createTaskModal" tabindex="-1" role="dialog"
                 aria-labelledby="createTaskModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-lg" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="createTaskModalLabel">Create Task</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <CreateTaskForm ref="CreateTaskForm"></CreateTaskForm>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary" v-on:click="createTask">Save
                                changes
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="table-responsive" v-if="!loading">
            <table class="table table-hover table-bordered">
                <thead>
                <tr>
                    <th scope="col" style="width: 5em">#</th>
                    <th scope="col">Name</th>
                    <th scope="col">Description</th>
                    <th scope="col">Labels</th>
                    <th scope="col" style="width: 5em">Actions</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(task, i) in tasks" :key="i">
                    <th scope="row">1</th>
                    <td>{{task.name}}</td>
                    <td>{{task.description}}</td>
                    <td>
                    <span class="badge badge-pill mr-1" v-for="(label, j) in task.labels" :key="j"
                          v-bind:style="{color: label.properties.color, background: label.properties.background}">{{label.label}}</span>
                    </td>
                    <td>
                        <div class="btn-group" role="group" aria-label="Basic example">
                            <a v-on:click.stop="showCreateTaskForm(task.id)" href="javascript:void(0)"
                               class="btn btn-primary btn-sm">
                                <span class="oi oi-pencil" title="pencil" aria-hidden="true"></span>
                            </a>
                            <a class="btn btn-primary btn-sm" href="javascript:void(0)"
                               v-on:click.stop="deleteTask(task.id)">
                                <span class="oi oi-trash" title="trash" aria-hidden="true"></span>
                            </a>
                        </div>
                    </td>
                </tr>
                <td colspan="5" class="text-center" v-if="tasks.length === 0">
                    <h4 class="display-5">No Tasks Found</h4>
                    <p class="text-muted mb-0">Try creating a new task</p>
                </td>
                </tbody>
            </table>
        </div>
    </div>
</template>

<!--suppress NpmUsedModulesInstalled -->
<script>
    import axios from 'axios';
    import config from "../config";

    import CreateTaskForm from '@/components/CreateTaskForm.vue';
    import $ from "jquery";

    export default {
        name: 'ProjectTasks',
        components: {CreateTaskForm},
        data() {
            return {
                tasks: null,
            }
        },
        methods: {
            deleteTask: function (task_id) {
                axios.delete(config.$api_url + '/projects/' + this.$route.params.projectId + '/tasks/' + task_id)
                    .then(response => {
                        let payload = response.data;
                        if (payload.status !== 'success') {
                            console.error(payload);
                        } else {
                            this.retrieveTasks();
                        }
                    });
            },
            retrieveTasks: function () {
                let tasks_url = config.$api_url + '/projects/' + this.$route.params.projectId + '/tasks';
                axios.get(tasks_url)
                    .then(response => {
                        let payload = response.data;
                        if (payload.status !== 'success') {
                            console.error(payload);
                        } else {
                            this.tasks = payload.data;
                        }
                    })
            },
            createTask: function () {
                this.$refs.CreateTaskForm.submit().then(() => {
                    this.retrieveTasks();
                    $('#createTaskModal .close').click();
                })
            },
            showCreateTaskForm(task_id = null) {
                this.$refs.CreateTaskForm.update(task_id);
                $('#createTaskModal').modal({show: true});
            },
            initialize: function () {
                this.retrieveTasks();
            },
        },
        mounted() {
            this.initialize();
        },
        computed: {
            loading: function () {
                return this.tasks === null;
            },
        },
    }
</script>