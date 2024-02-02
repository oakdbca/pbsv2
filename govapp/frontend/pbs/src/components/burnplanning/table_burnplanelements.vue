<template>
    <div id="bpe" class="container">Burn Plan Elements</div>
    <div class="card text-center">
        <TableSlotTemplate
            name="Burn Plan Elements"
            :queryset="queryset"
            :properties="properties"
        >
            <!-- Additional table headers -->
            <template #table_headers>
                <th>Action</th>
            </template>
            <!-- Additional table data cells -->
            <template #table_rows>
                <td><a href="#" @click="clickFunction($event)">View</a></td>
            </template>
        </TableSlotTemplate>
    </div>
</template>

<script>
import { utils, api_endpoints } from '@/utils/hooks';
import TableSlotTemplate from '@/components/forms/colocation/table_slot_template.vue';

export default {
    name: 'TableBurnPlanElements',
    components: { TableSlotTemplate },
    props: {},
    data: function () {
        return {
            burnPlanElements: [],
        };
    },
    computed: {
        queryset: function () {
            return this.burnPlanElements;
        },
        properties: function () {
            return [
                'id',
                'name',
                'indicative_treatment_year',
                'revised_indicative_treatment_year',
                'region',
                'district',
                'treatment',
                'status',
            ];
        },
    },
    mounted: async function () {
        console.info(`${this.$options?.name} template loaded`);

        utils
            .fetchUrl(api_endpoints.burn_plan_elements())
            .then((data) => {
                this.burnPlanElements = Object.assign({}, data.results);
                console.info(
                    `BPEs fetched ${JSON.stringify(this.burnPlanElements)}`
                );
            })
            .catch((error) => {
                console.error(`BPEs fetch failed with ${error}`);
            });
    },
    methods: {
        clickFunction: function (/** @type {any} */ event) {
            const id = $(event.target).closest('tr')[0].children[0].textContent;
            window.open(`burn-plan-elements/${id}`, '_blank');
        },
    },
};
</script>
