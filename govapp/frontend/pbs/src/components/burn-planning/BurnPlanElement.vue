<template>
    <div v-if="burnPlanElement" id="bpe" class="container">
        <div class="row">
            <div class="col">
                <h3>
                    Burn Plan Element:
                    <span class="text-secondary">{{
                        burnPlanElement.reference_number
                    }}</span>
                </h3>
            </div>
        </div>
        <div class="row">
            <div class="col-3">
                <PanelLogs
                    :communications-api-url="communicationsApiUrl"
                    :post-communications-entry-api-url="
                        postCommunicationsEntryApiUrl
                    "
                    :actions-api-url="actionsApiUrl"
                    :content-type="burnPlanElement.content_type"
                    :object-id="burnPlanElement.id"
                />
                <PanelWorkflow
                    :status="burnPlanElement.status"
                    :status-display="burnPlanElement.status_display"
                    :content-type="burnPlanElement.content_type"
                    :pk="burnPlanElement.id"
                    :assignable-users="assignableUsers"
                    :assign-to-me-api-url="assignToMeApiUrl"
                    :assign-to-api-url="assignToApiUrl"
                    :assigned-to="burnPlanElement.assigned_to"
                    :request-user-id="store.userData.id"
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
                <BootstrapTablist
                    :tab-names="[
                        'Plan',
                        'Operational Area(s)',
                        'Related Items',
                    ]"
                    :active-tab-index="0"
                    :spinner-on-tabs-by-index="[]"
                    @active-tab-index-changed="activeTabIndexChanged"
                >
                    <template #tab-plan>
                        <BootstrapAccordion
                            id="burn-plan-element-accordion"
                            title=""
                            content=""
                        >
                            <BootstrapAccordionItem heading="Details">
                                <div class="container">
                                    <div v-if="burnPlanElement">
                                        <!-- Non-editable fields -->
                                        <div
                                            v-for="name in readOnlyFields"
                                            :key="name"
                                        >
                                            <RowInputComponent
                                                :key="keyRowComponent(name)"
                                                :name="name"
                                                :value="burnPlanElement[name]"
                                                :disabled="true"
                                                @update:value="
                                                    burnPlanElement[name] =
                                                        $event
                                                "
                                            ></RowInputComponent>
                                        </div>
                                        <!-- Editable fields -->
                                        <RowInputComponent
                                            v-if="
                                                showRevisedIndicativeTreatmentYear
                                            "
                                            :key="
                                                keyRowComponent(
                                                    'revised_indicative_treatment_year'
                                                )
                                            "
                                            name="revised_indicative_treatment_year"
                                            :value="
                                                burnPlanElement[
                                                    'revised_indicative_treatment_year'
                                                ]
                                            "
                                            :disabled="false"
                                            :pattern="'[0-9]{4}'"
                                            :required="
                                                showRevisedIndicativeTreatmentYear
                                            "
                                            @update:value="
                                                burnPlanElement[
                                                    'revised_indicative_treatment_year'
                                                ] = $event
                                            "
                                        ></RowInputComponent>
                                        <RowInputComponent
                                            :key="
                                                keyRowComponent(
                                                    'return_interval'
                                                )
                                            "
                                            name="return_interval (years)"
                                            :value="
                                                burnPlanElement[
                                                    'return_interval'
                                                ]
                                            "
                                            :disabled="false"
                                            :pattern="'[0-9]{2}'"
                                            @update:value="
                                                burnPlanElement[
                                                    'return_interval'
                                                ] = $event
                                            "
                                        ></RowInputComponent>

                                        <RowSelectComponent
                                            :key="
                                                keyRowComponent(
                                                    'preferred_season'
                                                )
                                            "
                                            name="preferred_season"
                                            :selection="preferredSeasons"
                                            :selected-value="
                                                burnPlanElement[
                                                    'preferred_season'
                                                ]
                                            "
                                            :disabled="false"
                                            @update:value="
                                                burnPlanElement[
                                                    'preferred_season'
                                                ] = $event
                                            "
                                        ></RowSelectComponent>

                                        <RowRadiosComponent
                                            :key="keyRowComponent('treatment')"
                                            name="treatment"
                                            :selection="treatments"
                                            :selected-value="
                                                burnPlanElement['treatment'] ==
                                                null
                                                    ? noTreatment
                                                    : burnPlanElement[
                                                          'treatment'
                                                      ]
                                            "
                                            :disabled="false"
                                            @update:value="
                                                $event === noTreatment
                                                    ? (burnPlanElement[
                                                          'treatment'
                                                      ] = null)
                                                    : (burnPlanElement[
                                                          'treatment'
                                                      ] = $event)
                                            "
                                        ></RowRadiosComponent>

                                        <RowSelectComponent
                                            :key="
                                                keyRowComponent('justification')
                                            "
                                            name="justification"
                                            :selection="justifications"
                                            :selected-value="
                                                burnPlanElement['justification']
                                            "
                                            :disabled="false"
                                            @update:value="
                                                burnPlanElement[
                                                    'justification'
                                                ] = $event
                                            "
                                        ></RowSelectComponent>
                                        <RowSelectComponent
                                            :key="keyRowComponent('purpose')"
                                            name="purpose"
                                            :selection="purposes"
                                            :selected-value="
                                                burnPlanElement['purpose']
                                            "
                                            :disabled="false"
                                            @update:value="
                                                burnPlanElement['purpose'] =
                                                    $event
                                            "
                                        ></RowSelectComponent>
                                        <RowSelectComponent
                                            :key="keyRowComponent('program')"
                                            name="program"
                                            :selection="programs"
                                            :selected-value="
                                                burnPlanElement['program']
                                            "
                                            :disabled="false"
                                            @update:value="
                                                burnPlanElement['program'] =
                                                    $event
                                            "
                                        ></RowSelectComponent>

                                        <RowTextareaComponent
                                            :key="keyRowComponent('comments')"
                                            name="comments"
                                            :value="burnPlanElement['comments']"
                                            @update:value="
                                                burnPlanElement['comments'] =
                                                    $event
                                            "
                                        ></RowTextareaComponent>
                                    </div>
                                </div>
                            </BootstrapAccordionItem>
                            <BootstrapAccordionItem heading="Output Leaders">
                                Output Leaders body
                            </BootstrapAccordionItem>
                            <BootstrapAccordionItem heading="Documents">
                                Documents body
                            </BootstrapAccordionItem>
                        </BootstrapAccordion>
                    </template>
                    <template #tab-operational-areas>Tab 2 content</template>
                    <template #tab-related-items></template>
                </BootstrapTablist>
            </div>
        </div>
    </div>
</template>

<script>
import { utils, apiEndpoints } from '@/utils/hooks';

import { useStore } from '@/stores/state';

import PanelLogs from '../logging/PanelLogs.vue';

import RowInputComponent from '@/components/forms/colocation/RowInput.vue';
import RowSelectComponent from '@/components/forms/colocation/RowSelect.vue';
import RowRadiosComponent from '@/components/forms/colocation/RowRadios.vue';
import RowTextareaComponent from '@/components/forms/colocation/RowTextarea.vue';

import BootstrapTablist from '@/components/forms/BootstrapTablist.vue';
import BootstrapAccordion from '../forms/BootstrapAccordion.vue';
import BootstrapAccordionItem from '../forms/BootstrapAccordionItem.vue';

export default {
    name: 'BurnPlanElement',
    components: {
        RowInputComponent,
        RowSelectComponent,
        RowRadiosComponent,
        RowTextareaComponent,
        PanelLogs,
        BootstrapTablist,
        BootstrapAccordion,
        BootstrapAccordionItem,
    },
    props: {},
    data: function () {
        return {
            store: useStore(),
            burnPlanElement: null,
            assignableUsers: null,
            noTreatment: 'no_treatment',
            tabContentLoaded: false,
        };
    },
    computed: {
        readOnlyFields: () => {
            return [
                'name',
                'year',
                'reference_number',
                'last_relevant_treatment_year',
                'indicative_treatment_year',
            ];
        },
        showRevisedIndicativeTreatmentYear: function () {
            return (
                this.burnPlanElement['year'] ==
                    this.burnPlanElement['indicative_treatment_year'] &&
                this.burnPlanElement['treatment'] === this.noTreatment
            );
        },
        preferredSeasons: () => {
            return ['spring', 'summer', 'autumn', 'winter'];
        },
        treatments: function () {
            return ['burn', 'mechanical', 'both', this.noTreatment];
        },
        justifications: () => {
            return ['a', 'b', 'c', 'd'];
        },
        purposes: () => {
            return ['a', 'b', 'c', 'd'];
        },
        programs: () => {
            return ['a', 'b', 'c', 'd'];
        },

        communicationsApiUrl: function () {
            return (
                apiEndpoints.communications() +
                `?format=datatables&content_type=${this.burnPlanElement?.content_type}&object_id=${this.burnPlanElement?.id}`
            );
        },
        postCommunicationsEntryApiUrl() {
            return apiEndpoints.communications();
        },
        actionsApiUrl: function () {
            return (
                apiEndpoints.actions() +
                `?format=datatables&content_type=${this.burnPlanElement?.content_type}&object_id=${this.burnPlanElement?.id}`
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
                `?content_type=${this.burnPlanElement?.content_type}&object_id=${this.burnPlanElement?.id}`
            );
        },
    },
    mounted: async function () {
        const id = this.$route.params.pk;

        utils
            .fetchUrl(apiEndpoints.burnPlanElements(id))
            .then((data) => {
                this.burnPlanElement = Object.assign({}, data);
                console.info(
                    `BPE fetched ${JSON.stringify(this.burnPlanElement)}`
                );
            })
            .catch((error) => {
                console.error(`BPE fetch failed with ${error}`);
            });
    },
    methods: {
        keyRowComponent: function (/** @type {String} */ key) {
            return `bpe-${this.burnPlanElement.reference_number}-${key}`;
        },
        assignTo(value) {
            this.operationalPlan.assigned_to = value;
        },
        activeTabIndexChanged(index) {
            console.log(`activeTabIndexChanged ${index}`);
        },
    },
};
</script>

<style lang="css">
.capitalize {
    text-transform: capitalize;
}
</style>
