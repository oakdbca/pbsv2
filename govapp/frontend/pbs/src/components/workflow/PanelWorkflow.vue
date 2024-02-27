<template>
    <div class="card mb-3">
        <div class="card-header">Workflow</div>
        <div class="card-body border-bottom">
            <div class="input-group">
                <span id="basic-addon1" class="input-group-text">Status</span>
                <input
                    :value="status"
                    type="text"
                    class="form-control"
                    placeholder="Username"
                    aria-label="Username"
                    aria-describedby="basic-addon1"
                    disabled
                />
            </div>
        </div>
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
import PanelAssignable from '@/components/workflow/PanelAssignable.vue';

export default {
    name: 'OperationalPlan',
    components: {
        PanelAssignable,
    },
    props: {
        status: {
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
