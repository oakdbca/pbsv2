<template>
    <div class="card mb-3">
        <div class="card-header">Workflow</div>
        <PanelStatus :status="status" :status-display="statusDisplay" />
        <div class="card-body">
            <PanelAssignable
                :content-type="contentType"
                :pk="pk"
                :assigned-to="assignedTo"
                @assign-to-me="$emit('assignToMe')"
                @assign-to="assignTo"
            />
        </div>
        <slot
            ><!-- Add any custom workflow elements as card bodies to the parent component --></slot
        >
    </div>
</template>

<script>
import PanelStatus from '@/components/workflow/PanelStatus.vue';
import PanelAssignable from '@/components/workflow/PanelAssignable.vue';

export default {
    name: 'OperationalPlan',
    components: {
        PanelStatus,
        PanelAssignable,
    },
    props: {
        status: {
            type: String,
            required: true,
        },
        statusDisplay: {
            type: String,
            required: true,
        },
        contentType: {
            type: Number,
            required: true,
        },
        pk: {
            type: Number,
            required: true,
        },
        assignedTo: {
            type: Number,
            required: true,
        },
    },
    emits: ['assignToMe', 'assignTo'],
    created() {},
    methods: {
        assignTo(value) {
            this.$emit('assignTo', value);
        },
    },
};
</script>
