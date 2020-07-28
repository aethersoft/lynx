<template>
    <div id="sidebar-wrapper" v-if="typeof $route.meta.sidebar !== 'undefined'">
        <div class="sidebar-heading" v-if="$route.meta.sidebar.heading !== null">{{ $route.meta.sidebar.heading }}</div>
        <nav class="nav nav-pills flex-column">
            <router-link class="nav-link"
                         v-for="item in $route.meta.sidebar.items"
                         :to="{ name : item.to_name, params: { projectId: $route.params.projectId }}"
                         :key="item.to_name">
                <div class="d-flex flex-row align-items-center" :class="{'pl-3': (item.level === 1)}">
                    <span class="oi" aria-hidden="true" :class="'oi-' + item.icon" :title="item.icon"></span>
                    <p class="sidebar-item-name">{{ item.name }}</p>
                </div>
            </router-link>
        </nav>
    </div>
</template>

<style type="scss" scoped>
    #sidebar-wrapper {
        min-height: 100%;
        -webkit-transition: margin .25s ease-out;
        -moz-transition: margin .25s ease-out;
        -o-transition: margin .25s ease-out;
        transition: margin .25s ease-out;
        padding: 1rem;
        min-width: 200px;
    }

    #sidebar-wrapper .sidebar-heading {
        padding: 0.875rem 1.25rem;
        font-size: 1.2rem;
    }

    .sidebar-item-name {
        color: rgba(0, 0, 0, 0.5);
        font-family: Inter, sans-serif;
        font-size: 16px;
        line-height: 24px;
        font-weight: 400;
        margin: 0;
        padding: 0.5rem 0 0.5rem 20px;
    }

    @media (min-width: 768px) {
        #sidebar-wrapper {
            margin-left: 0;
        }
    }

</style>

<script>
    export default {
        name: 'Sidebar',
    }
</script>