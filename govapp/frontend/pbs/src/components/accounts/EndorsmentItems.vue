<template>
    <div class="card mb-3">
        <div class="card-header">Items Awaiting Your Endorsement</div>
        <div class="card-body">
            <template
                v-if="
                    itemsAwaitingEndorsement &&
                    itemsAwaitingEndorsement.length > 0
                "
            >
                <ItemList class="mb-3" :items="itemsAwaitingEndorsement" />
                <button
                    v-if="itemsAwaitingEndorsement.length > 5"
                    class="btn btn-primary btn-sm float-end"
                    @click="viewAllItems"
                >
                    View all <i class="bi bi-back ps-1"></i>
                </button>
            </template>
            <template v-else>
                <span class="text-muted"
                    >There are currently no items awaiting your endosement</span
                >
            </template>
        </div>
    </div>
</template>

<script>
import { apiEndpoints, utils } from '@/utils/hooks';

import ItemList from '@/components/accounts/ItemList.vue';

export default {
    name: 'EndorsmentItems',
    components: {
        ItemList,
    },
    data: function () {
        return {
            itemsAwaitingEndorsement: [],
        };
    },
    created() {
        this.fetchEndorsementItems();
    },
    methods: {
        fetchEndorsementItems() {
            utils.fetchUrl(apiEndpoints.endorsmentItems()).then((data) => {
                this.itemsAwaitingEndorsement = data;
            });
        },
    },
};
</script>
