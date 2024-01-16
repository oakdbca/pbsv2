<template>
    <div id="bpe" class="container">Burn Plan Elements</div>
    <div class="card text-center">
        <TableSlotTemplate
            name="Burn Plan Elements"
            :queryset="queryset"
            :properties="properties"
        >
            <!-- Additional table columns -->
            <template #table_headers>
                <th>Action</th>
            </template>
            <template #table_rows>
                <td>View</td>
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
        console.log(`${this.$options?.name} template loaded`);

        utils
            .fetchUrl(api_endpoints.burn_plan_elements())
            .then((data) => {
                this.burnPlanElements = Object.assign({}, data.results);
                console.log(
                    `BPE fetched ${JSON.stringify(this.burnPlanElements)}`
                );
            })
            .catch((error) => {
                console.error(`BPE fetch failed with ${error}`);
            });
    },
    methods: {},
};
</script>
