<template>
    <div class="accordion">
        <slot></slot>
    </div>
</template>

<script>
export default {
    name: 'BootstrapAccordion',
    props: {
        title: {
            type: String,
            required: true,
        },
        content: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            show: false,
        };
    },
    computed: {
        accordionClass() {
            return {
                'accordion-item': true,
                show: this.show,
            };
        },
    },
    methods: {
        toggle() {
            this.show = !this.show;
        },
    },
};
</script>
