<template>
    <div id="bpe" class="container">Burn Plan Elements</div>
    <div class="card text-center">
        <DataTableTemplate
            v-if="ajaxDataString"
            name="Burn Plan Elements"
            :ajax="ajax"
            :columns="columns"
        >
            <template #filter>
                <SelectFilter
                    id="treatment"
                    ref="selectFilter"
                    title="Treatment"
                    :filter-options="columns[6].filterOptions"
                    @selection-changed="selectionChanged($event)"
                />
            </template>
        </DataTableTemplate>
    </div>
</template>

<script>
import { api_endpoints } from '@/utils/hooks';
import DataTableTemplate from '@/components/forms/colocation/datatable_template.vue';
import SelectFilter from '@/components/forms/colocation/select_filter.vue';

export default {
    name: 'TableBurnPlanElements',
    components: { DataTableTemplate, SelectFilter },
    // props: {},
    data: function () {
        return {
            burnPlanElements: [],
            ajaxDataString: '',
            ajaxDataOptions: {},
        };
    },
    computed: {
        queryset: function () {
            return this.burnPlanElements;
        },
        ajax: function () {
            this.ajaxDataOptions;
            return {
                url: this.ajaxDataString,
                type: 'GET',
                data: function (d) {
                    $.each(this.ajaxDataOptions, (k, v) => {
                        d[k] = v;
                    });
                }.bind(this),
            };
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
                    title: 'Revised Indicative Treatment Year',
                },
                { data: 'region', title: 'Region' },
                { data: 'district', title: 'District' },
                {
                    data: 'treatment',
                    title: 'Treatment',
                    filter: true,
                    // TODO: Get filter options from api
                    filterOptions: [
                        { value: '1', text: 'Treat With Care' },
                        { value: '2', text: 'Burn After Reading' },
                    ],
                },
                { data: 'status', title: 'Status' },
                {
                    data: null,
                    title: 'Action',
                    orderable: false,
                    // eslint-disable-next-line @typescript-eslint/no-unused-vars
                    render: function (data, type, row) {
                        return `<a href="burn-plan-elements/${data.id}" target="_blank">View</a></br>
                                <a href="#" onclick="alert('Not yet implemented')">History</a>`;
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
            this.ajaxDataString = api_endpoints.burn_plan_elements();
            // TODO: Get filter params from session storage
            this.setAjax();
        });
    },
    methods: {
        /**
         * Sets or unsets a tag and value in the ajaxDataOptions object
         * @param {*} tag A tag
         * @param {*} value The value to set the tag to
         */
        setAjax: function (tag, value) {
            const ajaxDataOptions = { ...this.ajaxDataOptions };
            if (tag && value) {
                if (value == 'all') {
                    delete ajaxDataOptions[tag];
                } else {
                    ajaxDataOptions[tag] = value;
                }
                this.ajaxDataOptions = ajaxDataOptions;
            }
        },
        selectionChanged(event) {
            this.setAjax(event.id, event.value);
        },
    },
};
</script>
