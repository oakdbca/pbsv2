<template>
    <DataTableTemplate
        v-if="ajaxDataString"
        ref="burnPlanElements"
        name="burnPlanElements"
        :ajax="ajax"
        :columns="columns"
        :with-filters="true"
        @selection-changed-select="selectionChanged($event)"
        @selection-changed-remove="selectionChanged($event)"
        @mounted="populateFilters"
    >
    </DataTableTemplate>
</template>

<script>
import { apiEndpoints } from '@/utils/hooks';
import DataTableTemplate from '@/components/forms/colocation/DataTableTemplate.vue';

export default {
    name: 'TableBurnPlanElements',
    components: { DataTableTemplate },
    // props: {},
    data: function () {
        return {
            ajaxDataString: '',
            ajaxDataOptions: {},
            fieldFilterOptions: {
                indicative_treatment_year: [],
                revised_indicative_treatment_year: [],
                region: [],
                district: [],
                purpose: [],
                program: [],
                treatment: [],
                status: [],
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
                        d[k] = Object.values(v).join(',');
                    });
                    d.format = 'datatables'; // ?format=datatables
                }.bind(this),
            };
        },
        columns: function () {
            if (!this.fieldFilterOptions) return [];
            return [
                { data: 'id', title: 'ID', visible: false },
                { data: 'name', title: 'Name' },
                {
                    data: 'indicative_treatment_year',
                    title: 'Indicative Treatment Year',
                    filter: true,
                    filterOptions:
                        this.fieldFilterOptions.indicative_treatment_year,
                },
                {
                    data: 'revised_indicative_treatment_year',
                    title: 'Revised Indicative Treatment Year',
                    filter: true,
                    filterOptions:
                        this.fieldFilterOptions
                            .revised_indicative_treatment_year,
                },
                {
                    data: 'regions',
                    title: 'Region',
                    filter: true,
                    filterOptions: this.fieldFilterOptions.region,
                    // eslint-disable-next-line no-unused-vars
                    render: function (data, type, row) {
                        return data
                            ? data
                                  .map((item) => {
                                      return item.name;
                                  })
                                  .join(', ')
                            : 'N/A';
                    },
                },
                {
                    data: 'districts',
                    title: 'District',
                    filter: true,
                    filterOptions: this.fieldFilterOptions.district,
                    // eslint-disable-next-line no-unused-vars
                    render: function (data, type, row) {
                        return data
                            ? data
                                  .map((item) => {
                                      return item.name;
                                  })
                                  .join(', ')
                            : 'N/A';
                    },
                },
                {
                    data: 'purposes',
                    title: 'Purpose',
                    filter: true,
                    visible: false,
                    filterOptions: this.fieldFilterOptions.purpose,
                    multiple: true,
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
                    visible: false,
                    filterOptions: this.fieldFilterOptions.program,
                    multiple: true,
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
                    filterOptions: this.fieldFilterOptions.treatment,
                },
                {
                    data: 'status',
                    title: 'Status',
                    filter: true,
                    filterOptions: this.fieldFilterOptions.status,
                },
                {
                    data: null,
                    title: 'Action',
                    orderable: false,
                    // eslint-disable-next-line no-unused-vars
                    render: function (data, type, row) {
                        return `<a href="burn-plan-elements/${data.id}">View</a></br>
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
        this.$nextTick(() => {
            this.ajaxDataString = apiEndpoints.burnPlanElements();
            // TODO: Get filter params from session storage
            this.setAjax();
        });
    },
    methods: {
        /**
         * Sets or unsets an id and value in the ajaxDataOptions object
         * @param {String=} id An id
         * @param {Object=} value The table value object to set the id to
         * @param {Boolean=} multiple Whether the value is an array or not
         */
        setAjax: function (id, value, multiple = false) {
            const ajaxDataOptions = { ...this.ajaxDataOptions };
            if (!(id in ajaxDataOptions)) {
                ajaxDataOptions[id] = [];
            }
            let values;
            let empty = false;
            if (multiple) {
                empty = value.length == 0 ? true : false;
                values = value.map(({ value }) => value);
            } else {
                empty = value?.value == undefined ? true : false;
                values = empty ? null : [value.value];
            }

            if (empty) {
                delete ajaxDataOptions[id];
            } else {
                ajaxDataOptions[id] = values;
            }

            this.ajaxDataOptions = ajaxDataOptions;
        },
        selectionChanged(event) {
            this.setAjax(...Object.values(event));
        },
        populateFilters() {
            let vm = this;
            const table =
                this.$refs.burnPlanElements.$refs.burnPlanElementsDatatable.dt;
            table.on('xhr', function () {
                for (const [key, value] of Object.entries(
                    table.ajax.json().options
                )) {
                    vm.fieldFilterOptions[key] = value.map(function (row) {
                        return { value: row.key, text: row.value };
                    });
                }
            });
        },
    },
};
</script>
