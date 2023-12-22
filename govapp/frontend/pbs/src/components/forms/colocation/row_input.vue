<template>
    <div class="row p-1">
        <div class="col-4 text-start d-flex align-items-center capitalize">
            {{ replaceUnderscores(name) }}
        </div>
        <div class="col-4 text-start">
            <input
                :id="`text-input-${name}`"
                :value="value"
                class="form-control"
                :pattern="pattern"
                :required="required"
                :disabled="disabled"
                @change="
                    $emit(
                        'update:value',
                        /** @type {any} */ ($event.target).value
                    )
                "
            />
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
        value: {
            type: [String, Number],
            required: true,
        },
        pattern: {
            type: String,
            required: false,
            default: '.*',
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
