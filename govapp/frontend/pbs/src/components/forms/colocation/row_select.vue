<template>
    <RowSlotTemplate :name="name">
        <select
            :id="`select-${name}`"
            class="form-select"
            :required="required"
            :disabled="disabled"
            @change="
                $emit('update:value', /** @type {any} */ ($event.target).value)
            "
        >
            <option
                :value="null"
                :disabled="true"
                :selected="selectedValue == null"
            >
                {{ selectText }}
            </option>
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
    </RowSlotTemplate>
</template>

<script>
import { helpers } from '@/utils/hooks';
import RowSlotTemplate from '@/components/forms/colocation/row_slot_template.vue';

export default {
    name: 'RowInputComponent',
    components: {
        RowSlotTemplate,
    },
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
            required: false,
            default: null,
        },
        selectText: {
            type: String,
            required: false,
            default: 'Select a value',
        },
        required: {
            type: Boolean,
            required: false,
            default: false,
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
