<template>
    <LayoutDetails left-menu-col-width="4" :loading="loading">
        <template #heading>
            <h3 class="text-secondary">{{ heading }}</h3>
        </template>
        <template #left-menu>
            <div class="card mb-3">
                <div class="card-header">
                    Messages
                    <small class="float-end"
                        ><button
                            class="btn btn-sm btn-secondary"
                            @click="viewMessageHistory"
                        >
                            View Message History
                            <i class="bi bi-clock-history ms-1"></i></button
                    ></small>
                </div>
                <div class="card-body">
                    <LatestMessages />
                </div>
            </div>
        </template>
        <div class="container">
            <div class="row">
                <div class="col">
                    <div class="card mb-3">
                        <div class="card-header">Items Assigned to You</div>
                        <div class="card-body">
                            <ItemList class="mb-3" />
                            <button
                                class="btn btn-primary btn-sm float-end"
                                @click="viewAllItems"
                            >
                                View all <i class="bi bi-back ps-1"></i>
                            </button>
                        </div>
                    </div>
                    <div class="card mb-3">
                        <div class="card-header">
                            Items Awaiting Your Endorsement
                        </div>
                        <div class="card-body">
                            <ItemList class="mb-3" />
                            <button
                                class="btn btn-primary btn-sm float-end"
                                @click="viewAllItems"
                            >
                                View all <i class="bi bi-back ps-1"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </LayoutDetails>
</template>

<script>
import { useStore } from '@/stores/state';

import TimeSince from '@/utils/vue/TimeSince.vue';
import ItemList from '@/components/forms/ItemList.vue';
import BadgeStatus from '@/components/forms/BadgeStatus.vue';
import LayoutDetails from '@/components/layout/LayoutDetails.vue';
import LatestMessages from '@/components/accounts/LatestMessages.vue';

export default {
    name: 'AccountsHome',
    components: {
        BadgeStatus,
        ItemList,
        LatestMessages,
        LayoutDetails,
        TimeSince,
    },
    data() {
        return {
            store: useStore(),
            now: Date.now(),
            loading: true,
            messages: {
                1: {
                    title: 'Burn Plan Element Approved',
                    message:
                        'A burn plan element BPE000109 that you endorsed has been approved by:',
                    from: 'John Johns (Corporate Executive)',
                    time: 'just now',
                    type: 'success',
                },
                2: {
                    title: 'Burn Plan Element Assignment',
                    message:
                        'A new burn plan element BPE000099 has been assigned to you:',
                    from: 'Fred Smith (Swan Coastal, District Manager)',
                    time: '5 hours ago',
                    type: 'primary',
                },
                3: {
                    title: 'Aviation Awaiting Endorsement',
                    message:
                        'Aviation request AR000343 is awaiting your endorsement:',
                    from: 'Greg Sidebottom (Swan, Region Manager)',
                    time: '2 days ago',
                    type: 'primary',
                },
                4: {
                    title: 'Another Important Message',
                    message:
                        "You're in big trouble for not working fast enough.",
                    from: 'John Johns (Corporate Executive)',
                    time: '5 days ago',
                    type: 'primary',
                },
            },
        };
    },
    computed: {
        timeSinceLastLogin() {
            if (this.store.userData.last_login) {
                return this.now - new Date(this.store.userData.last_login);
            }
            return null;
        },
        heading() {
            if (this.timeSinceLastLogin) {
                if (this.timeSinceLastLogin < 60000) {
                    return `Welcome back ${this.store.userData.first_name}`;
                } else {
                    return 'User Dashboard';
                }
            }
            return '';
        },
    },
    created() {
        setInterval(() => {
            this.now = Date.now();
        }, 1000);
    },
    mounted() {
        this.loading = false;
        this.$nextTick(() => {
            this.showToasts();
        });
    },
    methods: {
        showToasts() {
            var toastElList = [].slice.call(
                document.querySelectorAll('.toast')
            );
            var toastList = toastElList.map(function (toastEl) {
                return new bootstrap.Toast(toastEl, { autohide: false });
            });
            for (var i = 0; i < toastList.length; i++) {
                toastList[i].show();
            }
        },
        viewMessageHistory() {
            alert('TODO: Show message history');
        },
        viewAllItems() {
            alert('TODO: Show all items');
        },
        markDismissed(id) {
            delete this.messages[id];
            console.log(
                'TODO: Mark message as dismissed in api so it does not show here again. ',
                id
            );
        },
    },
};
</script>
