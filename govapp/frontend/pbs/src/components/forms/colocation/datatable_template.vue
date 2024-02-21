<template>
    <DataTable
        :columns="table_columns"
        :ajax="ajaxDataString + '?format=datatables'"
        :options="options"
        class="text-capitalize"
        :class="tableClass"
    />
</template>

<script>
import _ from 'lodash';

import { helpers } from '@/utils/hooks';

import DataTable from 'datatables.net-vue3';
import DataTablesCore from 'datatables.net';
import 'datatables.net-responsive';
import 'datatables.net-buttons';

DataTable.use(DataTablesCore);

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
         * The ajax endpoint string to fetch data from
         */
        ajaxDataString: {
            type: String,
            required: false,
            default: '',
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
                buttons: ['copy', 'csv', 'excel', 'pdf', 'print'],
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
