<template>
    <DataTableTemplate
        v-if="ajax"
        name="Operational Plans"
        :ajax="ajax"
        :columns="columns"
    >
    </DataTableTemplate>
</template>

<script>
import { apiEndpoints, helpers } from '@/utils/hooks';
import DataTableTemplate from '@/components/forms/colocation/DataTableTemplate.vue';

export default {
    name: 'DatatableOperationalPlans',
    components: { DataTableTemplate },
    data: function () {
        return {
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
                        return `<a href="operational-plan/${data.id}/">View</a>`;
                    },
                },
            ];
        },
    },
    mounted: async function () {
        this.$nextTick(() => {
            this.ajax = apiEndpoints.operationalPlans() + `?format=datatables`;
        });
    },
};
</script>
