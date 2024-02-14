<template>
    <div class="row p-1">
        <div class="col-4 text-start d-flex align-items-center capitalize">
            {{ replaceUnderscores(name) }}
        </div>
        <div class="text-start" :class="colWidth">
            <slot></slot>
        </div>
    </div>
</template>

<script>
import { helpers } from "@/utils/hooks";

export default {
    name: "RowSlotTemplate",
    props: {
        name: {
            type: String,
            required: true,
        },
        colWidth: {
            type: String,
            required: false,
            default: "col-4",
        },
    },
    methods: {
        replaceUnderscores: helpers.replaceUnderscores,
    },
};
</script>
