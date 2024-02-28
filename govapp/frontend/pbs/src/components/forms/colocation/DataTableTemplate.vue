<template>
    <DataTable
        :ref="datatableRefName"
        :columns="tableColumns"
        :ajax="ajax"
        :options="options"
        class="text-capitalize"
        :class="tableClass"
        @selection-changed-select="$emit('selection-changed-select', $event)"
        @selection-changed-remove="$emit('selection-changed-remove', $event)"
        @vue:mounted="() => $emit('mounted')"
    >
    </DataTable>
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

// Add our custom selection-changed- events to the DataTable component's emits array, to stop vue from complaining about it missing
if (!DataTable.emits.includes('selection-changed-select'))
    DataTable.emits.push('selection-changed-select');
if (!DataTable.emits.includes('selection-changed-remove'))
    DataTable.emits.push('selection-changed-remove');

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
                    // The datatable-vue3 component
                    const component =
                        this.parent()[0].parentElement.__vueParentComponent;
                    // The selectionChanged function to be called when a filter is select or removed
                    const selectionChangedSelect = (e) => {
                        component.ctx.$emit('selection-changed-select', e);
                    };
                    const selectionChangedRemove = (e) => {
                        component.ctx.$emit('selection-changed-remove', e);
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
                                    options: columnOptions.filterOptions,
                                    showTitle: false, // we use the title in the header
                                    multiple: columnOptions.multiple
                                        ? true
                                        : false,
                                    onSelectionChangedSelect:
                                        selectionChangedSelect,
                                    onSelectionChangedRemove:
                                        selectionChangedRemove,
                                };
                                const select = createApp(SelectFilter, props);

                                let div_parent = document.createElement('div');

                                let div_original_header =
                                    document.createElement('div');
                                div_original_header.append(
                                    ...this.header().children
                                );

                                const id = `mountpoint-select-filter-${columnOptions.data}`;

                                div_parent.appendChild(div_original_header);

                                let div_select = document.createElement('div');
                                div_select.id = id;

                                div_parent.appendChild(div_select);

                                this.header().replaceChildren(div_parent);

                                select.mount(`#${id}`);

                                $(div_select).on('click', function (e) {
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
    emits: ['selection-changed-select', 'selection-changed-remove', 'mounted'],
    computed: {
        datatableRefName: function () {
            return this.name + 'Datatable';
        },
        /**
         * Columns object for the DataTable component
         */
        tableColumns: function () {
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
                this.$refs[this.datatableRefName].dt.ajax.reload();
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

<style scoped lang="css">
@import 'datatables.net-dt';
</style>
