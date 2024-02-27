<template>
    <!-- Actions Modal -->
    <div
        id="staticBackdropActions"
        class="modal fade"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
        tabindex="-1"
        aria-labelledby="staticBackdropLabel"
        aria-hidden="true"
    >
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 id="staticBackdropLabel" class="modal-title">
                        Action Logs
                    </h5>
                    <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>
                <div class="modal-body">
                    <DatatableActions :ajax="actionsAjax" />
                </div>
                <div class="modal-footer">
                    <button
                        type="button"
                        class="btn btn-secondary"
                        data-bs-dismiss="modal"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { api_endpoints } from '@/utils/hooks';

import DatatableActions from './DatatableActions.vue';

export default {
    components: { DatatableActions },
    props: {
        contentType: {
            type: Number,
            required: true,
        },
        pk: {
            type: Number,
            required: true,
        },
    },
    computed: {
        actionsAjax: function () {
            return (
                api_endpoints.actions() +
                `?format=datatables&content_type=${this.contentType}&object_id=${this.pk}`
            );
        },
    },
};
</script>
