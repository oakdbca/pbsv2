<template>
    <LayoutDetails :loading="loading">
        <template #heading>
            <h3 class="text-secondary">
                <template v-if="query">
                    Your Search for '<em>{{ query }}</em
                    >' returned {{ results.length }} result<template
                        v-if="results.length != 1"
                        >s</template
                    >
                </template>
                <template v-else>Search</template>
            </h3>
        </template>
        <template #left-menu>
            <div class="card">
                <div class="card-header">Advanced Search</div>
                <div class="card-body border-bottom">
                    <form method="GET" action="/search">
                        <p class="card-text">
                            <input
                                v-model="query"
                                class="form-control"
                                type="search"
                                name="q"
                                autofocus
                            />
                        </p>
                    </form>
                </div>
                <div class="card-body">TODO: Add advanced search options</div>
            </div>
        </template>
        <div class="container">
            <div class="row">
                <div class="col">
                    <SearchResults :results="results"></SearchResults>
                </div>
            </div>
        </div>
    </LayoutDetails>
</template>

<script>
import { utils, apiEndpoints } from '@/utils/hooks';

import LayoutDetails from '../layout/LayoutDetails.vue';

import SearchResults from './SearchResults.vue';

export default {
    name: 'ComponentSearch',
    components: {
        LayoutDetails,
        SearchResults,
    },
    data: function () {
        return {
            loading: true,
            results: [],
        };
    },
    computed: {
        query: function () {
            return this.$route.query.q ? this.$route.query.q : '';
        },
    },
    created: async function () {
        if (this.query) {
            await this.search();
        }
        this.loading = false;
    },
    methods: {
        search: async function () {
            await utils
                .fetchUrl(apiEndpoints.search(this.query))
                .then((data) => {
                    this.results = data;
                });
        },
    },
};
</script>
