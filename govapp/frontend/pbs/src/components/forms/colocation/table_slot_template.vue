<!-- Slot in table bodies -->
<template>
    <div class="row p-1">
        <div class="col-4 text-start d-flex align-items-center capitalize">
            {{ name }}
        </div>
        <div class="text-start">
            <table class="table text-small">
                <thead>
                    <tr>
                        <th
                            v-for="header in headers"
                            :key="`table-${name}-${header}`"
                            scope="col"
                        >
                            {{ replaceUnderscores(header) }}
                        </th>
                    </tr>
                </thead>
                <slot></slot>
            </table>
        </div>
    </div>
</template>

<script>
import { helpers } from '@/utils/hooks';

export default {
    name: 'TableSlotTemplate',
    props: {
        name: {
            type: String,
            required: true,
        },
        headers: {
            type: Array,
            required: false,
            default: () => [],
        },
    },
    methods: {
        replaceUnderscores: helpers.replaceUnderscores,
    },
};
</script>
