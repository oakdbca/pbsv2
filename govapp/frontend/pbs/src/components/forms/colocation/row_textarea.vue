<template>
    <div class="row p-1">
        <div class="col-4 text-start d-flex align-items-center capitalize">
            {{ replaceUnderscores(name) }}
        </div>
        <div class="col-4 text-start">
            <textarea
                :id="`textarea-${name}`"
                :value="value"
                class="form-control"
                :disabled="disabled"
                @change="
                    $emit(
                        'update:value',
                        /** @type {any} */ ($event.target).value
                    )
                "
            ></textarea>
        </div>
    </div>
</template>

<script>
import { helpers } from '@/utils/hooks';

export default {
    name: 'RowTextComponent',
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
