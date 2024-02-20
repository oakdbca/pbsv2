import { RouterView } from 'vue-router';
import { createRouter, createWebHistory } from 'vue-router';
import ProfileComponent from '@/components/accounts/Profile.vue';
import BurnPlanning from '@/components/burnplanning/burnplanning.vue';
import BurnPlanElement from '@/components/burnplanning/burnplanelement.vue';
import OperationalPlanning from '@/components/operational-planning/OperationalPlanning.vue';

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
            path: '/profile/',
            name: 'profile',
            component: ProfileComponent,
        },
        {
            path: '/burnplanning',
            name: 'burnplanning',
            component: BurnPlanning,
        },
        {
            path: '/operational-planning',
            name: 'operational-planning',
            component: OperationalPlanning,
        },
        {
            path: '/burn-plan-elements/:pk',
            name: 'burn-plan-elements',
            component: BurnPlanElement,
        },
    ],
});

export default router;
