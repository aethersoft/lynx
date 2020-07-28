<template>
    <div class="w-100 h-100 p-3">
        <ul class="nav nav-pills pb-3" id="pills-tab" role="tablist">
            <li class="nav-item">
                <a class="nav-link active" id="pills-preview-tab" data-toggle="pill" href="#pills-preview"
                   role="tab" aria-controls="pills-preview" aria-selected="false" v-on:click="update">Preview</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" id="pills-sourcecode-tab" data-toggle="pill" href="#pills-sourcecode"
                   role="tab" aria-controls="pills-sourcecode" aria-selected="true">Source</a>
            </li>
        </ul>
        <div class="tab-content" id="pills-content">
            <div class="tab-pane fade show active" id="pills-preview" role="tabpanel"
                 aria-labelledby="pills-preview-tab">
                <Presenter ref="presenter"></Presenter>
            </div>
            <div class="tab-pane fade" id="pills-sourcecode" role="tabpanel" aria-labelledby="pills-sourcecode-tab">
                <div class="card">
                    <label for="sourcecode" hidden></label>
                    <textarea id="sourcecode" v-model="presenter"></textarea>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    // import CodeMirror from "codemirror";
    import Presenter from "../components/Presenter";
    import axios from "axios";
    import config from "../config";
    // import 'codemirror/lib/codemirror.css'

    export default {
        components: {Presenter},
        data() {
            return {
                document: {text: ''},
                tasks: {},
                annotations: {},
                project: null,
                presenter: '',
            }
        },
        methods: {
            update() {
                if (this.project !== null)
                    this.$refs.presenter.update({
                        document: this.document,
                        tasks: this.tasks,
                        annotations: this.annotations,
                        template: this.presenter,
                    });
            },
        },
        mounted() {
            axios.get(config.$api_url + '/annotate/projects/' + this.$route.params.projectId)
                .then(response => {
                    let payload = response.data;
                    if (payload.data !== null) {
                        this.document = payload.data.document;
                        this.annotation_set = payload.data.annotation_set;
                        this.project = payload.data.document.project;
                        this.tasks = payload.data.document.project.tasks;
                        this.presenter = payload.data.document.project.presenter;
                        this.tasks.forEach(task => {
                            if (!(task.id in this.annotations)) {
                                if (task.type === 'sequence_tagging') {
                                    this.annotations[task.id] = [];
                                } else {
                                    this.annotations[task.id] = {}
                                }
                            }
                        });
                    }
                    this.$nextTick().then(this.update);
                });
        },
    }
</script>