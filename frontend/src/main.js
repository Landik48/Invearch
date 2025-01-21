import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import {createRouter, createMemoryHistory, createWebHistory} from 'vue-router'
import Startups from './components/Startups.vue'
import Home from './components/Home.vue'
import Profile from './components/Profile.vue'
import Register from './components/Register.vue'
import Auth from './components/Auth.vue'
import AOS from 'aos';
import 'aos/dist/aos.css';

AOS.init()

const routes = [
    {
        path: '/',
        component: Home,
     },
    {
        path: '/startups',
        component: Startups
     },
     {
        path: '/profile',

        component: Profile
     },
     {
        path: '/register',
        component: Register
     },
     {
        path: '/auth',
        component: Auth
     }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    linkActiveClass: 'active-router',
})

const app = createApp(App)
app.config.devtools = false;
app.use(router).mount('#app')