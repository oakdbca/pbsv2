<template>
    <div id="bpe" class="container">Burn Plan Elements</div>
    <div class="card text-center">
        <DataTableTemplate
            v-if="ajaxDataString"
            name="Burn Plan Elements"
            :ajax="ajax"
            :columns="columns"
            @selection-changed-select="selectionChanged($event)"
            @selection-changed-remove="selectionChanged($event)"
        >
        </DataTableTemplate>
    </div>
</template>

<script>
import { utils, api_endpoints } from '@/utils/hooks';
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
                treatments: [],
                regions: [],
                districts: [],
                purposes: [],
                programs: [],
                status: [],
                'indicative-treatment-years': [],
                'revised-indicative-treatment-years': [],
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
            return [
                { data: 'id', title: 'ID', visible: false },
                { data: 'name', title: 'Name' },
                {
                    data: 'indicative_treatment_year',
                    title: 'Indicative Treatment Year',
                    filter: true,
                    filterOptions:
                        this.fieldFilterOptions['indicative-treatment-years'],
                },
                {
                    data: 'revised_indicative_treatment_year',
                    title: 'Revised Indicative Treatment Year',
                    filter: true,
                    filterOptions:
                        this.fieldFilterOptions[
                            'revised-indicative-treatment-years'
                        ],
                },
                {
                    data: 'regions',
                    title: 'Region',
                    filter: true,
                    filterOptions: this.fieldFilterOptions.regions,
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
                    filterOptions: this.fieldFilterOptions.districts,
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
                    filterOptions: this.fieldFilterOptions.purposes,
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
                    filterOptions: this.fieldFilterOptions.programs,
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
                    filterOptions: this.fieldFilterOptions.treatments,
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
            // this.setAjax(event.id, event.value, event.multiple);
            this.setAjax(...Object.values(event));
        },
    },
};
</script>
