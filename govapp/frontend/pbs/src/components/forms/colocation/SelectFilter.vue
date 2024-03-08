<!-- A single dropdown with selectable items as a component -->
<template>
    <div class="form-group text-start">
        <label
            v-if="showTitle"
            :for="`select-filter-${id}`"
            class="text-secondary mb-1"
            >{{ title }}</label
        >
        <Multiselect
            :id="`select-filter-${id}`"
            v-model="selectedFilterItem"
            :multiple="multiple"
            :options="optionsFormatted"
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
            validator: (/** @type Object */ values) => {
                if (typeof values !== 'object') return false;

                return values.every((value) => {
                    const keys = Object.keys(value);
                    if (keys.length != 2) return false;
                    return (
                        (keys.includes('key') && keys.includes('value')) ||
                        (keys.includes('value') && keys.includes('text'))
                    );
                });
            },
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
    computed: {
        optionsFormatted: function () {
            // Allows to pass in key-value pairs or value-text pairs
            return this.mapKeyValuePairs(this.options);
        },
    },
    mounted: function () {
        // TODO: Get from session storage
        this.selectedFilterItem = this.mapKeyValuePairs(
            this.preSelectedFilterItem
        );
    },
    methods: {
        /**
         * Maps key-value pairs to value-text pairs to be used by the MultiSelect component
         */
        mapKeyValuePairs: function (options) {
            return options.map((option) => {
                return {
                    value: Object.hasOwn(option, 'key')
                        ? option.key
                        : option.value,
                    text: Object.hasOwn(option, 'key')
                        ? option.value
                        : option.text,
                };
            });
        },
    },
};
</script>

<style scoped>
@import 'vue-multiselect/dist/vue-multiselect.css';
</style>
