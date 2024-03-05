<template>
    <div class="card">
        <div class="card-header">{{ result.reference_number }}</div>
        <div class="card-body">
            <h5 class="card-title">Special title treatment</h5>
            <p class="card-text">
                With supporting text below as a natural lead-in to additional
                content.
            </p>
            <a :href="result.link" class="btn btn-primary">View Details Page</a>
        </div>
    </div>
</template>

<script>
export default {
    name: 'SearchResult',
    props: {
        result: {
            type: Object,
            default: () => {},
        },
    },
};
</script>
