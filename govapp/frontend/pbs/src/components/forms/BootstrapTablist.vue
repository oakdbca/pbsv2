<template>
    <div class="card-header">
        <ul
            id="burn-plan-element-tabs"
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
        tabNames: {
            type: Array,
            required: true,
        },
        activeTabIndex: {
            type: Number,
            default: 0,
            validator: (value) => {
                return value >= 0;
            },
        },
    },
    methods: {
        slugifyString(text, options = { lower: true }) {
            return slugify(text, options);
        },
        tabIdentifier(tabName) {
            return `tab-${this.slugifyString(tabName)}`;
        },
    },
};
</script>
