<template>
    <div class="row mb-2 p-2">
        <div class="col-md-3">
            <div class="form-group">
                <label for="select-filter">{{ title }}</label>
                <select
                    id="select-filter"
                    v-model="selectedFilterItem"
                    class="form-control"
                    @change="
                        $emit('selection-changed', {
                            id: id,
                            value: selectedFilterItem,
                        })
                    "
                >
                    <option :value="valueAll">All</option>
                    <option
                        v-for="option in filterOptions"
                        :key="option.value"
                        :value="option.value"
                    >
                        {{ option.text }}
                    </option>
                </select>
            </div>
        </div>
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
    },
    emits: ['selection-changed'],
    data: function () {
        return {
            valueAll: 'all',
            selectedFilterItem: null,
        };
    },
    mounted: function () {
        // TODO: Get from session storage
        this.selectedFilterItem = this.valueAll;
    },
};
</script>
