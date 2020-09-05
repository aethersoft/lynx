<template>
    <div class="media" style="min-width: 256px;">
        <div class="media-body">
            <template v-if="isAuthenticated">
                <p class="avatar-name">{{ user.first_name }} {{ user.last_name }}</p>
                <p class="avatar-username">Signed in as {{ user.username }}</p>
            </template>
            <template v-else>
                <p class="avatar-username">Anonymous</p>
            </template>
        </div>
    </div>
</template>

<style>
    .avatar-name {
        color: rgba(0, 0, 0, 0.8);
        font-size: 24px;
        padding: 8px 16px 0;
    }

    .avatar-username {
        color: rgba(0, 0, 0, 0.5);
        font-size: 12px;
        font-weight: 400;
        line-height: 1.25;
        padding: 0 16px 8px;
    }
</style>

<script>
    export default {
        name: 'Avatar',
        computed: {
            user: function () {
                return this.$store.getters.getUser;
            },
            isAuthenticated: function () {
                return this.$store.getters.isAuthenticated;
            }
        },
    }
</script>