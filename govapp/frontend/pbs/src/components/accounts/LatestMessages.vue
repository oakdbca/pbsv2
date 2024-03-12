<template>
    <div
        v-if="messages && Object.keys(messages).length > 0"
        class="toast-container"
    >
        <MessageToast
            v-for="message in orderedMessages"
            :key="message.id"
            :message="message"
            @dismiss-message="markDismissed"
        />
    </div>
    <div v-else class="text-secondary">No new messages to display</div>
</template>

<script>
import { apiEndpoints, utils } from '@/utils/hooks';

import MessageToast from '@/components/accounts/MessageToast.vue';

export default {
    name: 'LatestMessages',
    components: {
        MessageToast,
    },
    data: () => ({
        messages: null,
    }),
    computed: {
        orderedMessages() {
            // Javascript will reorder the response object keys according to it's own rules
            // so we need to sort it again
            return Object.values(this.messages).sort(
                (a, b) => new Date(b.created) - new Date(a.created)
            );
        },
    },
    created() {
        this.fetchLatestMessages();
    },
    methods: {
        async fetchLatestMessages() {
            await utils
                .fetchUrl(apiEndpoints.latestMessages(), {
                    method: 'GET',
                })
                .then((data) => {
                    this.messages = Object.assign({}, data);
                });
        },
        async markDismissed(id) {
            await utils
                .fetchUrl(apiEndpoints.dismissMessage(id), {
                    method: 'PATCH',
                })
                .then(() => {
                    delete this.messages[Number(id).toString()];
                });
        },
    },
};
</script>
