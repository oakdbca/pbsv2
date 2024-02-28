<template>
    <div class="card mb-3">
        <div class="card-header">Workflow</div>
        <PanelStatus :status="status" :status-display="statusDisplay" />
        <div v-if="assignableUsers" class="card-body">
            <PanelAssignable
                :content-type="contentType"
                :pk="pk"
                :assignable-users="assignableUsers"
                :assign-to-me-api-url="assignToMeApiUrl"
                :assign-to-api-url="assignToApiUrl"
                :assigned-to="assignedTo"
                :request-user-id="requestUserId"
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
            required: false,
            default: null,
        },
        contentType: {
            type: Number,
            required: true,
        },
        pk: {
            type: Number,
            required: true,
        },
        assignableUsers: {
            type: Array,
            required: false,
            default: null,
        },
        assignToMeApiUrl: {
            type: String,
            required: false,
            default: null,
        },
        assignToApiUrl: {
            type: String,
            required: false,
            default: null,
        },
        assignedTo: {
            type: Number,
            required: true,
        },
        requestUserId: {
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
