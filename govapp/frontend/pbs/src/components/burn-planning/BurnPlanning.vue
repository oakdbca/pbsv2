<template lang="html">
    <div id="bp" class="container px-4">
        <div class="row">
            <div class="col-12">
                <h3 class="text-secondary">Burn Plan Elements</h3>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <div class="card">
                    <div class="card-body p-3">
                        <TableBurnPlanElements></TableBurnPlanElements>
                    </div>
                </div>
            </div>
        </div>
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
