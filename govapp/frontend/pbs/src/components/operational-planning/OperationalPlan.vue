<template>
    <LayoutDetails :loading="!operationalPlan">
        <template #heading>
            <h3>
                Operational Plan:
                <span class="text-secondary">{{
                    operationalPlan.reference_number
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
                :content-type="operationalPlan.content_type"
                :object-id="operationalPlan.id"
            />
            <PanelWorkflow
                :status="operationalPlan.status"
                :status-display="operationalPlan.status_display"
                :content-type="operationalPlan.content_type"
                :pk="operationalPlan.id"
                :assignable-users="assignableUsers"
                :assign-to-me-api-url="assignToMeApiUrl"
                :assign-to-api-url="assignToApiUrl"
                :assigned-to="operationalPlan.assigned_to"
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
        <BootstrapAccordion id="operational-plan-accordion">
            <BootstrapAccordionItem
                heading="Overview One Two"
                icon-class="bi-exclamation-circle-fill"
                icon-color-class="text-warning"
            >
                Overview body
            </BootstrapAccordionItem>
            <BootstrapAccordionItem heading="Priority">
                Priority body
            </BootstrapAccordionItem>
            <BootstrapAccordionItem heading="Context">
                Context body
            </BootstrapAccordionItem>
        </BootstrapAccordion>
    </LayoutDetails>
</template>

<script>
import { useStore } from '@/stores/state';

import { apiEndpoints, utils } from '@/utils/hooks';

import LayoutDetails from '../layout/LayoutDetails.vue';

import BootstrapAccordion from '../forms/BootstrapAccordion.vue';
import BootstrapAccordionItem from '../forms/BootstrapAccordionItem.vue';

import PanelLogs from '../logging/PanelLogs.vue';

export default {
    name: 'OperationalPlan',
    components: {
        LayoutDetails,
        PanelLogs,
        BootstrapAccordion,
        BootstrapAccordionItem,
    },
    data() {
        return {
            store: useStore(),
            operationalPlan: null,
            assignableUsers: null,
        };
    },
    computed: {
        communicationsApiUrl: function () {
            return (
                apiEndpoints.communications() +
                `?format=datatables&content_type=${this.operationalPlan?.content_type}&object_id=${this.operationalPlan?.id}`
            );
        },
        postCommunicationsEntryApiUrl() {
            return apiEndpoints.communications();
        },
        actionsApiUrl: function () {
            return (
                apiEndpoints.actions() +
                `?format=datatables&content_type=${this.operationalPlan?.content_type}&object_id=${this.operationalPlan?.id}`
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
                `?content_type=${this.operationalPlan?.content_type}&object_id=${this.operationalPlan?.id}`
            );
        },
    },
    async created() {
        await this.fetchOperationalPlan();
        this.fetchAssignableUsers();
    },
    methods: {
        async fetchOperationalPlan() {
            var pk = this.$route.params.pk;
            await utils
                .fetchUrl(apiEndpoints.operationalPlans(pk))
                .then((data) => {
                    this.operationalPlan = Object.assign({}, data);
                });
        },
        fetchAssignableUsers() {
            utils
                .fetchUrl(
                    apiEndpoints.assignableUsers() +
                        `?content_type=${this.operationalPlan.content_type}&object_id=${this.operationalPlan.id}`
                )
                .then((data) => {
                    this.assignableUsers = data;
                });
        },
        assignTo(value) {
            this.operationalPlan.assigned_to = value;
        },
    },
};
</script>
