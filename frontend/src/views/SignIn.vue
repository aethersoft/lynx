<template>
    <div class="page page-align-center">
        <form class="form-signin" @submit.prevent="signin">
            <img class="mb-4" src="../assets/images/logo.svg" alt="Lynx" width="72"
                 height="72">
            <h1 class="h3 mb-3 font-weight-normal">Please sign in</h1>
            <div class="form-label-group">
                <input type="text" id="inputUsername" class="form-control" placeholder="Username" required=""
                       autofocus="" v-model="username">
                <label for="inputUsername" class="w-100 text-left">Username</label>
            </div>
            <div class="form-label-group">
                <input type="password" id="inputPassword" class="form-control" placeholder="Password" required=""
                       v-model="password">
                <label for="inputPassword" class="w-100 text-left">Password</label>
            </div>
            <button class="btn btn-lg btn-primary btn-block" type="submit">Sign In</button>
        </form>
    </div>
</template>

<style type="scss" scoped>
    .page {
        margin-top: -112px;
        padding-top: 112px;
        min-height: 100vh;
        width: 100%;
        overflow: hidden;
    }

    .page-align-center {
        display: flex;
        flex-flow: column;
    }

    .form-signin {
        width: 100%;
        max-width: 420px;
        padding: 15px;
        margin: auto;
        text-align: center;
    }
</style>

<!--suppress NpmUsedModulesInstalled -->
<script>
    export default {
        name: 'SignInForm',
        data() {
            return {
                username: '',
                password: '',
                errors: {
                    _root: null,
                },
            }
        },
        methods: {
            signin: function () {
                let username = this.username;
                let password = this.password;
                this.$store.dispatch('signin', {username, password})
                    .then((payload) => {
                        // redirect as required
                        let url = new URL(location.href);
                        let redirect = url.searchParams.get('redirect');
                        if (redirect !== null) {
                            this.$router.push(redirect);
                        } else if ('redirect' in payload) {
                            this.$router.push(payload.redirect);
                        }
                        this.$router.push('/');
                        this.$store.dispatch('success', {
                            title: 'Authentication',
                            body: 'Login successful!'
                        });
                    })
                    .catch(error => {
                        this.$store.dispatch('error', {
                            title: 'Authentication',
                            body: error['data']['_root'][0],
                        });
                    });
            }
        },
    }
</script>