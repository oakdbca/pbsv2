<!-- Slot in table header and body rows -->
<template>
    <div class="row p-1">
        <div class="col-4 text-start d-flex align-items-center capitalize">
            {{ name }}
        </div>
        <div class="text-start">
            <table class="table text-small">
                <thead>
                    <tr>
                        <th
                            v-for="column in columns"
                            :key="`table-${name}-${column}`"
                            scope="col"
                            class="capitalize"
                        >
                            {{ replaceUnderscores(column) }}
                        </th>
                        <!-- Additional table headers to be slotted here -->
                        <slot name="table_headers"></slot>
                    </tr>
                </thead>
                <tbody v-if="queryset_length">
                    <tr v-for="record in queryset" :key="`record-${record.id}`">
                        <td v-for="column in columns" :key="`column-${column}`">
                            <span v-if="Object.hasOwn(record, column)">
                                {{ record[column] }}
                            </span>
                        </td>
                        <!-- Additional table rows to be slotted here -->
                        <slot name="table_rows"></slot>
                    </tr>
                </tbody>
                <tbody v-else>
                    <tr>
                        <td>
                            <slot name="table_rows"></slot>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import { helpers } from '@/utils/hooks';

export default {
    name: 'TableSlotTemplate',
    props: {
        /**
         * Name of the table
         */
        name: {
            type: String,
            required: true,
        },
        /**
         * Model queryset to be displayed in the table
         */
        queryset: {
            type: Object,
            required: false,
            default: () => Object(),
        },
        /**
         * List of properties of the model queryset to be displayed in the table
         */
        properties: {
            type: Array,
            required: false,
            default: () => [],
        },
    },
    computed: {
        /**
         * Returns the list of columns to be displayed in the table
         * If no `properties` prop is provided, columns are derived from all properties of the queryset
         */
        columns: function () {
            if (this.properties.length > 0) {
                return this.properties;
            } else if (this.queryset_length > 0) {
                return Object.keys(this.queryset[0]);
            } else {
                return [];
            }
        },
        queryset_length: function () {
            return Object.keys(this.queryset).length;
        },
    },
    methods: {
        replaceUnderscores: helpers.replaceUnderscores,
    },
};
</script>

<style lang="css">
.capitalize {
    text-transform: capitalize;
}
</style>
