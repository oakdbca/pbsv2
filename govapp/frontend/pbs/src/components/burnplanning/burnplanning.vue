<template lang="html">
    <div id="bp" class="container m-0, p-0">
        Burn Planning
        <div class="row">
            <BurnPlanElement :burn-plan-element-id="1"></BurnPlanElement>
        </div>
    </div>
</template>

<script>
import BurnPlanElement from '@/components/burnplanning/burnplanelement.vue';

export default {
    name: 'BurnPlanning',
    components: { BurnPlanElement },
    data: function () {
        return {};
    },
    computed: {},
    mounted: async function () {
        console.log('BurnPlanning template loaded');
    },
    methods: {},
};
</script>
