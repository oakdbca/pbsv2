<template>
    <div id="bpe" class="container">Burn Plan Elements</div>
    <div class="card text-center">
        <DataTableTemplate
            v-if="ajaxDataString"
            name="Burn Plan Elements"
            :ajax="ajax"
            :columns="columns"
            @selection-changed="selectionChanged($event)"
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
import { utils, api_endpoints } from '@/utils/hooks';
import DataTableTemplate from '@/components/forms/colocation/datatable_template.vue';
import SelectFilter from '@/components/forms/colocation/select_filter.vue';

export default {
    name: 'TableBurnPlanElements',
    components: { DataTableTemplate, SelectFilter },
    // props: {},
    data: function () {
        return {
            ajaxDataString: '',
            ajaxDataOptions: {},
            fieldFilterOptions: {
                treatments: [{ value: 'all', text: 'All' }],
                regions: [{ value: 'all', text: 'All' }],
                districts: [{ value: 'all', text: 'All' }],
                purposes: [{ value: 'all', text: 'All' }],
                programs: [{ value: 'all', text: 'All' }],
            },
        };
    },
    computed: {
        ajax: function () {
            this.ajaxDataOptions;
            return {
                url: this.ajaxDataString,
                type: 'GET',
                data: function (d) {
                    $.each(this.ajaxDataOptions, (k, v) => {
                        d[k] = v;
                    });
                    d.format = 'datatables'; // ?format=datatables
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
                {
                    data: 'region',
                    title: 'Region',
                    filter: true,
                    filterOptions: this.fieldFilterOptions.regions,
                },
                {
                    data: 'district',
                    title: 'District',
                    filter: true,
                    filterOptions: this.fieldFilterOptions.districts,
                },
                {
                    data: 'purposes',
                    title: 'Purpose',
                    filter: true,
                    filterOptions: this.fieldFilterOptions.purposes,
                    // eslint-disable-next-line no-unused-vars
                    render: function (data, type, row) {
                        // TODO: Multi-select display and render
                        return data ? data[0].name : 'N/A';
                    },
                },
                {
                    data: 'programs',
                    title: 'Program',
                    filter: true,
                    filterOptions: this.fieldFilterOptions.programs,
                    // eslint-disable-next-line no-unused-vars
                    render: function (data, type, row) {
                        // TODO: Multi-select display and render
                        return data ? data[0].name : 'N/A';
                    },
                },
                {
                    data: 'treatment',
                    title: 'Treatment',
                    filter: true,
                    filterOptions: this.fieldFilterOptions.treatments,
                },
                { data: 'status', title: 'Status' },
                {
                    data: null,
                    title: 'Action',
                    orderable: false,
                    // eslint-disable-next-line no-unused-vars
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
        // TODO: outsource to a helper function
        const requests = Object.keys(this.fieldFilterOptions).map((field) =>
            utils
                .fetchUrl(`api/${field}/key-value-list/`)
                .then((response) => response)
        );

        await Promise.all(requests)
            .then((responses) => {
                responses.forEach((response, index) => {
                    this.fieldFilterOptions[
                        Object.keys(this.fieldFilterOptions)[index]
                    ].push(
                        ...response.map((item) => {
                            return { value: item.key, text: item.value };
                        })
                    );
                });
            })
            .catch((error) => {
                console.error('error', error);
            });

        this.$nextTick(() => {
            this.ajaxDataString = api_endpoints.burn_plan_elements();
            // TODO: Get filter params from session storage
            this.setAjax();
        });
    },
    methods: {
        /**
         * Sets or unsets a tag and value in the ajaxDataOptions object
         * @param {String=} tag A tag
         * @param {String=} value The value to set the tag to
         * @param {String=} valueAll The value to to use when unsetting the tag / filter all values
         */
        setAjax: function (tag, value, valueAll = 'all') {
            const ajaxDataOptions = { ...this.ajaxDataOptions };
            if (tag && value) {
                if (value == valueAll) {
                    delete ajaxDataOptions[tag];
                } else {
                    ajaxDataOptions[tag] = value;
                }
                this.ajaxDataOptions = ajaxDataOptions;
            }
        },
        selectionChanged(event) {
            this.setAjax(event.id, event.value, event.valueAll);
        },
    },
};
</script>
