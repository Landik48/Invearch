import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createMemoryHistory } from 'vue-router'
import Startups from './components/Startups.vue'
import Home from './components/Home.vue'
import Profile from './components/Profile.vue'
import Register from './components/Register.vue'
import Auth from './components/Auth.vue'

const routes = [
    { 
        path: '/',
        component: Home
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
    history: createMemoryHistory(),
    routes, 
    linkActiveClass: 'active-router',
})

createApp(App).use(router).mount('#app')