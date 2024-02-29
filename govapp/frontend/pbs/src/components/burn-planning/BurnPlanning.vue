<template lang="html">
    <div id="bp" class="container m-0, p-0">
        Burn Planning
        <div class="row"><TableBurnPlanElements></TableBurnPlanElements></div>
    </div>
</template>

<script>
import TableBurnPlanElements from '@/components/burn-planning/TableBurnPlanElements.vue';

export default {
    name: 'BurnPlanning',
    components: { TableBurnPlanElements },
    data: function () {
        return {};
    },
    computed: {},
    mounted: async function () {
        console.log(`${this.$options?.name} template loaded`);
    },
    methods: {},
};
</script>
