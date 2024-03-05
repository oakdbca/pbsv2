<template>
    <div class="container">
        <div class="row">
            <div class="col">
                <slot v-if="!loading" name="heading"></slot>
                <ContentLoader
                    v-else
                    width="100%"
                    height="50"
                    class="mb-2"
                ></ContentLoader>
            </div>
        </div>
        <div class="row">
            <div class="col-3">
                <slot v-if="!loading" name="left-menu"></slot>
                <ContentLoader
                    v-else
                    width="100%"
                    height="650"
                    class="mb-3"
                ></ContentLoader>
            </div>
            <div class="col">
                <slot v-if="!loading" name="default"></slot>
                <ContentLoader
                    v-else
                    width="100%"
                    height="650"
                    class="mb-3"
                ></ContentLoader>
            </div>
        </div>
    </div>
</template>

<script>
import { ContentLoader } from 'vue-content-loader';

export default {
    name: 'LayoutDetails',
    components: {
        ContentLoader,
    },
    props: {
        loading: {
            type: Boolean,
            default: true,
        },
    },
};
</script>
