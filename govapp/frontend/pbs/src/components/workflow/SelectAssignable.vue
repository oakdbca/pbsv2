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
import { api_endpoints, utils } from '@/utils/hooks';

export default {
    name: 'SelectAssignable',
    props: {
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
    emits: ['assignTo'],
    data() {
        return {
            assignableUsers: null,
        };
    },
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
    created() {
        this.fetchAssignableUsers();
    },
    methods: {
        fetchAssignableUsers() {
            utils
                .fetchUrl(
                    api_endpoints.assignableUsers() +
                        `?content_type=${this.contentType}&object_id=${this.pk}`,
                )
                .then((data) => {
                    this.assignableUsers = data;
                });
        },
    },
};
</script>
