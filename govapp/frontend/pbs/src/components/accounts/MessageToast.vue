<template>
    <div
        v-if="message"
        :id="`message-${message.id}`"
        class="toast show"
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
    >
        <div
            class="toast-header bg-success text-white"
            :class="`bg-${message.type}`"
        >
            <strong class="me-auto">{{ message.subject }} </strong>
            <small class="text-white"
                ><TimeSince :date="message.created" suffix=" ago"
            /></small>
            <button
                type="button"
                class="btn-close btn-close-white"
                data-bs-dismiss="toast"
                aria-label="Close"
                @click="$emit('dismissMessage', message.id)"
            ></button>
        </div>
        <div class="toast-body">
            {{ message.content }}
            <div class="mt-2">From: {{ message.sender.username }}</div>
        </div>
    </div>
</template>

<script>
import TimeSince from '@/utils/vue/TimeSince.vue';

export default {
    name: 'MessageToast',
    components: {
        TimeSince,
    },
    props: {
        message: {
            type: Object,
            required: true,
        },
    },
    emits: ['dismissMessage'],
};
</script>
