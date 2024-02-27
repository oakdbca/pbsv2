<template>
    <div v-if="operationalPlan" class="container">
        <div class="row">
            <div class="col">
                <h3>
                    Operational Plan:
                    <span class="text-secondary">{{
                        operationalPlan.reference_number
                    }}</span>
                </h3>
            </div>
        </div>
        <div class="row">
            <div class="col-3">
                <PanelLogs
                    :content-type="operationalPlan.content_type"
                    :pk="operationalPlan.id"
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
                    @assign-to-me="assignToMe"
                    @assign-to="assignTo"
                ></PanelWorkflow>
                <div class="card">
                    <div class="card-header">Actions</div>
                    <div class="card-body">
                        <button class="btn btn-primary">Submit</button>
                    </div>
                </div>
            </div>
            <div class="col">
                <div id="operational-plan-accordion" class="accordion">
                    <div class="accordion-item">
                        <h2
                            id="panelsStayOpen-headingOne"
                            class="accordion-header"
                        >
                            <button
                                class="accordion-button collapsed"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#panelsStayOpen-collapseOne"
                                aria-expanded="false"
                                aria-controls="panelsStayOpen-collapseOne"
                            >
                                Overview
                            </button>
                        </h2>
                        <div
                            id="panelsStayOpen-collapseOne"
                            class="accordion-collapse collapse"
                            aria-labelledby="panelsStayOpen-headingOne"
                        >
                            <div class="accordion-body">Overview body</div>
                        </div>
                    </div>
                    <div class="accordion-item">
                        <h2
                            id="panelsStayOpen-headingTwo"
                            class="accordion-header"
                        >
                            <button
                                class="accordion-button collapsed"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#panelsStayOpen-collapseTwo"
                                aria-expanded="false"
                                aria-controls="panelsStayOpen-collapseTwo"
                            >
                                Priority
                            </button>
                        </h2>
                        <div
                            id="panelsStayOpen-collapseTwo"
                            class="accordion-collapse collapse"
                            aria-labelledby="panelsStayOpen-headingTwo"
                        >
                            <div class="accordion-body">Priority body</div>
                        </div>
                    </div>
                    <div class="accordion-item">
                        <h2
                            id="panelsStayOpen-headingThree"
                            class="accordion-header"
                        >
                            <button
                                class="accordion-button collapsed"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#panelsStayOpen-collapseThree"
                                aria-expanded="false"
                                aria-controls="panelsStayOpen-collapseThree"
                            >
                                Context
                            </button>
                        </h2>
                        <div
                            id="panelsStayOpen-collapseThree"
                            class="accordion-collapse collapse"
                            aria-labelledby="panelsStayOpen-headingThree"
                        >
                            <div class="accordion-body">Context Body</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useStore } from '@/stores/state';

import { api_endpoints, utils } from '@/utils/hooks';

import PanelLogs from '../logging/PanelLogs.vue';
import PanelWorkflow from '../workflow/PanelWorkflow.vue';

export default {
    name: 'OperationalPlan',
    components: {
        PanelWorkflow,
        PanelLogs,
    },
    data() {
        return {
            store: useStore(),
            operationalPlan: null,
            assignableUsers: null,
        };
    },
    computed: {
        assignableUsersApiUrl() {
            return api_endpoints.assignableUsers();
        },
        assignToMeApiUrl() {
            return api_endpoints.assignToMe();
        },
        assignToApiUrl() {
            return (
                api_endpoints.assignTo() +
                `?content_type=${this.operationalPlan?.content_type}&object_id=${this.operationalPlan?.pk}`
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
                .fetchUrl(api_endpoints.operationalPlans(pk))
                .then((data) => {
                    this.operationalPlan = Object.assign({}, data);
                });
        },
        fetchAssignableUsers() {
            utils
                .fetchUrl(
                    api_endpoints.assignableUsers() +
                        `?content_type=${this.operationalPlan.content_type}&object_id=${this.operationalPlan.id}`
                )
                .then((data) => {
                    this.assignableUsers = data;
                });
        },
        assignToMe() {},
        assignTo(value) {
            this.operationalPlan.assigned_to = value;
        },
    },
};
</script>
