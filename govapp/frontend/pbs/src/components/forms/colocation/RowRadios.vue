<template>
    <RowSlotTemplate :name="name" col-width="col-8">
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
                    :required="required"
                    :disabled="disabled"
                    @change="
                        $emit(
                            'update:value',
                            /** @type {any} */ ($event.target).value
                        )
                    "
                />
                <label :for="item" class="form-check-label capitalize ms-1">{{
                    replaceUnderscores(item)
                }}</label>
            </div>
        </div>
    </RowSlotTemplate>
</template>

<script>
import { helpers } from '@/utils/hooks';
import RowSlotTemplate from '@/components/forms/colocation/RowSlotTemplate.vue';

export default {
    name: 'RowRadiosComponent',
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
