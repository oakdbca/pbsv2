<template>
    <DataTableTemplate
        ref="communicationLogs"
        name="communicationLogs"
        :ajax="communicationsApiUrl"
        :columns="columns"
        @mounted="addEventListeners"
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
    emits: ['selected-communication-log'],
    computed: {
        columns: function () {
            return [
                { data: 'id', title: 'ID', visible: false },
                { data: 'created_at', title: 'Date Logged' },
                { data: 'type', title: 'Type' },
                { data: 'to', title: 'To' },
                { data: 'subject', title: 'Subject' },
                {
                    data: 'id',
                    title: 'Actions',
                    render: function (row, type, full) {
                        var object = JSON.stringify(full);
                        return `<a href="#" data-action="view" data-object="${object}" class="btn btn-primary btn-sm">View Details <i class="bi bi-back ps-1"></i></a>`;
                    },
                },
            ];
        },
    },
    methods: {
        addEventListeners: function () {
            var vm = this;
            var table =
                this.$refs.communicationLogs.$refs.communicationLogsDatatable
                    .dt;
            table.on('click', 'tbody tr a[data-action]', function () {
                vm.selectedCommunicationLog = table
                    .row(this.closest('tr'))
                    .data();
                vm.$emit(
                    'selected-communication-log',
                    vm.selectedCommunicationLog
                );
            });
        },
    },
};
</script>
