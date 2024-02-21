<template>
    <!-- Add New Communication Log Modal -->
    <div
        id="staticBackdropCommunicationsAdd"
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
                        Communication Log - Add Entry
                    </h5>
                    <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>
                <div class="modal-body">
                    <div class="container-fluid">
                        <div class="row">
                            <form
                                id="communications-add-form"
                                class="needs-validation"
                                novalidate
                            >
                                <div v-if="errors">
                                    <BootstrapAlert
                                        id="errors"
                                        ref="errors"
                                        class="d-flex align-items-center"
                                        type="danger"
                                        icon="exclamation-triangle-fill"
                                    >
                                        <ErrorRenderer :errors="errors" />
                                    </BootstrapAlert>
                                </div>

                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <div class="row mb-2">
                                            <label
                                                class="col-form-label col-sm-3"
                                                for="to"
                                                >To</label
                                            >
                                            <div class="col-sm-9">
                                                <input
                                                    id="to"
                                                    v-model="communication.to"
                                                    type="text"
                                                    class="form-control"
                                                    name="to"
                                                    autofocus
                                                    required
                                                />
                                            </div>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <div class="row mb-2">
                                            <label
                                                class="col-form-label col-sm-3"
                                                for="fromm"
                                                >From</label
                                            >
                                            <div class="col-sm-9">
                                                <input
                                                    v-model="
                                                        communication.fromm
                                                    "
                                                    type="text"
                                                    class="form-control"
                                                    name="fromm"
                                                    maxlength="200"
                                                    required
                                                />
                                            </div>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <div class="row mb-2">
                                            <label
                                                class="col-form-label col-sm-3"
                                                for="type"
                                                >Type</label
                                            >
                                            <div class="col-sm-9">
                                                <select
                                                    v-model="communication.type"
                                                    class="form-select"
                                                    name="type"
                                                    required
                                                >
                                                    <option
                                                        value=""
                                                        selected
                                                        disabled
                                                    >
                                                        Select Type
                                                    </option>
                                                    <option value="email">
                                                        Email
                                                    </option>
                                                    <option value="mail">
                                                        Mail
                                                    </option>
                                                    <option value="phone">
                                                        Phone
                                                    </option>
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <div class="row mb-2">
                                            <label
                                                class="col-form-label col-sm-3"
                                                for="subject"
                                                >Subject</label
                                            >
                                            <div class="col-sm-9">
                                                <input
                                                    v-model="
                                                        communication.subject
                                                    "
                                                    type="text"
                                                    class="form-control"
                                                    name="subject"
                                                    maxlength="200"
                                                    required
                                                />
                                            </div>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <div class="row mb-2">
                                            <label
                                                class="col-form-label col-sm-3"
                                                for="text"
                                                >Text</label
                                            >
                                            <div class="col-sm-9">
                                                <textarea
                                                    v-model="communication.text"
                                                    name="text"
                                                    class="form-control"
                                                    required
                                                ></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <div class="row mb-2">
                                            <label
                                                class="col-form-label col-sm-3"
                                                for=""
                                                >Attachments</label
                                            >
                                            <div class="col-sm-9">
                                                <template
                                                    v-if="files && files.length"
                                                >
                                                    <ul class="list-group">
                                                        <li
                                                            v-for="(
                                                                f, i
                                                            ) in files"
                                                            :key="i"
                                                            class="list-group-item rounded"
                                                        >
                                                            <div class="row">
                                                                <div
                                                                    class="col"
                                                                >
                                                                    <span
                                                                        v-if="
                                                                            f.file ==
                                                                            null
                                                                        "
                                                                        class="btn btn-primary btn-sm btn-file float-start"
                                                                        ><i
                                                                            class="fa fa-upload"
                                                                            aria-hidden="true"
                                                                        ></i>

                                                                        Attach
                                                                        File
                                                                        <input
                                                                            type="file"
                                                                            :name="
                                                                                'file-upload-' +
                                                                                i
                                                                            "
                                                                            :class="
                                                                                'file-upload-' +
                                                                                i
                                                                            "
                                                                            @change="
                                                                                uploadFile(
                                                                                    'file-upload-' +
                                                                                        i,
                                                                                    f,
                                                                                )
                                                                            "
                                                                        />
                                                                    </span>
                                                                    <span
                                                                        v-else
                                                                        class="btn btn-secondary btn-file btn-sm float-start"
                                                                        ><i
                                                                            class="fa fa-edit"
                                                                        ></i>
                                                                        Update
                                                                        File
                                                                        <input
                                                                            type="file"
                                                                            :name="
                                                                                'file-upload-' +
                                                                                i
                                                                            "
                                                                            :class="
                                                                                'file-upload-' +
                                                                                i
                                                                            "
                                                                            @change="
                                                                                uploadFile(
                                                                                    'file-upload-' +
                                                                                        i,
                                                                                    f,
                                                                                )
                                                                            "
                                                                        />
                                                                    </span>
                                                                </div>
                                                                <div
                                                                    class="col-7 text-truncate"
                                                                >
                                                                    {{ f.name }}
                                                                </div>
                                                                <div
                                                                    class="col-sm-1"
                                                                >
                                                                    <button
                                                                        v-if="
                                                                            f.file ||
                                                                            i >
                                                                                0
                                                                        "
                                                                        class="btn btn-danger btn-sm"
                                                                        @click.prevent="
                                                                            removeFile(
                                                                                i,
                                                                            )
                                                                        "
                                                                    >
                                                                        <i
                                                                            class="fa fa-trash"
                                                                            aria-hidden="true"
                                                                        ></i>
                                                                    </button>
                                                                </div>
                                                            </div>
                                                        </li>
                                                    </ul>
                                                </template>
                                                <div
                                                    class="border-top mt-3 p-2"
                                                >
                                                    <button
                                                        class="btn btn-sm btn-primary"
                                                        @click.prevent="
                                                            attachAnother
                                                        "
                                                    >
                                                        <i
                                                            class="fa fa-add"
                                                        ></i>
                                                        Add Another File
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
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
import ErrorRenderer from '@/utils/vue/ErrorRenderer.vue';

export default {
    components: {
        ErrorRenderer,
    },
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
    data() {
        return {
            communication: {
                to: '',
                fromm: '',
                type: '',
                subject: '',
                text: '',
            },
            files: [],
            errors: null,
        };
    },
};
</script>
