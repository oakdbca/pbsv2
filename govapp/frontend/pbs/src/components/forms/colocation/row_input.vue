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
                :disabled="disabled"
                :pattern="pattern"
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
        disabled: {
            type: Boolean,
            required: false,
            default: false,
        },
        pattern: {
            type: String,
            required: false,
            default: '.*',
        },
    },
    emits: ['update:value'],
    methods: {
        replaceUnderscores: helpers.replaceUnderscores,
    },
};
</script>
