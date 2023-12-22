<template>
    <div class="row p-1">
        <div class="col-4 text-start capitalize">
            {{ replaceUnderscores(name) }}
        </div>
        <div class="col-8 text-start">
            <div class="row">
                <div
                    v-for="item in selection"
                    :key="item"
                    class="col-2 text-nowrap"
                >
                    <input
                        :id="`radio-input-${item}`"
                        :value="item"
                        :checked="item === selectedValue"
                        class="form-check-input"
                        type="radio"
                        :name="item"
                        :disabled="disabled"
                        @change="
                            $emit(
                                'update:value',
                                /** @type {any} */ ($event.target).value
                            )
                        "
                    />
                    <label
                        :for="item"
                        class="form-check-label capitalize ms-1"
                        >{{ replaceUnderscores(item) }}</label
                    >
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { helpers } from '@/utils/hooks';

export default {
    name: 'RowRadiosComponent',
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
