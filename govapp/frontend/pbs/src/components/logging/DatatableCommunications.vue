<template>
    <DataTableTemplate
        v-if="ajax"
        name="Communciation Logs"
        :ajax-data-string="ajax"
        :columns="columns"
    >
    </DataTableTemplate>
</template>

<script>
import { api_endpoints } from '@/utils/hooks';
import DataTableTemplate from '@/components/forms/colocation/datatable_template.vue';

export default {
    name: 'DatatableCommunications',
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
                { data: 'created_at', title: 'Date' },
                { data: 'type', title: 'Type' },
                { data: 'to', title: 'To' },
                { data: 'from', title: 'From' },
                { data: 'subject', title: 'Subject' },
            ];
        },
    },
    mounted: async function () {
        this.$nextTick(() => {
            this.ajax =
                api_endpoints.communications() +
                `?format=datatables&content_type${this.contentType}&object_id=${this.pk}`;
        });
    },
};
</script>
