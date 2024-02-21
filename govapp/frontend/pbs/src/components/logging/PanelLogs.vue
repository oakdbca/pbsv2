<template>
    <div class="card mb-3">
        <div class="card-header">Logs</div>
        <div class="card-body border-bottom">
            <label for="assigned-to" class="form-label">Communications</label>
            <div class="rounded border py-2">
                <span class="ps-3 pe-2"><i class="bi bi-card-list"></i> </span>
                <a
                    href="#"
                    class="pe-5"
                    data-bs-toggle="modal"
                    data-bs-target="#staticBackdropCommunications"
                    >View</a
                >
                <span class="pe-2">
                    <i class="bi bi-plus-circle"></i>
                </span>
                <a
                    href="#"
                    data-bs-toggle="modal"
                    data-bs-target="#staticBackdropCommunicationsAdd"
                    >Add Entry</a
                >
            </div>
        </div>
        <div class="card-body">
            <label for="assigned-to" class="form-label">Actions</label>
            <div class="rounded border py-2">
                <span class="ps-3 pe-2"><i class="bi bi-card-list"></i> </span>
                <a
                    href="#"
                    class=""
                    data-bs-toggle="modal"
                    data-bs-target="#staticBackdropActions"
                    >View</a
                >
            </div>
        </div>
    </div>
    <ModalCommunications :content-type="38" :pk="1" />
    <ModalCommunicationsAdd :content-type="38" :pk="1" />
    <ModalActions :content-type="38" :pk="1" />
</template>

<script>
import ModalCommunications from './ModalCommunications.vue';
import ModalCommunicationsAdd from './ModalCommunicationsAdd.vue';
import ModalActions from './ModalActions.vue';

export default {
    name: 'PanelLogs',
    components: {
        ModalCommunications,
        ModalCommunicationsAdd,
        ModalActions,
    },
    props: {
        modelName: {
            type: String,
            required: true,
        },
        pk: {
            type: Number,
            required: true,
        },
    },
};
</script>
