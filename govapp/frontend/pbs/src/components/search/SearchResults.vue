<template>
    <SearchResult
        v-for="result in results"
        :key="result.id"
        :result="result"
    ></SearchResult>
</template>

<script>
import SearchResult from './SearchResult.vue';

export default {
    name: 'SearchResults',
    components: {
        SearchResult,
    },
    props: {
        results: {
            type: Array,
            default: () => [],
        },
    },
};
</script>
