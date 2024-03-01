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
                        class="btn-close btn-close-white"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>
                <div class="modal-body">
                    <DatatableCommunications
                        :communications-api-url="communicationsApiUrl"
                        @selected-communication-log="toggleDetailsModal"
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
    <div
        id="detailsModal"
        class="modal"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
        aria-hidden="true"
        aria-labelledby="detailsModalLabel"
        tabindex="-1"
    >
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div v-if="selectedCommunicationLog" class="modal-content">
                <div class="modal-header">
                    <h5 id="detailsModalLabel" class="modal-title">
                        {{ selectedCommunicationLog.type }} from
                        {{ selectedCommunicationLog.from }} logged by
                        {{ selectedCommunicationLog.username }} on
                        {{ selectedCommunicationLog.created_at }}
                    </h5>
                    <button
                        type="button"
                        class="btn-close btn-close-white"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>
                <div class="modal-body">
                    <div class="table-responsive p-2">
                        <table class="table table-striped">
                            <tbody>
                                <tr>
                                    <th scope="row">Logged By</th>
                                    <td>
                                        {{ selectedCommunicationLog.username }}
                                    </td>
                                </tr>
                                <tr>
                                    <th scope="row">Date Logged</th>
                                    <td>
                                        {{
                                            selectedCommunicationLog.created_at
                                        }}
                                    </td>
                                </tr>
                                <tr>
                                    <th scope="row">Type</th>
                                    <td>{{ selectedCommunicationLog.type }}</td>
                                </tr>
                                <tr>
                                    <th scope="row">To</th>
                                    <td>{{ selectedCommunicationLog.to }}</td>
                                </tr>
                                <tr v-if="selectedCommunicationLog.cc">
                                    <th scope="row">CC</th>
                                    <td>{{ selectedCommunicationLog.cc }}</td>
                                </tr>
                                <tr>
                                    <th scope="row">From</th>
                                    <td>{{ selectedCommunicationLog.from }}</td>
                                </tr>
                                <tr>
                                    <th scope="row">Subject</th>
                                    <td>
                                        {{ selectedCommunicationLog.subject }}
                                    </td>
                                </tr>
                                <tr>
                                    <th scope="row">Text</th>
                                    <td>{{ selectedCommunicationLog.text }}</td>
                                </tr>
                                <tr>
                                    <th scope="row">Documents</th>
                                    <td>
                                        <div
                                            v-if="
                                                selectedCommunicationLog.documents
                                            "
                                            class="list-group"
                                        >
                                            <a
                                                v-for="document in selectedCommunicationLog.documents"
                                                :key="document.id"
                                                :href="document.file"
                                                target="_blank"
                                                class="list-group-item list-group-item-action"
                                                >{{ document.name }}
                                                <i
                                                    class="bi bi-file-earmark-text"
                                                ></i
                                            ></a>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="modal-footer">
                    <button
                        type="button"
                        class="btn btn-secondary pe-2"
                        data-bs-dismiss="modal"
                    >
                        Close
                    </button>
                    <button
                        class="btn btn-primary"
                        data-bs-target="#staticBackdropCommunications"
                        data-bs-toggle="modal"
                        data-bs-dismiss="modal"
                    >
                        Back to all communications
                        <i class="bi bi-back ps-1"></i>
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
    data: function () {
        return {
            selectedCommunicationLog: null,
        };
    },
    methods: {
        toggleDetailsModal: function (selectedCommunicationLog) {
            this.selectedCommunicationLog = selectedCommunicationLog;
            var staticBackdropCommunicationsElement = document.getElementById(
                'staticBackdropCommunications'
            );
            var staticBackdropCommunicationsModal =
                bootstrap.Modal.getOrCreateInstance(
                    staticBackdropCommunicationsElement
                );
            staticBackdropCommunicationsModal.hide();

            var detailsModalElement = document.getElementById('detailsModal');
            var detailsModal =
                bootstrap.Modal.getOrCreateInstance(detailsModalElement);
            detailsModal.show();
        },
    },
};
</script>
