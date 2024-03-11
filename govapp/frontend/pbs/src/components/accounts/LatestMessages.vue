<template>
    <div
        v-if="messages && Object.keys(messages).length > 0"
        class="toast-container"
    >
        <MessageToast
            v-for="message in Object.values(messages)"
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
