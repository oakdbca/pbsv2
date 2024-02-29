<!-- A collection of multiple SelectFilter components -->
<template>
    <!-- px-4 is the padding on the left and right -->
    <!-- py-4 is the top and bottom padding -->
    <div v-if="show" class="container px-4 py-4">
        <!-- gx-5 is the gutter between columns -->
        <div class="row gx-5">
            <template v-for="column in columns" :key="column.data">
                <div
                    v-if="column.filterOptions && column.filter"
                    class="col-md-3"
                >
                    <SelectFilter
                        :id="column.data"
                        :title="column.title"
                        :options="column.filterOptions"
                        :show-title="true"
                        :multiple="column.multiple"
                        @selection-changed-select="
                            $emit('selection-changed-select', $event)
                        "
                        @selection-changed-remove="
                            $emit('selection-changed-remove', $event)
                        "
                    >
                    </SelectFilter>
                </div>
            </template>
        </div>
    </div>
</template>

<script>
import SelectFilter from '@/components/forms/colocation/SelectFilter.vue';

export default {
    name: 'SelectFilterTemplate',
    components: { SelectFilter },
    props: {
        columns: {
            type: Array,
            required: true,
        },
        show: {
            type: Boolean,
            required: false,
            default: true,
        },
    },
    emits: ['selection-changed-select', 'selection-changed-remove'],
};
</script>
