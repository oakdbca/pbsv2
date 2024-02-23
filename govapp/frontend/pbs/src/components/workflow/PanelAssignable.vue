<template>
    <div class="mb-3">
        <label for="assigned-to" class="form-label">Assigned To</label>
        <SelectAssignable
            :content-type="contentType"
            :pk="pk"
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
import { api_endpoints, utils } from '@/utils/hooks';

import { useStore } from '@/stores/state';

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
        assignedTo: {
            type: Number,
            required: true,
        },
    },
    emits: ['assignToMe', 'assignTo'],
    data() {
        return {
            store: useStore(),
        };
    },
    computed: {
        assignedToMe() {
            return this.store.userData.id === this.assignedTo;
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
        assignToMe() {
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
            utils
                .fetchUrl(api_endpoints.assignToMe(), requestOptions)
                .then((data) => {
                    console.log(data);
                    this.$emit('assignTo', data.user_id);
                });
            this.$emit('assignToMe');
        },
        assignTo(value) {
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
            utils
                .fetchUrl(
                    api_endpoints.assignTo() +
                        `?content_type=${this.content_type}&object_id=${this.pk}&user_id=${value}`,
                    requestOptions,
                )
                .then((response) => {
                    console.log(response);
                });
            this.$emit('assignTo', value);
        },
    },
};
</script>
