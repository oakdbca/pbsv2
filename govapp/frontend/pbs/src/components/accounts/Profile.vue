<template>
    <div class="container px-5">
        <div class="row">
            <div class="col">
                <h3 class="text-secondary">Profile</h3>
                <div class="row mb-3">
                    <div class="col-sm-6 mb-3 mb-sm-0">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">#Users Name#</h5>
                                <div class="card-text">
                                    <table class="table table-sm">
                                        <tbody>
                                            <tr>
                                                <td>Username</td>
                                                <td>John</td>
                                            </tr>
                                            <tr>
                                                <td>First Name</td>
                                                <td>John</td>
                                            </tr>
                                            <tr>
                                                <td>Last Name</td>
                                                <td>Doe</td>
                                            </tr>
                                            <tr>
                                                <td>Email</td>
                                                <td>Email</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">District</h5>
                                <p class="card-text">
                                    <select class="form-select">
                                        <option value="1">District 1</option>
                                        <option value="2">District 2</option>
                                        <option value="3">District 3</option>
                                        <option value="4">District 4</option>
                                    </select>
                                </p>
                            </div>
                            <div class="card-body">
                                <h5 class="card-title">Groups</h5>
                                <p class="card-text">
                                    <span class="badge bg-primary"
                                        >Group 1</span
                                    >
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ProfileComponent',
    data() {
        return {};
    },
    created() {},
    methods: {},
};
</script>

<style lang="scss" scoped></style>
