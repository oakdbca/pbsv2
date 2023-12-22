<template>
    <div class="row p-1">
        <div class="col-4 text-start capitalize">
            {{ replaceUnderscores(name) }}
        </div>
        <div class="col-4 text-start">
            <select
                :id="`select-${name}`"
                class="form-select"
                :disabled="disabled"
                @change="
                    $emit(
                        'update:value',
                        /** @type {any} */ ($event.target).value
                    )
                "
            >
                <option
                    v-for="item in selection"
                    :key="`select-${name}-${item}`"
                    :value="item"
                    :selected="selectedValue === item"
                    class="capitalize"
                >
                    {{ item.charAt(0).toUpperCase() + item.slice(1) }}
                </option>
            </select>
        </div>
    </div>
</template>

<script>
import { helpers } from '@/utils/hooks';

export default {
    name: 'RowInputComponent',
    props: {
        name: {
            type: String,
            required: true,
        },
        selection: {
            type: Array,
            required: true,
        },
        selectedValue: {
            type: [String, Number],
            required: true,
        },
        disabled: {
            type: Boolean,
            required: false,
            default: false,
        },
    },
    emits: ['update:value'],
    methods: {
        replaceUnderscores: helpers.replaceUnderscores,
    },
};
</script>
