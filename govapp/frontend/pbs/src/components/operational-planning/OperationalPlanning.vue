<template lang="html">
    <div class="container px-4">
        <div class="row">
            <div class="col-12">
                <h3 class="text-secondary">Operational Planning</h3>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <div class="card">
                    <div class="card-body p-3">
                        <DatatableOperationalPlans></DatatableOperationalPlans>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import DatatableOperationalPlans from '@/components/operational-planning/DatatableOperationalPlans.vue';

export default {
    name: 'BurnPlanning',
    components: { DatatableOperationalPlans },
};
</script>
