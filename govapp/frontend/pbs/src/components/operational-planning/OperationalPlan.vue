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
                    :pk="1"
                />
                <div class="card mb-3">
                    <div class="card-header">Workflow</div>
                    <div class="card-body border-bottom">
                        <div class="input-group">
                            <span id="basic-addon1" class="input-group-text"
                                >Status</span
                            >
                            <input
                                v-model="operationalPlan.status"
                                type="text"
                                class="form-control"
                                placeholder="Username"
                                aria-label="Username"
                                aria-describedby="basic-addon1"
                                disabled
                            />
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <label for="assigned-to" class="form-label"
                                >Assigned To</label
                            >
                            <select id="assigned-to" class="form-select">
                                <option>Someone Else</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <button
                                type="button"
                                class="btn btn-primary float-end"
                            >
                                Assign to me
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="16"
                                    height="16"
                                    fill="currentColor"
                                    class="bi bi-person-raised-hand"
                                    viewBox="0 0 16 16"
                                >
                                    <path
                                        d="M6 6.207v9.043a.75.75 0 0 0 1.5 0V10.5a.5.5 0 0 1 1 0v4.75a.75.75 0 0 0 1.5 0v-8.5a.25.25 0 1 1 .5 0v2.5a.75.75 0 0 0 1.5 0V6.5a3 3 0 0 0-3-3H6.236a1 1 0 0 1-.447-.106l-.33-.165A.83.83 0 0 1 5 2.488V.75a.75.75 0 0 0-1.5 0v2.083c0 .715.404 1.37 1.044 1.689L5.5 5c.32.32.5.754.5 1.207"
                                    />
                                    <path
                                        d="M8 3a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3"
                                    />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
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
import { api_endpoints, utils } from '@/utils/hooks';
import PanelLogs from '@/components/logging/PanelLogs.vue';
export default {
    name: 'OperationalPlan',
    components: {
        PanelLogs,
    },
    data() {
        return {
            operationalPlan: null,
        };
    },
    created() {
        this.fetchOperationalPlan();
    },
    methods: {
        fetchOperationalPlan() {
            var pk = this.$route.params.pk;
            utils.fetchUrl(api_endpoints.operationalPlans(pk)).then((data) => {
                this.operationalPlan = Object.assign({}, data);
            });
        },
    },
};
</script>
