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
                                <div v-for="idx in readOnlyFields" :key="idx">
                                    <RowInputForm
                                        :key="`bpe-${burnPlanElement.reference_number}-${idx}`"
                                        :idx="idx"
                                        :field="burnPlanElement[idx]"
                                        :disabled="true"
                                        @update:field="
                                            burnPlanElement[idx] = $event
                                        "
                                    ></RowInputForm>
                                </div>
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
import RowInputForm from '@/components/forms/row_input_form.vue';

export default {
    name: 'BurnPlanElement',
    components: { FormSection, RowInputForm },
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
    methods: {},
};
</script>

<style lang="css">
.capitalize {
    text-transform: capitalize;
}
</style>
