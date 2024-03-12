<template>
    <li
        class="list-group-item d-flex justify-content-between align-items-start"
    >
        <div class="ms-2 me-auto">
            <div class="fw-bold">
                <a :href="item.link">{{ item.reference_number }}</a>
            </div>
            {{ item.name }}
        </div>
        <BadgeStatus
            class="p-2"
            :status="item.status"
            :status-display="item.status_display"
        />
    </li>
</template>

<script>
import BadgeStatus from '@/components/forms/BadgeStatus.vue';

export default {
    name: 'ListItem',
    components: {
        BadgeStatus,
    },
    props: {
        item: {
            type: Object,
            required: true,
        },
    },
};
</script>
