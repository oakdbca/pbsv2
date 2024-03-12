<template>
    <div v-if="burnPlanElement" id="bpe" class="container">
        {{ burnPlanElement }}
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
                                <div v-if="burnPlanElement" class="container">
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
                                                burnPlanElement[name] = $event
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

                                    <RowSlotTemplate name="Preferred Season">
                                        <SelectFilter
                                            :id="selectFilterId('season')"
                                            title="Preferred Season"
                                            :options="
                                                burnPlanElement.filter_options
                                                    .season
                                            "
                                            :pre-selected-filter-item="
                                                burnPlanElement.preferred_season
                                            "
                                            :show-title="false"
                                            @selection-changed-select="
                                                selectionChanged(
                                                    $event,
                                                    'preferred_season'
                                                )
                                            "
                                            @selection-changed-remove="
                                                console.log($event)
                                            "
                                        >
                                        </SelectFilter>
                                    </RowSlotTemplate>

                                    <RowSlotTemplate name="Treatment">
                                        <SelectFilter
                                            :id="selectFilterId('treatment')"
                                            title="Treatment"
                                            :options="
                                                burnPlanElement.filter_options
                                                    .treatment
                                            "
                                            :pre-selected-filter-item="
                                                burnPlanElement.treatment_id
                                            "
                                            :show-title="false"
                                            placeholder="No treatment"
                                            @selection-changed-select="
                                                selectionChanged(
                                                    $event,
                                                    'treatment_id',
                                                    'treatment'
                                                )
                                            "
                                            @selection-changed-remove="
                                                console.log($event)
                                            "
                                        >
                                        </SelectFilter>
                                    </RowSlotTemplate>

                                    <RowSlotTemplate name="Justification">
                                        <SelectFilter
                                            :id="
                                                selectFilterId('justification')
                                            "
                                            title="Justification"
                                            :options="
                                                burnPlanElement.filter_options
                                                    .justification
                                            "
                                            :pre-selected-filter-item="
                                                burnPlanElement.justification_id
                                            "
                                            :show-title="false"
                                            @selection-changed-select="
                                                selectionChanged(
                                                    $event,
                                                    'justification_id',
                                                    'justification'
                                                )
                                            "
                                            @selection-changed-remove="
                                                console.log($event)
                                            "
                                        >
                                        </SelectFilter>
                                    </RowSlotTemplate>

                                    <RowSlotTemplate name="Purpose">
                                        <SelectFilter
                                            :id="selectFilterId('purpose')"
                                            title="Purpose"
                                            :options="
                                                burnPlanElement.filter_options
                                                    .purpose
                                            "
                                            :pre-selected-filter-item="
                                                selectedPurposes
                                            "
                                            :show-title="false"
                                            @selection-changed-select="
                                                selectionChanged(
                                                    $event,
                                                    'purpose'
                                                )
                                            "
                                            @selection-changed-remove="
                                                console.log($event)
                                            "
                                        >
                                        </SelectFilter>
                                    </RowSlotTemplate>

                                    <RowSlotTemplate name="Program">
                                        <SelectFilter
                                            :id="selectFilterId('program')"
                                            title="Program"
                                            :options="
                                                burnPlanElement.filter_options
                                                    .program
                                            "
                                            :pre-selected-filter-item="
                                                selectedPurposes
                                            "
                                            :show-title="false"
                                            @selection-changed-select="
                                                selectionChanged(
                                                    $event,
                                                    'program'
                                                )
                                            "
                                            @selection-changed-remove="
                                                console.log($event)
                                            "
                                        >
                                        </SelectFilter>
                                    </RowSlotTemplate>

                                    <RowTextareaComponent
                                        :key="keyRowComponent('comments')"
                                        name="comments"
                                        :value="burnPlanElement['comments']"
                                        @update:value="
                                            burnPlanElement['comments'] = $event
                                        "
                                    ></RowTextareaComponent>
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

import { useUserStore } from '@/stores/user';

import PanelLogs from '../logging/PanelLogs.vue';

import RowInputComponent from '@/components/forms/colocation/RowInput.vue';
import RowTextareaComponent from '@/components/forms/colocation/RowTextarea.vue';
import RowSlotTemplate from '@/components/forms/colocation/RowSlotTemplate.vue';

import BootstrapTablist from '@/components/forms/BootstrapTablist.vue';
import BootstrapAccordion from '../forms/BootstrapAccordion.vue';
import BootstrapAccordionItem from '../forms/BootstrapAccordionItem.vue';

import SelectFilter from '@/components/forms/colocation/SelectFilter.vue';

export default {
    name: 'BurnPlanElement',
    components: {
        RowInputComponent,
        RowTextareaComponent,
        PanelLogs,
        BootstrapTablist,
        BootstrapAccordion,
        BootstrapAccordionItem,
        SelectFilter,
        RowSlotTemplate,
    },
    props: {},
    data: function () {
        return {
            store: useUserStore(),
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
                this.burnPlanElement['treatment'] === null
            );
        },

        selectedPurposes: function () {
            return this.burnPlanElement.purposes.map((purpose) => {
                return { value: purpose.id, text: purpose.name };
            });
        },
        selectedPrograms: function () {
            return this.burnPlanElement.programs.map((program) => {
                return { value: program.id, text: program.name };
            });
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
        selectFilterId(filterName) {
            const ct = this.burnPlanElement.content_type;
            const id = this.burnPlanElement.id;
            return `select-filter--content-type-${ct}-id-${id}-name-${filterName}`;
        },
        selectionChanged(selected, idField, textField = null) {
            if (Object.hasOwn(this.burnPlanElement, idField)) {
                this.burnPlanElement[idField] = selected.value.value;
            } else {
                console.error(
                    `selectionChanged: ${idField} not found in burnPlanElement`
                );
            }
            if (textField !== null) {
                if (Object.hasOwn(this.burnPlanElement, textField)) {
                    this.burnPlanElement[textField] = selected.value.text;
                } else {
                    console.error(
                        `selectionChanged: ${textField} not found in burnPlanElement`
                    );
                }
            }
        },
    },
};
</script>

<style lang="css">
.capitalize {
    text-transform: capitalize;
}
</style>
