<template>
    <div class="container">
        <div class="row">
            <div class="col">
                <h3 class="text-secondary">
                    Search<span v-if="query"> Results for '{{ query }}'</span>
                </h3>
            </div>
        </div>
        <div class="row">
            <div class="col-3">
                <div class="card">
                    <div class="card-header">Advanced Search</div>
                    <div class="card-body">
                        <h4 class="card-title">Title</h4>
                        <p class="card-text">Text</p>
                    </div>
                </div>
            </div>
            <div class="col-9">
                <div class="container">
                    <div class="row">
                        <div class="col">
                            <h4>Search Results</h4>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ComponentSearch',
    computed: {
        query: function () {
            return this.$route.query.q ? this.$route.query.q : '';
        },
    },
};
</script>

<style lang="scss" scoped></style>
