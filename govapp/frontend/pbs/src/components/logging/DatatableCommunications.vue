<template>
    <DataTableTemplate
        name="Communciation Logs"
        :ajax="communicationsApiUrl"
        :columns="columns"
    >
    </DataTableTemplate>
</template>

<script>
import DataTableTemplate from '@/components/forms/colocation/DataTableTemplate.vue';

export default {
    name: 'DatatableCommunications',
    components: { DataTableTemplate },
    props: {
        communicationsApiUrl: {
            type: String,
            required: true,
        },
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
};
</script>
