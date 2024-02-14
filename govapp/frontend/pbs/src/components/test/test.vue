<template>
    <div id="testvue" class="container">This is a test page!!</div>
</template>

<script>
import { NotImplementedError } from "@/utils/errors";
import { utils, helpers } from "@/utils/hooks";

/**
 * Test URL for testing fetchUrl
 * @constant testUrl
 * @type {string}
 */
const testUrlOk = `https://kmi.dbca.wa.gov.au/geoserver/public/wms/?SERVICE=WMS&VERSION=1.0.0&REQUEST=GetCapabilities`;

export default {
    name: "TestVue",
    components: {},
    data: function () {
        return {};
    },
    computed: {},
    mounted: async function () {
        console.log("test template loaded");
        this.testErrors();
        this.testFetch(testUrlOk);
        this.testFetch("https://fail.to.fetch");
        /**
         * @type {DateStr} date_str
         */
        const date_str = "2021-01-01";
        this.testDate(date_str);
        this.testDate(null);
        this.testDate(undefined);
    },
    methods: {
        testErrors: () => {
            try {
                throw new NotImplementedError(
                    "test.vue: Testing error handling",
                );
            } catch (error) {
                console.log(error);
                console.log(helpers.formatError(error));
            }
        },
        testFetch: (/** @type {string} */ url) => {
            utils
                .fetchUrl(url)
                .then(() => {
                    console.log(`${url} OK`);
                })
                .catch(() => {
                    console.log(`${url} failed`);
                });
        },
        /**
         * @function testDate
         * @param {DateStr} date_str
         */
        testDate: (date_str) => {
            console.log(new Date(date_str));
        },
    },
};
</script>
