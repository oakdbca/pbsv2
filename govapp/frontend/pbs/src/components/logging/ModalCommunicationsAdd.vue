<template>
    <!-- Add New Communication Log Modal -->
    <div
        id="staticBackdropCommunicationsAdd"
        class="modal"
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
                        class="btn-close btn-close-white"
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
                                                <div class="invalid-feedback">
                                                    Please enter who the
                                                    communication was to.
                                                </div>
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
                                                <div class="invalid-feedback">
                                                    Please enter who the
                                                    communication was from.
                                                </div>
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
                                                    id="type"
                                                    v-model="communication.type"
                                                    class="form-select"
                                                    name="type"
                                                    required
                                                >
                                                    <option
                                                        selected
                                                        disabled
                                                        :value.attr="''"
                                                    >
                                                        Select Type
                                                    </option>
                                                    <option value="1">
                                                        Email
                                                    </option>
                                                    <option value="2">
                                                        Phone
                                                    </option>
                                                    <option value="3">
                                                        Mail
                                                    </option>
                                                    <option value="4">
                                                        Person
                                                    </option>
                                                    <option value="5">
                                                        Other
                                                    </option>
                                                </select>
                                                <div class="invalid-feedback">
                                                    Please select the type of
                                                    communication.
                                                </div>
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
                                                <div class="invalid-feedback">
                                                    Please enter subject of the
                                                    communication.
                                                </div>
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
                                                <div class="invalid-feedback">
                                                    Please enter text of the
                                                    communication.
                                                </div>
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
                                                                        class="btn btn-primary btn-file float-start"
                                                                        ><i
                                                                            class="bi bi-file-earmark-arrow-up"
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
                                                                                    f
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
                                                                                    f
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
                                                                                i
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
                        Cancel
                    </button>
                    <button
                        type="button"
                        class="btn btn-primary"
                        @click.prevent="validateForm"
                    >
                        Add Entry
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { constants } from '@/utils/hooks';

export default {
    props: {
        postCommunicationsEntryApiUrl: {
            type: String,
            required: true,
        },
        contentType: {
            type: Number,
            required: true,
        },
        objectId: {
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
            files: [
                {
                    file: null,
                    name: '',
                },
            ],
            errors: null,
        };
    },
    mounted() {
        var communicationsModal = document.getElementById(
            'staticBackdropCommunicationsAdd'
        );
        communicationsModal.addEventListener('shown.bs.modal', function () {
            $('input[name="to"]').trigger('focus');
        });
    },
    methods: {
        uploadFile(target, file_obj) {
            let _file = null;
            let input = $('.' + target)[0];
            if (input.files && input.files[0]) {
                let reader = new FileReader();
                reader.readAsDataURL(input.files[0]);
                reader.onload = function (e) {
                    _file = e.target.result;
                };
                _file = input.files[0];
            }
            file_obj.file = _file;
            file_obj.name = _file.name;
        },
        removeFile(index) {
            let length = this.files.length;
            $('.file-row-' + index).remove();
            this.files.splice(index, 1);
            this.$nextTick(() => {
                length == 1 ? this.attachAnother() : '';
            });
        },
        attachAnother() {
            this.files.push({
                file: null,
                name: '',
            });
        },
        close: function () {
            let vm = this;
            this.communication = {
                type: '',
            };
            this.errors = null;
            $('#communications-add-form').removeClass('was-validated');
            let file_length = vm.files.length;
            this.files = [];
            for (let i = 0; i < file_length; i++) {
                vm.$nextTick(() => {
                    $('.file-row-' + i).remove();
                });
            }
            this.attachAnother();
            const communicationsAddModal = bootstrap.Modal.getInstance(
                document.getElementById('staticBackdropCommunicationsAdd')
            );
            communicationsAddModal.hide();
        },
        validateForm: function () {
            const form = document.getElementById('communications-add-form');

            if (form.checkValidity()) {
                this.postCommunicationsEntry();
            } else {
                form.classList.add('was-validated');
                $('#communications-add-form').find(':invalid').first().focus();
            }

            return false;
        },
        postCommunicationsEntry: function () {
            let vm = this;
            const form = document.getElementById('communications-add-form');
            let formData = new FormData(form);
            formData.append('content_type', this.contentType);
            formData.append('object_id', this.objectId);
            for (let i = 0; i < vm.files.length; i++) {
                formData.append('files', vm.files[i].file);
            }
            fetch(vm.postCommunicationsEntryApiUrl, {
                body: formData,
                method: 'POST',
            })
                .then(async (response) => {
                    const data = await response.json();
                    if (!response.ok) {
                        vm.errors = data || response.statusText;
                        return;
                    }
                    swal.fire({
                        title: 'Success',
                        text: 'Communication log entry added successfully',
                        icon: 'success',
                        showConfirmButton: false,
                        timer: 1500,
                    });
                    vm.close();
                })
                .catch((error) => {
                    console.error('There was an error:', error);
                });
        },
    },
};
</script>

<style scoped lang="css">
.btn-file {
    position: relative;
    overflow: hidden;
}

.btn-file input[type='file'] {
    position: absolute;
    top: 0;
    right: 0;
    min-width: 100%;
    min-height: 100%;
    font-size: 100px;
    text-align: right;
    filter: alpha(opacity=0);
    opacity: 0;
    outline: none;
    background: white;
    cursor: inherit;
    display: block;
}
</style>
