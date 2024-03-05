<template>
    <div class="card mb-3">
        <div class="card-header text-capitalize">
            {{ result.verbose_name }} - {{ result.reference_number }}
            <BadgeStatus
                class="float-end p-2"
                :status="result.status"
                :status-display="result.status_display"
            />
        </div>
        <div class="card-body">
            <h5 class="card-title">{{ result.name }}</h5>
            <a :href="result.link">View Details Page</a>
        </div>
    </div>
</template>

<script>
import BadgeStatus from '@/components/forms/BadgeStatus.vue';

export default {
    name: 'SearchResult',
    components: {
        BadgeStatus,
    },
    props: {
        result: {
            type: Object,
            default: () => {},
        },
    },
};
</script>
