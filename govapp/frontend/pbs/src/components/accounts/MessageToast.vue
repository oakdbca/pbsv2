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
            <small class="text-white">{{ message.time }}</small>
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
export default {
    name: 'MessageToast',
    props: {
        message: {
            type: Object,
            required: true,
        },
    },
    emits: ['dismissMessage'],
};
</script>
