<template>
    <Banner v-if="!isAuthenticated"></Banner>
    <div class="container p-3" v-else>
        <AssignedProjects></AssignedProjects>
    </div>
</template>

<!--suppress NpmUsedModulesInstalled -->
<script>
    import Banner from '@/components/Banner.vue';
    import AssignedProjects from "./AssignedProjects";

    export default {
        name: 'Home',
        components: {
            AssignedProjects,
            Banner
        },
        computed: {
            isAuthenticated: function () {
                return this.$store.getters.isAuthenticated;
            }
        },
    }
</script>