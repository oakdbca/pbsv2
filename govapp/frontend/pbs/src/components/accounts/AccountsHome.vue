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
                    <AssignedItems :assigned-items="assignedItems" />
                    <EndorsmentItems
                        :items-awaiting-endorsement="itemsAwaitingEndorsement"
                    />
                </div>
            </div>
        </div>
    </LayoutDetails>
</template>

<script>
import { useStore } from '@/stores/state';

import ItemList from '@/components/accounts/ItemList.vue';
import LayoutDetails from '@/components/layout/LayoutDetails.vue';
import LatestMessages from '@/components/accounts/LatestMessages.vue';
import AssignedItems from '@/components/accounts/AssignedItems.vue';
import EndorsmentItems from '@/components/accounts/EndorsmentItems.vue';

export default {
    name: 'AccountsHome',
    components: {
        AssignedItems,
        EndorsmentItems,
        ItemList,
        LatestMessages,
        LayoutDetails,
    },
    data() {
        return {
            store: useStore(),
            now: Date.now(),
            loading: true,
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
    beforeUnmount() {
        clearInterval(this.now);
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
    },
};
</script>
