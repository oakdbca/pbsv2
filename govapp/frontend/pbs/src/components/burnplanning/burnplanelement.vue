<template>
    <div id="bpe" class="container">Burn Plan Element</div>
    <div class="card text-center">
        <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs">
                <li class="nav-item">
                    <a
                        class="nav-link active"
                        tabindex="1"
                        aria-current="true"
                        href="#"
                        >Plan</a
                    >
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#" tabindex="2">Tab</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#" tabindex="3">Disabled tab</a>
                </li>
            </ul>
        </div>
        <div class="card-body">
            <h4 class="card-title">Title</h4>
            <p class="card-text">Body</p>
        </div>
    </div>
</template>

<script>
import { utils, api_endpoints /**, helpers */ } from '@/utils/hooks';

export default {
    name: 'BurnPlanElement',
    components: {},
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
    computed: {},
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
