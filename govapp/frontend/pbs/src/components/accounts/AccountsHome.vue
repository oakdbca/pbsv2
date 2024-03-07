<template>
    <LayoutDetails left-menu-col-width="4" :loading="loading">
        <template #heading>
            <h3 class="text-secondary">{{ heading }}</h3>
        </template>
        <template #left-menu>
            <div class="card mb-3">
                <div class="card-header">Messages</div>
                <div class="card-body">
                    <div v-if="toasts" class="toast-container">
                        <div
                            class="toast show"
                            role="alert"
                            aria-live="assertive"
                            aria-atomic="true"
                        >
                            <div class="toast-header bg-success text-white">
                                <strong class="me-auto"
                                    >Burn Plan Element Approved
                                </strong>
                                <small class="text-white">just now</small>
                                <button
                                    type="button"
                                    class="btn-close btn-close-white"
                                    data-bs-dismiss="toast"
                                    aria-label="Close"
                                ></button>
                            </div>
                            <div class="toast-body">
                                A burn plan element BPE000109 that you endorsed
                                has been approved by:
                                <div class="mt-2">
                                    John Johns (Corporate Executive)
                                </div>
                            </div>
                        </div>

                        <div
                            class="toast show"
                            role="alert"
                            aria-live="assertive"
                            aria-atomic="true"
                        >
                            <div class="toast-header bg-primary text-white">
                                <strong class="me-auto"
                                    >Burn Plan Element Assignment
                                </strong>
                                <small class="text-white">5 hours ago</small>
                                <button
                                    type="button"
                                    class="btn-close btn-close-white"
                                    data-bs-dismiss="toast"
                                    aria-label="Close"
                                ></button>
                            </div>
                            <div class="toast-body">
                                A new burn plan element BPE000099 has been
                                assigned to you:
                                <div class="mt-2">
                                    Fred Smith (Swan Coastal, District Manager)
                                </div>
                            </div>
                        </div>

                        <div
                            class="toast"
                            role="alert"
                            aria-live="assertive"
                            aria-atomic="true"
                        >
                            <div class="toast-header bg-primary text-white">
                                <img src="" class="rounded me-2" alt="" />
                                <strong class="me-auto"
                                    >Aviation Awaiting Endorsement</strong
                                >
                                <small class="text-white">2 days ago</small>
                                <button
                                    type="button"
                                    class="btn-close btn-close-white"
                                    data-bs-dismiss="toast"
                                    aria-label="Close"
                                ></button>
                            </div>
                            <div class="toast-body">
                                Aviation request AR000343 is awaiting your
                                endorsement:
                                <div class="mt-2">
                                    Greg Sidebottom (Swan, Region Manager)
                                </div>
                            </div>
                        </div>

                        <div
                            class="toast"
                            role="alert"
                            aria-live="assertive"
                            aria-atomic="true"
                        >
                            <div class="toast-header bg-primary text-white">
                                <img src="" class="rounded me-2" alt="" />
                                <strong class="me-auto"
                                    >Another Important Message</strong
                                >
                                <small class="text-white">5 days ago</small>
                                <button
                                    type="button"
                                    class="btn-close btn-close-white"
                                    data-bs-dismiss="toast"
                                    aria-label="Close"
                                ></button>
                            </div>
                            <div class="toast-body">
                                You're in big trouble for not working fast
                                enough.
                                <div class="mt-2">
                                    John Johns (Corporate Executive)
                                </div>
                            </div>
                        </div>
                    </div>
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
                            <button class="btn btn-primary btn-sm float-end">
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
                            <button class="btn btn-primary btn-sm float-end">
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

export default {
    name: 'AccountsHome',
    components: {
        BadgeStatus,
        ItemList,
        LayoutDetails,
        TimeSince,
    },
    data() {
        return {
            store: useStore(),
            now: Date.now(),
            loading: true,
            toasts: [
                {
                    title: 'Burn Plan Element Approved',
                    message:
                        'A burn plan element BPE000109 that you endorsed has been approved by:',
                    from: 'John Johns (Corporate Executive)',
                    time: 'just now',
                    type: 'success',
                },
                {
                    title: 'Burn Plan Element Assignment',
                    message:
                        'A new burn plan element BPE000099 has been assigned to you:',
                    from: 'Fred Smith (Swan Coastal, District Manager)',
                    time: '5 hours ago',
                    type: 'primary',
                },
                {
                    title: 'Aviation Awaiting Endorsement',
                    message:
                        'Aviation request AR000343 is awaiting your endorsement:',
                    from: 'Greg Sidebottom (Swan, Region Manager)',
                    time: '2 days ago',
                    type: 'primary',
                },
                {
                    title: 'Another Important Message',
                    message:
                        "You're in big trouble for not working fast enough.",
                    from: 'John Johns (Corporate Executive)',
                    time: '5 days ago',
                    type: 'primary',
                },
            ],
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
    },
};
</script>
