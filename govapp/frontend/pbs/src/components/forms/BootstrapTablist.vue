<template>
    <div class="card-header">
        <ul
            :id="`${slugifyString(parentComponentNameSlugified)}-tablist`"
            class="nav nav-tabs card-header-tabs"
            role="tablist"
        >
            <li
                v-for="(tabName, index) in tabNames"
                :key="`${tabIdentifier(tabName)}-${index}`"
                class="nav-item"
            >
                <a
                    :class="
                        index === activeTabIndex
                            ? 'nav-link active'
                            : 'nav-link'
                    "
                    :href="`#${tabIdentifier(tabName)}`"
                    data-bs-toggle="pill"
                    role="tab"
                    :tabindex="index"
                    :aria-current="index === activeTabIndex ? 'true' : 'false'"
                    :aria-selected="index === activeTabIndex ? 'true' : 'false'"
                    @click="onTabClicked($event, index)"
                    >{{ tabName }}</a
                >
            </li>
        </ul>
    </div>

    <div class="card-body">
        <div class="tab-content mt-3">
            <div
                v-for="(tabName, index) in tabNames"
                :id="`${tabIdentifier(tabName)}`"
                :key="`${tabIdentifier(tabName)}-${index}`"
                :class="
                    index === activeTabIndex ? 'tab-pane active' : 'tab-pane'
                "
                role="tabpanel"
            >
                <slot :name="`tab-${slugifyString(tabName)}`">
                    {{ `Use '<template #tab-${slugifyString(tabName)}
                        >Your content</template
                    >' to slot in your content for the ${tabName} tab.` }}</slot
                >
            </div>
        </div>
    </div>
</template>

<script>
var slugify = require('slugify');

export default {
    name: 'BootstrapTablist',
    props: {
        /**
         * An array of tab names
         */
        tabNames: {
            type: Array,
            required: true,
        },
        /**
         * The index of the active tab when the component is created
         */
        activeTabIndex: {
            type: Number,
            default: 0,
            validator: (value, props) => {
                if (parseInt(value) !== value) {
                    return false;
                }
                return value >= 0 && value < props.tabNames.length;
            },
        },
    },
    emits: ['activeTabIndexChanged'],
    data: function () {
        return {
            activeTabIndexInternal: this.activeTabIndex,
        };
    },
    computed: {
        parentComponentNameSlugified() {
            return this.unPascalCaseString(this.$parent.$options.name);
        },
    },
    created() {
        console.log(`${this.$options.name} created`);
    },
    methods: {
        slugifyString(
            text,
            options = { lower: true, remove: /[*+~.()'"!:@]/g }
        ) {
            return slugify(text, options);
        },
        /**
         * Replaces occurrences of xY in a string with x Y
         * @param {String} text A string in PascalCase
         */
        unPascalCaseString(text) {
            return text.replace(/([^A-Z])([A-Z])/g, '$1 $2');
        },
        tabIdentifier(tabName) {
            return `tab-${this.slugifyString(tabName)}`;
        },
        /**
         * Sets the active tab index to the index of the tab that was clicked and
         * emits the activeTabIndexChanged event to the parent component when the active tab is changed
         * @param {Object} event The click event
         * @param {*} index The index of the tab that was clicked
         */
        onTabClicked(event, index) {
            if (index != this.activeTabIndexInternal) {
                this.activeTabIndexInternal = index;
                this.$emit('activeTabIndexChanged', index);
            }
        },
    },
};
</script>
