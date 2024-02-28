<!-- A single dropdown with selectable items as a component -->
<template>
    <div class="form-group">
        <label v-if="showTitle" for="select-filter">{{ title }}</label>
        <Multiselect
            :id="`select-filter-${id}`"
            v-model="selectedFilterItem"
            :multiple="multiple"
            :options="options"
            :name="name"
            :label="label"
            :track-by="name"
            :placeholder="placeholder"
            class="form-control"
            @select="
                $emit('selection-changed-select', {
                    id: id,
                    value: selectedFilterItem,
                    multiple: multiple,
                })
            "
            @remove="
                $emit('selection-changed-remove', {
                    id: id,
                    value: selectedFilterItem,
                    multiple: multiple,
                })
            "
        >
        </Multiselect>
    </div>
</template>

<script>
import { Multiselect } from 'vue-multiselect';
export default {
    name: 'SelectFilter',
    components: { Multiselect },
    props: {
        id: {
            type: String,
            required: true,
        },
        title: {
            type: String,
            required: true,
        },
        options: {
            type: Object,
            required: true,
        },
        preSelectedFilterItem: {
            type: Array,
            required: false,
            default: () => [],
        },
        showTitle: {
            type: Boolean,
            required: false,
            default: true,
        },
        name: {
            type: String,
            required: false,
            default: 'value',
        },
        label: {
            type: String,
            required: false,
            default: 'text',
        },
        multiple: {
            type: Boolean,
            required: false,
            default: false,
        },
        placeholder: {
            type: String,
            required: false,
            default: 'Select a value',
        },
    },
    emits: ['selection-changed-select', 'selection-changed-remove'],
    data: function () {
        return {
            selectedFilterItem: [],
        };
    },
    mounted: function () {
        console.log(`${this.$options?.name} template loaded`);
        // TODO: Get from session storage
        this.selectedFilterItem = this.preSelectedFilterItem;
    },
};
</script>

<style scoped>
@import 'vue-multiselect/dist/vue-multiselect.css';
</style>
