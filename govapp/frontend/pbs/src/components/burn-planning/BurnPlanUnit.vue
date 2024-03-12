<template>
    <LayoutDetails :loading="!burnPlanUnit">
        <template #heading>
            <h3>
                Burn Planning Unit:
                <span class="text-secondary">{{
                    burnPlanUnit.reference_number
                }}</span>
            </h3>
        </template>
        <template #left-menu>
            <PanelLogs
                :communications-api-url="communicationsApiUrl"
                :post-communications-entry-api-url="
                    postCommunicationsEntryApiUrl
                "
                :actions-api-url="actionsApiUrl"
                :content-type="burnPlanUnit.content_type"
                :object-id="burnPlanUnit.id"
            />
            <PanelWorkflow
                :status="burnPlanUnit.status"
                :status-display="burnPlanUnit.status_display"
                :content-type="burnPlanUnit.content_type"
                :pk="burnPlanUnit.id"
                :assignable-users="assignableUsers"
                :assign-to-me-api-url="assignToMeApiUrl"
                :assign-to-api-url="assignToApiUrl"
                :assigned-to="burnPlanUnit.assigned_to"
                :request-user-id="store.userData.id"
                @assign-to="assignTo"
            ></PanelWorkflow>
            <div class="card">
                <div class="card-header">Actions</div>
                <div class="card-body">
                    <button class="btn btn-primary">Submit</button>
                </div>
            </div>
        </template>
        <BootstrapAccordion id="burn-plan-unit-accordion">
            <BootstrapAccordionItem
                :id="`${burnPlanUnit.content_type}-${burnPlanUnit.id}-details`"
                heading="Details"
            >
                Details body
            </BootstrapAccordionItem>
            <BootstrapAccordionItem
                :id="`${burnPlanUnit.content_type}-${burnPlanUnit.id}-documents`"
                heading="Documents"
            >
                Documents
            </BootstrapAccordionItem>
        </BootstrapAccordion>
    </LayoutDetails>
</template>

<script>
import { useUserStore } from '@/stores/user';

import { apiEndpoints, utils } from '@/utils/hooks';

import LayoutDetails from '../layout/LayoutDetails.vue';

import BootstrapAccordion from '../forms/BootstrapAccordion.vue';
import BootstrapAccordionItem from '../forms/BootstrapAccordionItem.vue';

import PanelLogs from '../logging/PanelLogs.vue';

export default {
    name: 'BurnPlanUnit',
    components: {
        LayoutDetails,
        PanelLogs,
        BootstrapAccordion,
        BootstrapAccordionItem,
    },
    data() {
        return {
            store: useUserStore(),
            burnPlanUnit: null,
            assignableUsers: null,
        };
    },
    computed: {
        communicationsApiUrl: function () {
            return (
                apiEndpoints.communications() +
                `?format=datatables&content_type=${this.burnPlanUnit?.content_type}&object_id=${this.burnPlanUnit?.id}`
            );
        },
        postCommunicationsEntryApiUrl() {
            return apiEndpoints.communications();
        },
        actionsApiUrl: function () {
            return (
                apiEndpoints.actions() +
                `?format=datatables&content_type=${this.burnPlanUnit?.content_type}&object_id=${this.burnPlanUnit?.id}`
            );
        },
        assignableUsersApiUrl() {
            return apiEndpoints.assignableUsers();
        },
        assignToMeApiUrl() {
            return apiEndpoints.assignToMe();
        },
        assignToApiUrl() {
            return (
                apiEndpoints.assignTo() +
                `?content_type=${this.burnPlanUnit?.content_type}&object_id=${this.burnPlanUnit?.id}`
            );
        },
    },
    async created() {
        await this.fetchBurnPlanUnit();
        this.fetchAssignableUsers();
    },
    methods: {
        async fetchBurnPlanUnit() {
            var pk = this.$route.params.pk;
            await utils
                .fetchUrl(apiEndpoints.burnPlanningUnits(pk))
                .then((data) => {
                    this.burnPlanUnit = Object.assign({}, data);
                });
        },
        fetchAssignableUsers() {
            utils
                .fetchUrl(
                    apiEndpoints.assignableUsers() +
                        `?content_type=${this.burnPlanUnit.content_type}&object_id=${this.burnPlanUnit.id}`
                )
                .then((data) => {
                    this.assignableUsers = data;
                });
        },
        assignTo(value) {
            this.burnPlanUnit.assigned_to = value;
        },
    },
};
</script>
