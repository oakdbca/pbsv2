<template>
    <ol class="list-group">
        <ListItem v-for="item in items" :key="item.id" :item="item" />
    </ol>
</template>

<script>
import ListItem from '@/components/accounts/Item.vue';

export default {
    name: 'ItemList',
    components: {
        ListItem,
    },
    props: {
        items: {
            type: Array,
            required: true,
        },
    },
};
</script>
