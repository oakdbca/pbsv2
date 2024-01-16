<template>
    <div id="bpe" class="container">Burn Plan Elements</div>
    <div class="card text-center">
        <TableSlotTemplate
            name="Burn Plan Elements"
            :headers="[
                'ID',
                'Name',
                'Indicative Treatment Year',
                'Revised Treatment Year',
                'Region',
                'District',
                'Treatment',
                'Status',
                'Action',
            ]"
        >
            <tbody>
                <tr v-for="bpe in burnPlanElements" :key="bpe.id">
                    <td>{{ bpe.id }}</td>
                    <td>{{ bpe.name }}</td>
                    <td>{{ bpe.indicative_treatment_year }}</td>
                    <td>{{ bpe.revised_indicative_treatment_year }}</td>
                    <td>{{ bpe.region }}</td>
                    <td>{{ bpe.district }}</td>
                    <td>{{ bpe.treatment }}</td>
                    <td>{{ bpe.status }}</td>
                    <td>View</td>
                </tr>
            </tbody>
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
    computed: {},
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
