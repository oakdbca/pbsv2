<template>
    <div id="bpe" class="container">Burn Plan Elements</div>
    <div class="card text-center">
        <TableSlotTemplate
            name="Burn Plan Elements"
            :ajax-data-string="ajax"
            :columns="columns"
            :key="`bpe-${ajax}`"
        >
        </TableSlotTemplate>
    </div>
</template>

<script>
import { api_endpoints } from '@/utils/hooks';
import TableSlotTemplate from '@/components/forms/colocation/table_slot_template.vue';

export default {
    name: 'TableBurnPlanElements',
    components: { TableSlotTemplate },
    props: {},
    data: function () {
        return {
            burnPlanElements: [],
            ajax: '',
        };
    },
    computed: {
        queryset: function () {
            return this.burnPlanElements;
        },
        columns: function () {
            return [
                { data: 'id', title: 'ID', visible: false },
                { data: 'name', title: 'Name' },
                {
                    data: 'indicative_treatment_year',
                    title: 'Indicative Treatment Year',
                },
                {
                    data: 'revised_indicative_treatment_year',
                    title: 'Revise d Indicative Treatment Year',
                },
                { data: 'region', title: 'Region' },
                { data: 'district', title: 'District' },
                { data: 'treatment', title: 'Treatment' },
                { data: 'status', title: 'Status' },
                {
                    data: null,
                    title: 'Action',
                    orderable: false,
                    render: function (data, type, row) {
                        return `<a href="burn-plan-elements/${data.id}" target="_blank">View</a>`;
                    },
                },
            ];
        },
        headers: function () {
            return [
                'id',
                'name',
                'indicative_treatment_year',
                'revised_indicative_treatment_year',
                'region',
                'district',
                'treatment',
                'status',
            ];
        },
    },
    mounted: async function () {
        console.info(`${this.$options?.name} template loaded`);
        this.$nextTick(() => {
            this.ajax = api_endpoints.burn_plan_elements();
        });
    },
    methods: {},
};
</script>
