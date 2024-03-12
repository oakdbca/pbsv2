<template>
    <div
        id="importBurnPlanningUnits"
        class="modal fade"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
        tabindex="-1"
        aria-labelledby="importBurnPlanningUnitsLabel"
        aria-hidden="true"
    >
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1
                        id="importBurnPlanningUnitsLabel"
                        class="modal-title fs-5"
                    >
                        Import Burn Planning Units
                    </h1>
                    <button
                        type="button"
                        class="btn-close btn-close-white"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <label for="importFile" class="form-label"
                                >Select file to import</label
                            >
                            <input
                                id="importFile"
                                type="file"
                                class="form-control"
                            />
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button
                        type="button"
                        class="btn btn-secondary"
                        data-bs-dismiss="modal"
                    >
                        Cancel
                    </button>
                    <button type="button" class="btn btn-primary">
                        Import
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ModalImportBurnPlanningUnits',
};
</script>

<style lang="scss" scoped></style>
