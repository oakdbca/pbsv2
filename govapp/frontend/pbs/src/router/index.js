import { RouterView } from 'vue-router';
import { createRouter, createWebHistory } from 'vue-router';
import Test from '@/components/test/test.vue';

var NotFoundComponent = null;
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
            path: '/test',
            name: 'test-page',
            component: Test,
        },
    ],
});

export default router;
