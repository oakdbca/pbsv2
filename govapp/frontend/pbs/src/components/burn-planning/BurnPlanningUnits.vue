<template lang="html">
    <div id="bp" class="container px-4">
        <div class="row">
            <div class="col-12">
                <h3 class="text-secondary">
                    Burn Planning Units
                    <button
                        class="btn btn-primary float-end"
                        data-bs-toggle="modal"
                        data-bs-target="#exportBurnPlanningUnits"
                    >
                        Export <i class="bi bi-box-arrow-up"></i>
                    </button>
                    <button
                        class="btn btn-primary float-end me-2"
                        data-bs-toggle="modal"
                        data-bs-target="#importBurnPlanningUnits"
                    >
                        Import <i class="bi bi-box-arrow-down"></i>
                    </button>
                </h3>
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
    <ModalImportBurnPlanningUnits></ModalImportBurnPlanningUnits>
    <ModalExportBurnPlanningUnits></ModalExportBurnPlanningUnits>
</template>

<script>
import DataTableBurnPlanUnits from '@/components/burn-planning/DataTableBurnPlanUnits.vue';

import ModalImportBurnPlanningUnits from '@/components/burn-planning/ModalImportBurnPlanningUnits.vue';
import ModalExportBurnPlanningUnits from '@/components/burn-planning/ModalExportBurnPlanningUnits.vue';

export default {
    name: 'BurnPlanning',
    components: {
        DataTableBurnPlanUnits,
        ModalImportBurnPlanningUnits,
        ModalExportBurnPlanningUnits,
    },
};
</script>
