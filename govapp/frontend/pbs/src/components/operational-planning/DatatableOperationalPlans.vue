<template>
    <DataTableTemplate
        v-if="ajax"
        name="Operational Plans"
        :ajax-data-string="ajax"
        :columns="columns"
    >
    </DataTableTemplate>
</template>

<script>
import { api_endpoints, helpers } from '@/utils/hooks';
import DataTableTemplate from '@/components/forms/colocation/datatable_template.vue';

export default {
    name: 'DatatableOperationalPlans',
    components: { DataTableTemplate },
    data: function () {
        return {
            burnPlanElements: [],
            ajax: '',
        };
    },
    computed: {
        columns: function () {
            return [
                { data: 'id', title: 'ID', visible: false },
                { data: 'name', title: 'Name' },
                {
                    data: 'burn_plan_unit',
                    name: 'operational_area__burn_plan_element__burn_plan_unit__reference_number',
                    title: 'Burn Plan Unit',
                },
                { data: 'year', title: 'Year' },
                {
                    data: 'regions',
                    title: 'Regions',
                    render: function (row, type, full) {
                        return helpers.bootstrapBadgesFromList(full.regions);
                    },
                },
                {
                    data: 'districts',
                    title: 'Districts',
                    render: function (row, type, full) {
                        return helpers.bootstrapBadgesFromList(full.districts);
                    },
                },
                { data: 'status', title: 'Status' },
                { data: 'assigned_to_name', title: 'Assigned To' },
                {
                    data: null,
                    title: 'Action',
                    orderable: false,
                    render: function (data) {
                        return `<a href="operational-plan/${data.id}/" target="_blank">View</a>`;
                    },
                },
            ];
        },
    },
    mounted: async function () {
        console.info(`${this.$options?.name} template loaded`);
        this.$nextTick(() => {
            this.ajax = api_endpoints.operationalPlans();
        });
    },
};
</script>
