<template>
    <div class="w-100 p-3">
        <CreateProjectForm ref="createProjectForm"></CreateProjectForm>
        <button type="button" class="btn btn-primary" v-on:click="updateChanges">Save</button>
        <hr>
        <CreateProjectUserRolesForm></CreateProjectUserRolesForm>
    </div>
</template>


<!--suppress NpmUsedModulesInstalled -->
<script>
    import CreateProjectUserRolesForm from '@/components/CreateUserRolesForm.vue';
    import CreateProjectForm from '@/components/CreateProjectForm.vue';

    export default {
        name: 'ProjectSettings',
        components: {CreateProjectForm, CreateProjectUserRolesForm},
        methods: {
            updateChanges() {
                this.$refs.createProjectForm.submit().then(() => {
                    this.$store.dispatch('success', {
                        title: 'Project',
                        body: 'Project update success.'
                    });
                });
            }
        }
    }
</script>