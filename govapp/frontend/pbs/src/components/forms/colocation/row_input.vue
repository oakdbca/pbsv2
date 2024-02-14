<template>
    <RowSlotTemplate :name="name">
        <input
            :id="`text-input-${name}`"
            :value="value"
            class="form-control"
            :pattern="pattern"
            :required="required"
            :disabled="disabled"
            @change="
                $emit('update:value', /** @type {any} */ ($event.target).value)
            "
        />
    </RowSlotTemplate>
</template>

<script>
import { helpers } from "@/utils/hooks";
import RowSlotTemplate from "@/components/forms/colocation/row_slot_template.vue";

export default {
    name: "RowInputComponent",
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
            required: true,
        },
        pattern: {
            type: String,
            required: false,
            default: ".*",
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
    emits: ["update:value"],
    methods: {
        replaceUnderscores: helpers.replaceUnderscores,
    },
};
</script>
