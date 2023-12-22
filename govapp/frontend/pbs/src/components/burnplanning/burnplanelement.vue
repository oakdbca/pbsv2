<template>
    <div id="bpe" class="container">Burn Plan Element</div>
    <div class="card text-center">
        <div class="card-header">
            <ul
                id="burn-plan-element-tabs"
                class="nav nav-tabs card-header-tabs"
                role="tablist"
            >
                <li class="nav-item">
                    <a
                        class="nav-link active"
                        href="#tab-plan"
                        data-bs-toggle="pill"
                        role="tab"
                        tabindex="1"
                        aria-current="true"
                        aria-selected="true"
                        >Plan</a
                    >
                </li>
                <li class="nav-item">
                    <a
                        class="nav-link"
                        href="#tab-operational-areas"
                        data-bs-toggle="pill"
                        role="tab"
                        tabindex="2"
                        aria-selected="false"
                        >Operational Area(s)</a
                    >
                </li>
                <li class="nav-item">
                    <a
                        class="nav-link"
                        href="#tab-related-items"
                        data-bs-toggle="pill"
                        role="tab"
                        tabindex="3"
                        aria-selected="false"
                        >Related Items</a
                    >
                </li>
            </ul>
        </div>

        <div class="card-body">
            <div class="tab-content mt-3">
                <div id="tab-plan" class="tab-pane active" role="tabpanel">
                    {{ burnPlanElement }}
                    <FormSection
                        id="bpe-plan-details"
                        label="Details"
                        index="1"
                        :form-collapse="false"
                    >
                        <!-- revised_indicative_treatment_year
                        return_interval
                        preferred_season
                        treatment
                        justification
                        purpose
                        program
                        comments -->
                        <div class="container">
                            <div v-if="Object.keys(burnPlanElement).length > 0">
                                <!-- Non-editable fields -->
                                <div v-for="name in readOnlyFields" :key="name">
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
                                    @update:value="
                                        burnPlanElement[
                                            'revised_indicative_treatment_year'
                                        ] = $event
                                    "
                                ></RowInputComponent>
                                <RowInputComponent
                                    :key="keyRowComponent('return_interval')"
                                    name="return_interval (years)"
                                    :value="burnPlanElement['return_interval']"
                                    :disabled="false"
                                    :pattern="'[0-9]{2}'"
                                    @update:value="
                                        burnPlanElement['return_interval'] =
                                            $event
                                    "
                                ></RowInputComponent>

                                <RowSelectComponent
                                    :key="keyRowComponent('preferred_season')"
                                    name="preferred_season"
                                    :selection="preferredSeasons"
                                    :selected-value="
                                        burnPlanElement['preferred_season']
                                    "
                                    :disabled="false"
                                    @update:value="
                                        burnPlanElement['preferred_season'] =
                                            $event
                                    "
                                ></RowSelectComponent>

                                <RowRadiosComponent
                                    :key="keyRowComponent('treatment')"
                                    name="treatment"
                                    :selection="treatments"
                                    :selected-value="
                                        burnPlanElement['treatment']
                                    "
                                    :disabled="false"
                                    @update:value="
                                        burnPlanElement['treatment'] = $event
                                    "
                                ></RowRadiosComponent>

                                <RowSelectComponent
                                    :key="keyRowComponent('justification')"
                                    name="justification"
                                    :selection="justifications"
                                    :selected-value="
                                        burnPlanElement['justification']
                                    "
                                    :disabled="false"
                                    @update:value="
                                        burnPlanElement['justification'] =
                                            $event
                                    "
                                ></RowSelectComponent>
                                <RowSelectComponent
                                    :key="keyRowComponent('purpose')"
                                    name="purpose"
                                    :selection="purposes"
                                    :selected-value="burnPlanElement['purpose']"
                                    :disabled="false"
                                    @update:value="
                                        burnPlanElement['purpose'] = $event
                                    "
                                ></RowSelectComponent>
                                <RowSelectComponent
                                    :key="keyRowComponent('program')"
                                    name="program"
                                    :selection="programs"
                                    :selected-value="burnPlanElement['program']"
                                    :disabled="false"
                                    @update:value="
                                        burnPlanElement['program'] = $event
                                    "
                                ></RowSelectComponent>
                            </div>
                        </div>
                    </FormSection>
                    <FormSection
                        id="bpe-plan-output-leaders"
                        label="Output Leaders"
                        index="2"
                        :form-collapse="true"
                    ></FormSection>
                    <FormSection
                        id="bpe-plan-documents"
                        label="Documents"
                        index="3"
                        :form-collapse="true"
                    ></FormSection>
                </div>
                <div
                    id="tab-operational-areas"
                    class="tab-pane"
                    role="tabpanel"
                >
                    <p class="card-text">TODO: Operational Areas</p>
                </div>
                <div id="tab-related-items" class="tab-pane" role="tabpanel">
                    <p class="card-text">TODO: Related Items</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { utils, api_endpoints } from '@/utils/hooks';
import FormSection from '@/components/forms/section_toggle.vue';
import RowInputComponent from '@/components/forms/colocation/row_input.vue';
import RowSelectComponent from '@/components/forms/colocation/row_select.vue';
import RowRadiosComponent from '@/components/forms/colocation/row_radios.vue';

export default {
    name: 'BurnPlanElement',
    components: {
        FormSection,
        RowInputComponent,
        RowSelectComponent,
        RowRadiosComponent,
    },
    props: {
        burnPlanElementId: {
            type: Number,
            required: true,
        },
    },
    data: function () {
        return {
            burnPlanElement: {},
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
        preferredSeasons: () => {
            return ['spring', 'summer', 'autumn', 'winter'];
        },
        treatments: () => {
            return ['burn', 'mechanical', 'both', 'no_treatment'];
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
    },
    mounted: async function () {
        console.log('BPE template loaded');

        utils
            .fetchUrl(api_endpoints.burn_plan_element(this.burnPlanElementId))
            .then((data) => {
                this.burnPlanElement = Object.assign({}, data.results[0]);
                console.log(
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
    },
};
</script>

<style lang="css">
.capitalize {
    text-transform: capitalize;
}
</style>
