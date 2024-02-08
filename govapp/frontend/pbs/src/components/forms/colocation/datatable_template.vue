<template>
    <div class="row p-1">
        <div
            class="col-4 text-start d-flex align-items-center capitalize"
        ></div>
        <div class="text-start">
            <DataTable
                :columns="table_columns"
                :ajax="ajaxDataString"
                :options="options"
                class="capitalize"
                :class="tableClass"
            />
        </div>
    </div>
</template>

<script>
import _ from 'lodash';

import { helpers } from '@/utils/hooks';

import DataTable from 'datatables.net-vue3';
import DataTablesCore from 'datatables.net-bs5';
import 'datatables.net-responsive-bs5';
import 'datatables.net-buttons-bs5';
import 'datatables.net-buttons/js/buttons.html5';
import 'datatables.net-buttons/js/buttons.print';
import 'datatables.net-select-bs5';

import pdfMake from 'pdfmake';
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import pdfFonts from 'pdfmake/build/vfs_fonts';
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
pdfMake.vfs = pdfFonts.pdfMake.vfs;

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
                dom: '<"container-fluid"<"row"<"col"l><"col"f><"col"<"float-end"B>>>>rtip', // 'Blfprtip'
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
                        ..._.chain(row_merged).toPairs().sortBy(headers).value()
                    )[1];
                    result.push(row);
                    return result;
                },
                []
            );

            return table_data;
        },
    },
};
</script>

<style lang="css">
@import '@/../node_modules/bootstrap/dist/css/bootstrap.min.css';
@import '@/../node_modules/datatables.net-bs5/css/dataTables.bootstrap5.min.css';
@import '@/../node_modules/datatables.net-buttons-bs5/css/buttons.bootstrap5.min.css';

.capitalize {
    text-transform: capitalize;
}
</style>
