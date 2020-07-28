<template>
    <form id="tasks-form" class="form-page" method="post" v-on:submit.prevent="submit" v-if="!loading">
        <div class="form-group">
            <label for="inputName" class="col-sm-2 col-form-label">Name</label>
            <div class="col-sm-10">
                <input id="inputName" name="name" type="text" class="form-control" placeholder="Task Name"
                       v-model="task.name">
            </div>
        </div>
        <div class="form-group">
            <label for="taskTypeSelect" class="col-sm-2 col-form-label">Type</label>
            <div class="col-sm-10">
                <select class="custom-select my-1 mr-sm-2" id="taskTypeSelect" name="type" v-model="task.type">
                    <option v-bind:value="type.value" v-bind:class="{selected: (type.value===task.type)}"
                            v-for="(type, i) in task_types" :key="i">
                        {{type.text}}
                    </option>
                </select>
            </div>
        </div>
        <div class="form-group">
            <label for="taskDescription" class="col-sm-2 col-form-label">Description</label>
            <div class="col-sm-10">
                <textarea class="form-control" id="taskDescription" name="description" rows="2"
                          placeholder="Task Description" v-model="task.description"></textarea>
            </div>
        </div>
        <div class="form-group">
            <label for="taskDescription" class="col-sm-2 col-form-label">Labels</label>
            <div class="col-sm-10">
                <table id="label-table" class="table">
                    <thead>
                    <tr>
                        <th scope="col">
                            <input type="checkbox" aria-label="Select all labels"
                                   v-model="allLabelsSelected" @click="selectAllLabels">
                        </th>
                        <th scope="col">Label</th>
                        <th scope="col">Background Color</th>
                        <th scope="col">Text Color</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="(label, i) in task.labels" :key="i">
                        <td><input type="checkbox" aria-label="Select all labels" v-model="label.selected"></td>
                        <td><input type="text" class="form-control" v-model="label.label"></td>
                        <td><input type="text" class="form-control" v-model="label.properties.background"></td>
                        <td><input type="text" class="form-control" v-model="label.properties.color"></td>
                    </tr>
                    </tbody>
                </table>
                <div class="form-row pb-3">
                    <div class="col-2">
                        <button class="btn btn-primary btn-sm w-100" type="button" role="button"
                                v-on:click="addLabel">
                            <span>Add</span>
                        </button>
                    </div>
                    <div class="col-2">
                        <button class="btn btn-primary btn-sm w-100" type="button" role="button"
                                v-on:click="deleteLabel">
                            <span>Delete</span>
                        </button>
                    </div>
                </div>
                <div class="form-row justify-content-end" hidden>
                    <div class="col-2">
                        <button class="btn btn-success btn-sm w-100" type="submit">
                            <span>Save</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </form>
</template>

<script>
    import axios from 'axios';
    import config from "../config";

    export default {
        name: 'CreateTaskForm',
        data() {
            return {
                task_id: null,
                task_types: [
                    {value: 'document_labeling', text: 'Document Labeling'},
                    {value: 'sequence_tagging', text: 'Sequence Tagging'},
                    {value: 'text_to_text', text: 'Text to Text'},
                ],
                task: null,
                allLabelsSelected: false,
            }
        },
        methods: {
            selectAllLabels: function () {
                this.task.labels.forEach(l => {
                    l.selected = !this.allLabelsSelected;
                });
            },
            submit: function () {
                return new Promise((resolve, reject) => {
                    if (window.FormData !== undefined) {
                        const labels = this.task.labels.map((label) => {
                            const l = Object.assign({}, label);
                            delete l.selected;
                            return l
                        });
                        let data = {
                            name: this.task.name,
                            description: this.task.description,
                            type: this.task.type,
                            labels: labels,
                        };
                        let url = config.$api_url + '/projects/' + this.$route.params.projectId + '/tasks';
                        let promise;
                        if (this.task_id === null) {
                            promise = axios.post(url, data);
                        } else {
                            url += '/' + this.task_id;
                            promise = axios.put(url, data);
                        }
                        promise.then(function (response) {
                            const payload = response.data;
                            if (payload.status === 'success') {
                                resolve(payload.data);
                            } else {
                                console.error(payload.data);
                                reject([payload].data);
                            }
                        }).catch((error) => {
                            console.error(error);
                            reject(error);
                        });
                    } else {
                        reject({'_root': ['Form data is not defined.']});
                    }
                });
            },
            addLabel: function () {
                this.task.labels.push({
                    id: null,
                    label: 'New Label',
                    properties: {background: '#fafffa', color: '#343a40'},
                    selected: false,
                });
            },
            deleteLabel: function () {
                this.task.labels = this.task.labels.filter((l) => !l.selected);
            },
            update: function (task_id = null) {
                this.task_id = task_id;
                // Load the task here if task id is not null
                if (this.task_id !== null) {
                    let url = config.$api_url + '/projects/' + this.$route.params.projectId + '/tasks/' + this.task_id;
                    let self = this;
                    axios.get(url).then(function (response) {
                        let payload = response.data;
                        if (response.data.status === 'success') {
                            let task = payload.data;
                            self.task = {
                                name: task.name,
                                description: task.description,
                                type: task.type,
                                labels: task.labels,
                            };
                            this.$store.dispatch('success', {
                                title: 'Task',
                                body: 'Task created!'
                            });
                        } else {
                            console.error(payload.data);
                        }
                    }).catch(console.error);
                } else {
                    this.task = {
                        name: '',
                        type: 'document_labeling',
                        description: '',
                        labels: [],
                    }
                }
            },
        },
        mounted() {
            this.update();
        },
        computed: {
            loading: function () {
                return this.task === null;
            },
        },
    }
</script>