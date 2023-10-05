<template>
    <div id="testvue" class="container">This is a test page!!</div>
</template>

<script>
import { NotImplementedError } from '@/utils/errors';
import { utils, helpers } from '@/utils/hooks';

/**
 * @constant {string} testUrl - Test URL for testing fetchUrl
 */
const testUrlOk = `https://kmi.dbca.wa.gov.au/geoserver/public/wms/?SERVICE=WMS&VERSION=1.0.0&REQUEST=GetCapabilities`;

export default {
    name: 'TestVue',
    components: {},
    data: function () {
        return {};
    },
    computed: {},
    mounted: async function () {
        console.log('test template loaded');
        this.testErrors();
        this.testFetch(testUrlOk);
        this.testFetch('https://fail.to.fetch');
    },
    methods: {
        testErrors: () => {
            try {
                throw new NotImplementedError(
                    'test.vue: Testing error handling'
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
    },
};
</script>
