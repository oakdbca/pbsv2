import { RouterView } from 'vue-router';
import { createRouter, createWebHistory } from 'vue-router';
import BurnPlanning from '@/components/burnplanning/burnplanning.vue';
import BurnPlanElement from '@/components/burnplanning/burnplanelement.vue';

const NotFoundComponent = null;
const router = createRouter({
    history: createWebHistory(),
    strict: false,
    routes: [
        {
            path: '/',
            name: 'home',
            component: RouterView,
        },
        {
            path: '/:pathMatch(.+)',
            component: NotFoundComponent,
        },
        {
            path: '/burnplanning',
            name: 'burnplanning',
            component: BurnPlanning,
        },
        {
            path: '/burn-plan-elements/:pk',
            name: 'burn-plan-elements',
            component: BurnPlanElement,
        },
    ],
});

export default router;
