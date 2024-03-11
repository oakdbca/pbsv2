<template>
    <div class="card mb-3">
        <div class="card-header">Items Assigned to You</div>
        <div class="card-body">
            <template v-if="assignedItems && assignedItems.length > 0">
                <ItemList class="mb-3" :items="assignedItems" />
                <button
                    v-if="assignedItems.length > 5"
                    class="btn btn-primary btn-sm float-end"
                    @click="viewAllItems"
                >
                    View all <i class="bi bi-back ps-1"></i>
                </button>
            </template>
            <template v-else>
                <span class="text-muted"
                    >There are currently no items assigned to you</span
                >
            </template>
        </div>
    </div>
</template>

<script>
import { apiEndpoints, utils } from '@/utils/hooks';

import ItemList from '@/components/accounts/ItemList.vue';

export default {
    name: 'AssignedItems',
    components: {
        ItemList,
    },
    data: function () {
        return {
            assignedItems: [],
        };
    },
    created() {
        this.fetchAssignedItems();
    },
    methods: {
        fetchAssignedItems() {
            utils.fetchUrl(apiEndpoints.assignedItems()).then((data) => {
                this.assignedItems = data;
            });
        },
    },
};
</script>
