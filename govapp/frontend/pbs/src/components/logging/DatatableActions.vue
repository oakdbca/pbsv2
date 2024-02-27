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
import { api_endpoints } from '@/utils/hooks';
import DataTableTemplate from '@/components/forms/colocation/DataTableTemplate.vue';

export default {
    name: 'DatatableActions',
    components: { DataTableTemplate },
    props: {
        contentType: {
            type: Number,
            required: true,
        },
        pk: {
            type: Number,
            required: true,
        },
    },
    data: function () {
        return {
            ajax: '',
        };
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
    mounted: async function () {
        this.$nextTick(() => {
            this.ajax =
                api_endpoints.actions() +
                `?format=datatables&content_type${this.contentType}&object_id=${this.pk}`;
        });
    },
};
</script>
