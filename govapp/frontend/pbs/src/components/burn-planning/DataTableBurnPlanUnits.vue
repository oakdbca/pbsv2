<template>
    <DataTableTemplate
        v-if="ajax"
        name="Burn Plan Units"
        :ajax="ajax"
        :columns="columns"
    >
    </DataTableTemplate>
</template>

<script>
import { apiEndpoints, helpers } from '@/utils/hooks';
import DataTableTemplate from '@/components/forms/colocation/DataTableTemplate.vue';

export default {
    name: 'DatatableBurnPlanUnits',
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
                { data: 'active_from', title: 'Active From' },
                { data: 'active_to', title: 'To' },
                { data: 'return_interval', title: 'Return Interval' },
                {
                    data: 'regions',
                    title: 'Regions',
                    render: function (row, type, full) {
                        return helpers.bootstrapBadgesFromList(full.regions);
                    },
                },
                {
                    data: 'district_names',
                    title: 'Districts',
                    render: function (row, type, full) {
                        return helpers.bootstrapBadgesFromList(
                            full.district_names
                        );
                    },
                },
                { data: 'status', title: 'Status' },
                {
                    data: null,
                    title: 'Action',
                    orderable: false,
                    render: function (data) {
                        return `<a href="/burn-planning-units/${data.id}">View</a>`;
                    },
                },
            ];
        },
    },
    mounted: async function () {
        this.$nextTick(() => {
            this.ajax = apiEndpoints.burnPlanningUnits() + `?format=datatables`;
        });
    },
};
</script>
