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
            validator: (
                /** @type {{ key: String, value: String; }[] | { value: String, text: String; }[] } */ values
            ) => {
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
            type: [Number, String, Object, Array],
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
        // Purpose needs to use this function to map the key-value pairs to value-text pairs
        this.selectedFilterItem = this.getSelectedFilterItemByKey(
            this.preSelectedFilterItem
        );
    },
    methods: {
        /**
         * Maps key-value pairs to value-text pairs to be used by the MultiSelect component
         * @param {{ key: String, value: String; }[] | { value: String, text: String; }[] } options The key-value pair(s) to be mapped
         */
        mapKeyValuePairs: function (options) {
            return options.map((option) => {
                return {
                    value: Object.hasOwn(option, 'key')
                        ? option.key.toString() // Casting to string to avoid potential type mismatch
                        : option.value.toString(),
                    text: Object.hasOwn(option, 'key')
                        ? option.value.toString()
                        : option.text.toString(),
                };
            });
        },
        /**
         * Returns value-text pair(s) from the model's filter_options property by filter id and item key(s)
         * to be used by the MultiSelect component as selected value(s).
         * The key being the respective model field entry and the value being its human readable representation.
         * For example: `[ { "value": ..., "text": ... }, ... ]`
         * @param {Number|String|(Number|String|{value:String|Number;})[]} selected The selected filter item key(s),
         * or an object in the form of { value: string | number; text: string; }, or an array of such objects
         * @returns {Object[]} An array of filter item objects
         */
        getSelectedFilterItemByKey: function (selected) {
            const filterOptions = this.optionsFormatted;
            if (selected === null) return [];

            return filterOptions.filter(
                (/** @type {{ value: string | number; }} */ item) => {
                    if (['number', 'string'].includes(typeof selected)) {
                        // Single value number or string
                        return item.value === selected.toString();
                    }

                    if (Array.isArray(selected)) {
                        // Array
                        if (
                            selected.length > 0 &&
                            typeof selected[0] === 'object'
                        ) {
                            // Array of objects
                            return selected.some(
                                (s) =>
                                    /** @type {{value: Number | String}} */ (
                                        s
                                    ).value.toString() === item.value
                            );
                        } else {
                            // Array of numbers or strings
                            return selected
                                .map((s) => s.toString())
                                .includes(
                                    /** @type {{value: String}} */ (item).value
                                );
                        }
                    }

                    // Object in the form of { value: string | number; text: string; }
                    if (typeof selected === 'object') {
                        return (
                            item.value ===
                            /** @type {Object} */ (selected).value?.toString()
                        );
                    }
                    return []; // Else
                }
            );
        },
    },
};
</script>

<style scoped>
@import 'vue-multiselect/dist/vue-multiselect.css';
</style>
