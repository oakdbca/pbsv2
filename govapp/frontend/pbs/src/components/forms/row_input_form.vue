<template>
    <div class="row p-1">
        <div class="col-4 text-start capitalize">
            {{ replaceUnderscores(idx) }}
        </div>
        <div class="col-4 text-start">
            <input
                :id="`text-input-${idx}`"
                :value="field"
                class="form-control"
                :disabled="disabled"
                @change="
                    $emit(
                        'update:field',
                        /** @type {any} */ ($event.target).value
                    )
                "
            />
        </div>
    </div>
</template>

<script>
export default {
    name: 'RowInputForm',
    props: {
        idx: {
            type: String,
            required: true,
        },
        field: {
            type: [String, Number],
            required: true,
        },
        disabled: {
            type: Boolean,
            required: false,
            default: false,
        },
    },
    emits: ['update:field'],
    methods: {
        replaceUnderscores: function (/** @type {string} */ str) {
            return str.replace(/_/g, ' ');
        },
    },
};
</script>
