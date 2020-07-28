import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './views/Home.vue'

Vue.use(VueRouter);

let sidebar = {
    heading: null,
    items: [{
        name: 'Dashboard',
        to_name: 'ProjectDashboard',
        icon: 'dashboard',
        level: 0,
    }, {
        name: 'Reports',
        to_name: 'ProjectReports',
        icon: 'graph',
        level: 0,
    }, {
        name: 'Documents',
        to_name: 'ProjectDocuments',
        icon: 'document',
        level: 0,
    }, {
        name: 'Tasks',
        to_name: 'ProjectTasks',
        icon: 'task',
        level: 0,
    }, {
        name: 'Presenter',
        to_name: 'ProjectPresenter',
        icon: 'eye',
        level: 0,
    }, {
        name: 'Settings',
        to_name: 'ProjectSettings',
        icon: 'cog',
        level: 0,
    },
    ]
};

const routes = [
    {
        path: '/',
        name: 'Home',
        meta: {
            sidebar: null,
            navbar: {
                active: 'home'
            }
        },
        component: Home
    },
    {
        path: '/projects',
        name: 'Projects',
        meta: {
            sidebar: null,
            navbar: {
                active: 'projects'
            }
        },
        component: () => import('./views/Projects.vue')
    },
    {
        path: '/about',
        name: 'About',
        meta: {
            sidebar: null,
            navbar: {
                active: 'about'
            }
        },
        component: () => import('./views/About.vue')
    },
    {
        path: '/signup',
        name: 'Sign Up',
        meta: {
            sidebar: null,
            navbar: {
                active: 'home'
            }
        },
        component: () => import('./views/SignUp.vue')
    },
    {
        path: '/signin',
        name: 'Sign In',
        meta: {
            sidebar: null,
            navbar: {
                active: 'home'
            }
        },
        component: () => import('./views/SignIn.vue')
    },
    {
        path: '/projects/:projectId/',
        redirect: to => {
            const {params} = to;
            return {name: 'ProjectDashboard', params: {projectId: params.projectId}}
        }
    },
    {
        path: '/projects/:projectId/dashboard',
        name: 'ProjectDashboard',
        meta: {
            sidebar: sidebar,
            navbar: {
                active: 'projects'
            }
        },
        component: () => import('./views/ProjectDashboard.vue')
    },
    {
        path: '/projects/:projectId/reports',
        name: 'ProjectReports',
        meta: {
            sidebar: sidebar,
            navbar: {
                active: 'projects'
            }
        },
        component: () => import('./views/ProjectReports.vue')
    },
    {
        path: '/projects/:projectId/documents',
        name: 'ProjectDocuments',
        meta: {
            sidebar: sidebar,
            navbar: {
                active: 'projects'
            }
        },
        component: () => import('./views/ProjectDocuments.vue')
    },
    {
        path: '/projects/:projectId/tasks',
        name: 'ProjectTasks',
        meta: {
            sidebar: sidebar,
            navbar: {
                active: 'projects'
            }
        },
        component: () => import('./views/ProjectTasks.vue')
    },
    {
        path: '/projects/:projectId/settings',
        name: 'ProjectSettings',
        meta: {
            sidebar: sidebar,
            navbar: {
                active: 'projects'
            }
        },
        component: () => import('./views/ProjectSettings.vue')
    },
    {
        path: '/projects/:projectId/presenter',
        name: 'ProjectPresenter',
        meta: {
            sidebar: sidebar,
            navbar: {
                active: 'projects'
            }
        },
        component: () => import('./views/ProjectPresenter.vue')
    },
    {
        path: '/a/projects/:projectId',
        name: 'AnnotateProject',
        meta: {
            sidebar: null,
            navbar: {
                active: 'home'
            }
        },
        component: () => import('./views/Annotate.vue')
    },
    {
        path: '/a/projects/:projectId/documents',
        name: 'AssignedDocuments',
        meta: {
            sidebar: null,
            navbar: {
                active: 'home'
            }
        },
        component: () => import('./views/AssignedDocuments.vue')
    },
    {
        path: '/a/projects/:projectId/documents/:documentId',
        name: 'AnnotateDocument',
        meta: {
            sidebar: null,
            navbar: {
                active: 'home'
            }
        },
        component: () => import('./views/Annotate.vue')
    },
    {
        path: '*',
        name: 'PageNotFound',
        meta: {
            sidebar: null,
            navbar: {
                active: 'home'
            }
        },
        component: () => import('./views/PageNotFound.vue')
    },
    {
        path: '/sidebar_test',
        name: 'sidebar_test',
        meta: {
            sidebar: sidebar,
            navbar: {
                active: 'home'
            }
        },
        component: () => import('./views/Home.vue')
    },
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    linkActiveClass: 'active',
    routes
});

export default router
