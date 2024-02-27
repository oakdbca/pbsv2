<template>
    <div class="mb-3">
        <label for="assigned-to" class="form-label">Assigned To</label>
        <SelectAssignable
            :assignable-users="assignableUsers"
            :assigned-to="assignedTo"
            @assign-to="assignTo"
        />
    </div>
    <div class="mb-3">
        <button
            type="button"
            class="btn btn-primary float-end"
            :disabled="assignedToMe"
            @click.prevent="assignToMe"
        >
            {{ assignToMeButtonText }}
            <i class="bi" :class="assignToMeIconClass"></i>
        </button>
    </div>
</template>

<script>
import SelectAssignable from './SelectAssignable.vue';

export default {
    name: 'PanelAssignable',
    components: {
        SelectAssignable,
    },
    props: {
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
        assignedTo: {
            type: Number,
            required: true,
        },
        requestUserId: {
            type: Number,
            required: true,
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
    },
    emits: ['assignToMe', 'assignTo'],
    computed: {
        assignedToMe() {
            return this.requestUserId === this.assignedTo;
        },
        assignToMeButtonText() {
            return this.assignedToMe ? 'Assigned to you' : 'Assign to me';
        },
        assignToMeIconClass() {
            return this.assignedToMe
                ? 'bi-person-fill-check'
                : 'bi-person-raised-hand';
        },
    },
    methods: {
        async assignToMe() {
            const requestOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content_type: this.contentType,
                    object_id: this.pk,
                }),
            };
            await fetch(this.assignToMeApiUrl, requestOptions).then(
                async (response) => {
                    await response.json().then((data) => {
                        this.$emit('assignTo', data.user_id);
                    });
                }
            );
            this.$emit('assignToMe');
        },
        async assignTo(value) {
            const requestOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content_type: this.contentType,
                    object_id: this.pk,
                    user_id: value,
                }),
            };
            await fetch(this.assignToApiUrl, requestOptions);
            this.$emit('assignTo', value);
        },
    },
};
</script>
