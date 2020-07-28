<template>
    <div id="presenter"></div>
</template>

<script>
    import $ from 'jquery';
    import Annotator from "../assets/scripts/annotator";
    import Vue from "vue";

    export default {
        name: 'Presenter',
        data() {
            return {
                loading: true,
                presenter: null,
            }
        },
        methods: {
            update({document, tasks, annotations, template}) {
                const Template = Vue.extend({
                    template: template,
                    data() {
                        return {
                            document: document,
                            annotations: annotations,
                            tasks: tasks,
                        }
                    },
                    methods: {
                        update: function () {
                            for (let i = 0; i < this.tasks.length; i++) {
                                let task = this.tasks[i];
                                if (task.type === 'sequence_tagging') {
                                    let annotations = this.annotations[task.id];
                                    let options = task.labels.map(item => ({
                                        'value': item.id,
                                        'label': item.label
                                    }));
                                    let a = new Annotator('sequence_tagging_' + task.id, this.document.text, options);
                                    // load initial annotations
                                    a.setAnnotations(annotations);
                                    // listen to events - delete
                                    a.addEventListener('delete', (annotation) => {
                                        annotations = annotations.filter((e) => {
                                            return e.id !== annotation.id;
                                        });
                                        a.setAnnotations(annotations);
                                    });
                                    // listen to events - update
                                    a.addEventListener('update', (annotation, value) => {
                                        if (annotation.id === 0) { // new annotation
                                            // << new annotation.id should be assigned by the db for now calculate
                                            // the maximum value we have in list and add one.
                                            let new_id = 0;
                                            annotations.forEach((item) => {
                                                if (new_id < item.id)
                                                    new_id = item.id;
                                            });
                                            // >>
                                            annotation.id = new_id + 1;
                                            annotation.label = value;
                                            annotations.push(annotation);
                                        } else {
                                            annotations.forEach((item) => {
                                                if (item.id === annotation.id)
                                                    item.label = value;
                                            });
                                        }
                                        a.setAnnotations(annotations);
                                    });
                                    // initialize annotator
                                    a.initialize();
                                }
                            }
                        },
                        getAnnotations() {
                            let data = [];
                            for (let i = 0; i < this.tasks.length; i++) {
                                let task = this.tasks[i];
                                let annotations = this.annotations[task.id];
                                if (task.type === 'document_labeling') {
                                    // supports multiple annotations for task
                                    for (let key in annotations) {
                                        if (annotations[key]) {
                                            data.push({
                                                task_id: task.id,
                                                label_id: Number.parseInt(key)
                                            });
                                        }
                                    }
                                } else if (task.type === 'sequence_tagging') {
                                    // supports multiple annotations for task
                                    annotations.forEach((item) => {
                                        data.push({
                                            task_id: task.id,
                                            label_id: Number.parseInt(item.label),
                                            span: item.span
                                        });
                                    });
                                } else if (task.type === 'text_to_text') {
                                    data.push({task_id: task.id, text: annotations});
                                }
                            }
                            return data;
                        },
                    }
                });
                this.presenter = new Template().$mount();
                // Presenter
                $('#presenter').html(this.presenter.$el);
            },
            getAnnotations() {
                return this.presenter.getAnnotations();
            }
        },
    }
</script>