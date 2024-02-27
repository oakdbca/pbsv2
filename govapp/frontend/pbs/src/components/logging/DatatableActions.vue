<template>
    <DataTableTemplate
        v-if="ajax"
        name="Actions"
        :ajax="ajax"
        :columns="columns"
    >
    </DataTableTemplate>
</template>

<script>
import DataTableTemplate from '@/components/forms/colocation/DataTableTemplate.vue';

export default {
    name: 'DatatableActions',
    components: { DataTableTemplate },
    props: {
        ajax: {
            type: String,
            required: true,
        },
    },
    computed: {
        columns: function () {
            return [
                { data: 'id', title: 'ID', visible: false },
                { data: 'username', title: 'Who' },
                { data: 'what', title: 'What' },
                { data: 'when', title: 'When' },
            ];
        },
    },
};
</script>
