//import Vue from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
//import external_routes from '@/components/external/routes'
//import internal_routes from '@/components/internal/routes'

//Vue.use(Router)
var NotFoundComponent = null

//console.log(process.env.BASE_URL)
const router = createRouter({
    //history: createWebHistory(process.env.BASE_URL),
    history: createWebHistory(),
    //strict: true,
    routes: [
        {
            path: '/:pathMatch(.*)',
            component: NotFoundComponent
        },

//        internal_routes,
    ]
})

export default router;
