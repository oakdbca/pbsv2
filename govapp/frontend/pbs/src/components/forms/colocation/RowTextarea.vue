<template>
    <RowSlotTemplate :name="name">
        <textarea
            :id="`textarea-${name}`"
            :value="value"
            class="form-control"
            :required="required"
            :disabled="disabled"
            @change="
                $emit('update:value', /** @type {any} */ ($event.target).value)
            "
        ></textarea>
    </RowSlotTemplate>
</template>

<script>
import { helpers } from '@/utils/hooks';
import RowSlotTemplate from '@/components/forms/colocation/RowSlotTemplate.vue';

export default {
    name: 'RowTextComponent',
    components: {
        RowSlotTemplate,
    },
    props: {
        name: {
            type: String,
            required: true,
        },
        value: {
            type: [String, Number],
            required: false,
            default: '',
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
