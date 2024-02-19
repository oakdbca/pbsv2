<template>
    <div class="form-group">
        <label for="select-filter">{{ title }}</label>
        <select
            :id="`select-filter-${id}`"
            v-model="selectedFilterItem"
            class="form-control"
            @change="
                $emit('selection-changed', {
                    id: id,
                    value: selectedFilterItem,
                    valueAll: valueAll,
                })
            "
        >
            <option
                v-for="option in filterOptions"
                :key="option.value"
                :value="option.value"
            >
                {{ option.text }}
            </option>
        </select>
    </div>
</template>

<script>
export default {
    name: 'SelectFilter',
    props: {
        id: {
            type: String,
            required: true,
        },
        title: {
            type: String,
            required: true,
        },
        filterOptions: {
            type: Object,
            required: true,
        },
        valueAll: {
            type: String,
            required: false,
            default: 'all',
        },
    },
    emits: ['selection-changed'],
    data: function () {
        return {
            selectedFilterItem: null,
        };
    },
    mounted: function () {
        // TODO: Get from session storage
        this.selectedFilterItem = this.valueAll;
    },
};
</script>
