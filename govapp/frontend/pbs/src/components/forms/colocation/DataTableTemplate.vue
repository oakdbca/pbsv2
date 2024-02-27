<template>
    <DataTable
        ref="datatable"
        :columns="table_columns"
        :ajax="ajax"
        :options="options"
        class="text-capitalize"
        :class="tableClass"
        @selection-changed="$emit('selection-changed', $event)"
    />
</template>

<script>
import _ from 'lodash';
import { helpers } from '@/utils/hooks';
import SelectFilter from '@/components/forms/colocation/SelectFilter.vue';

import { createApp } from 'vue';

import DataTable from 'datatables.net-vue3';
import DataTablesCore from 'datatables.net-bs5';
import Select from 'datatables.net-select-bs5';
import Responsive from 'datatables.net-responsive'; // -bs5 not working
import Buttons from 'datatables.net-buttons'; // -bs5 not working
import ButtonsHtml5 from 'datatables.net-buttons/js/buttons.html5';
import 'datatables.net-buttons-bs5/js/buttons.bootstrap5.js';

DataTable.use(DataTablesCore);
DataTable.use(Select);
DataTable.use(Responsive);
DataTable.use(Buttons);
DataTable.use(ButtonsHtml5);

// Add our custom selection-changed event to the DataTable component's emits array, to stop vue from complaining about it missing
if (!DataTable.emits.includes('selection-changed'))
    DataTable.emits.push('selection-changed');

export default {
    name: 'DataTableTemplate',
    components: { DataTable },
    props: {
        /**
         * Name of the table
         */
        name: {
            type: String,
            required: true,
        },
        /**
         * The ajax endpoint string or object to fetch data from
         */
        ajax: {
            type: [String, Object],
            required: true,
        },
        /**
         * A list of dictionaries in the form of [{data: 'column', title: 'Column Title'}, ...]
         * Use either this or headers. Columns take precedence over headers
         */
        columns: {
            type: Array,
            required: false,
            default: () => [],
        },
        /**
         * Options for the DataTable component
         */
        options: {
            type: Object,
            required: false,
            default: () => ({
                responsive: true,
                select: false,
                dom: '<"container-fluid"<"row"<"col"l><"col"f><"col"<"float-end"B>>>>rtip', // 'lfBrtip'
                buttons: ['copy', 'csv', 'excel'],
                // eslint-disable-next-line no-unused-vars
                initComplete: function (settings, json) {
                    console.log('Table initialized!');
                    // The datatable-vue3 component
                    const component =
                        this.parent()[0].parentElement.__vueParentComponent;
                    // The selectionChanged function to be called when a filter is changed
                    const selectionChanged = (e) => {
                        component.ctx.$emit('selection-changed', e);
                    };
                    this.api()
                        .columns()
                        .every(function () {
                            const columnOptions =
                                this.context[0].aoColumns[this.index()];
                            const filter = columnOptions.filter;

                            if (filter == true) {
                                const props = {
                                    id: columnOptions.data,
                                    title: columnOptions.title,
                                    filterOptions: columnOptions.filterOptions,
                                    showTitle: false, // we use the title in the header
                                    onSelectionChanged: selectionChanged,
                                };
                                const select = createApp(SelectFilter, props);

                                let div = document.createElement('div');

                                div = document.createElement('div');
                                const id = `mountpoint-select-filter-${columnOptions.data}`;
                                div.id = id;
                                this.header().appendChild(div);
                                select.mount(`#${id}`);
                                // div.appendChild(select);

                                $(div).on('click', function (e) {
                                    e.stopPropagation();
                                });
                            }
                        });
                },
            }),
        },
        /**
         * A string of classes to apply to the table
         */
        tableClass: {
            type: String,
            required: false,
            default: 'table table-hover table-striped',
        },
        /**
         * A list of headers that correspond to column names in the queryset
         * Use either this or columns. Columns take precedence over headers
         */
        headers: {
            type: Array,
            required: false,
            default: () => [],
        },
    },
    emits: ['selection-changed'],
    computed: {
        /**
         * Columns object for the DataTable component
         */
        table_columns: function () {
            // If columns are provided, use them
            if (this.columns.length) {
                return this.columns;
            }
            // Otherwise, derive from headers headers
            const columns = [];
            _.forEach(this.headers, (value) => {
                columns.push({
                    data: value,
                    title: this.replaceUnderscores(value),
                });
            });
            if (columns.length) {
                return columns;
            }
            // If no headers are provided, use id as the default
            return [{ data: 'id', title: 'Id' }];
        },
    },
    watch: {
        ajax: {
            // eslint-disable-next-line no-unused-vars
            handler: function (val) {
                // Reload the table when the ajax prop changes
                this.$refs.datatable.dt.ajax.reload();
            },
            deep: true,
        },
    },
    methods: {
        replaceUnderscores: helpers.replaceUnderscores,
        /**
         * Converts a queryset and headers to a format that DataTables can understand
         * @param {Array} queryset
         * @param {Array} headers A list of column headers
         * @returns {Array} A list of rows, each row is an array of values
         */
        tableData: function (queryset, headers) {
            const table_data = _.reduce(
                queryset,
                (result, value /**, key*/) => {
                    // Initialize the table row with null values
                    const row_full = {};
                    _.forEach(headers, (v /**, k*/) => {
                        row_full[v] = null;
                    });
                    // Pick queryset row values by headers
                    const row_serialized = _.pickBy(value, (v, k) => {
                        return headers.includes(k);
                    });
                    // Merge the two rows, overwriting null values where applicable
                    const row_merged = { ...row_full, ...row_serialized };
                    // Sort by headers order, create an array, and push to result
                    const row = _.zip(
                        ..._.chain(row_merged)
                            .toPairs()
                            .sortBy(headers)
                            .value(),
                    )[1];
                    result.push(row);
                    return result;
                },
                [],
            );

            return table_data;
        },
    },
};
</script>

<style lang="css">
@import 'datatables.net-dt';
</style>
