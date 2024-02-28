<template>
    <template v-if="assignableUsers">
        <select
            id="assigned-to"
            v-model="assignedToComputed"
            class="form-select"
        >
            <option
                v-for="user in assignableUsers"
                :key="user.id"
                :value="user.id"
            >
                {{ user.name }}
            </option>
        </select>
    </template>
    <template v-else>
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </template>
</template>

<script>
export default {
    name: 'SelectAssignable',
    props: {
        assignableUsers: {
            type: Array,
            required: false,
            default: null,
        },
        assignedTo: {
            type: Number,
            required: true,
        },
    },
    emits: ['assignTo'],
    computed: {
        assignedToComputed: {
            get() {
                return this.assignedTo;
            },
            set(value) {
                this.$emit('assignTo', value);
            },
        },
    },
};
</script>
