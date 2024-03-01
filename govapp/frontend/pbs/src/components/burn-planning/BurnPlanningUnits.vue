<template lang="html">
    <div id="bp" class="container px-4">
        <div class="row">
            <div class="col-12">
                <h3 class="text-secondary">Burn Planing Units</h3>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <div class="card">
                    <div class="card-body p-3">
                        <DataTableBurnPlanUnits></DataTableBurnPlanUnits>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import DataTableBurnPlanUnits from '@/components/burn-planning/DataTableBurnPlanUnits.vue';

export default {
    name: 'BurnPlanning',
    components: { DataTableBurnPlanUnits },
};
</script>
