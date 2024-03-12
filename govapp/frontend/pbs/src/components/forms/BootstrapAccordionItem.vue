<template>
    <div class="accordion-item">
        <h2 :id="`heading${slugifiedHeading}`" class="accordion-header">
            <button
                class="accordion-button"
                :class="[
                    collapsed ? 'collapsed' : '',
                    iconColorClass ? iconColorClass : '',
                ]"
                type="button"
                data-bs-toggle="collapse"
                :data-bs-target="`#collapse${slugifiedHeading}`"
                :aria-expanded="collapsed ? 'false' : 'true'"
                :aria-controls="`collapse${slugifiedHeading}`"
                @click="toggleCollapsed"
            >
                {{ heading }}
                <div class="ms-auto">
                    <i
                        v-if="iconClass"
                        class="accordion-item-icon bi fs-5"
                        :class="[iconClass, iconColorClass]"
                    ></i>
                </div>
            </button>
        </h2>
        <div
            :id="`collapse${slugifiedHeading}`"
            class="accordion-collapse collapse"
            :class="{ show: !collapsed }"
            :aria-labelledby="`heading${slugifiedHeading}`"
        >
            <div class="accordion-body">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<script>
import { useAccordionStore } from '@/stores/accordions';

var slugify = require('slugify');

export default {
    name: 'BootstrapAccordionItem',
    props: {
        id: {
            // Unique id for the accordion item
            // If it's not present then the state of the accordion item will not be persisted
            type: String,
            default: null,
        },
        heading: {
            type: String,
            required: true,
        },
        iconClass: {
            type: String,
            default: '',
        },
        iconColorClass: {
            type: String,
            default: '',
        },
    },
    data: () => ({
        collapsed: true,
        store: useAccordionStore(),
    }),
    computed: {
        slugifiedHeading() {
            return this.id ? this.id : slugify(this.heading, { lower: true });
        },
    },
    created() {
        if (this.id && this.id in this.store.accordionData) {
            this.collapsed = this.store.accordionData[this.id];
        }
    },
    methods: {
        toggleCollapsed() {
            this.collapsed = !this.collapsed;
            if (this.id) {
                this.store.accordionData[this.id] = this.collapsed;
            }
        },
    },
};
</script>
<style scoped lang="css">
.accordion-button::after {
    margin-left: 1em;
}
</style>
