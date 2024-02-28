<template>
    <!-- Communications Modal -->
    <div
        id="staticBackdropCommunications"
        class="modal fade"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
        tabindex="-1"
        aria-labelledby="staticBackdropLabel"
        aria-hidden="true"
    >
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 id="staticBackdropLabel" class="modal-title">
                        Communication Logs
                    </h5>
                    <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>
                <div class="modal-body">
                    <DatatableCommunications
                        :communications-api-url="communicationsApiUrl"
                    />
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
import DatatableCommunications from './DatatableCommunications.vue';

export default {
    components: { DatatableCommunications },
    props: {
        communicationsApiUrl: {
            type: String,
            required: true,
        },
    },
};
</script>
