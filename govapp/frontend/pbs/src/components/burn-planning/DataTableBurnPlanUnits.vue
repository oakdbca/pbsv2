<template>
    <DataTableTemplate
        v-if="ajaxDataString"
        :ref="refName"
        :name="refName"
        :ajax="ajax"
        :columns="columns"
        :with-filters="true"
        @selection-changed-select="selectionChanged($event)"
        @selection-changed-remove="selectionChanged($event)"
        @mounted="populateFilters(refName)"
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
            ajaxDataString: '',
            ajaxDataOptions: {},
            fieldFilterOptions: {
                active_from: [],
                active_to: [],
                return_interval: [],
                region: [],
                district: [],
                status: [],
            },
        };
    },
    computed: {
        refName: function () {
            return 'burnPlanUnits';
        },
        ajax: function () {
            this.ajaxDataOptions;
            return {
                url: this.ajaxDataString,
                type: 'GET',
                data: function (d) {
                    $.each(this.ajaxDataOptions, (k, v) => {
                        d[k] = Object.values(v).join(',');
                    });
                    d.format = 'datatables';
                }.bind(this),
            };
        },
        columns: function () {
            return [
                { data: 'id', title: 'ID', visible: false },
                { data: 'name', title: 'Name' },
                {
                    data: 'active_from',
                    title: 'Active From',
                    filter: true,
                    filterOptions: this.fieldFilterOptions.active_from,
                },
                {
                    data: 'active_to',
                    title: 'To',
                    filter: true,
                    filterOptions: this.fieldFilterOptions.active_to,
                },
                {
                    data: 'return_interval',
                    title: 'Return Interval',
                    filter: true,
                    filterOptions: this.fieldFilterOptions.return_interval,
                },
                {
                    data: 'regions',
                    title: 'Regions',
                    filter: true,
                    filterOptions: this.fieldFilterOptions.region,
                    render: function (row, type, full) {
                        return helpers.bootstrapBadgesFromList(full.regions);
                    },
                },
                {
                    data: 'district_names',
                    title: 'Districts',
                    name: 'district',
                    filter: true,
                    filterOptions: this.fieldFilterOptions.district,
                    render: function (row, type, full) {
                        return helpers.bootstrapBadgesFromList(
                            full.district_names
                        );
                    },
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
                    render: function (data) {
                        return `<a href="/burn-planning-units/${data.id}">View</a>`;
                    },
                },
            ];
        },
    },
    mounted: async function () {
        this.$nextTick(() => {
            this.ajaxDataString = apiEndpoints.burnPlanningUnits();
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
        populateFilters(refName) {
            let vm = this;
            const table = this.$refs[refName].$refs[`${refName}Datatable`].dt;
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
