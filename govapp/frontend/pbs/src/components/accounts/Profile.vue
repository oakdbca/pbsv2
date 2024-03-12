<template>
    <div v-if="store.userData" class="container px-5">
        <div class="row">
            <div class="col">
                <h3 class="text-secondary">Profile</h3>
                <div class="row mb-3">
                    <div class="col-sm-6 mb-3 mb-sm-0">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">
                                    {{ store.userData.full_name }}
                                </h5>
                                <div class="card-text">
                                    <table class="table table-sm">
                                        <tbody>
                                            <tr>
                                                <td>Username</td>
                                                <td>
                                                    {{
                                                        store.userData.username
                                                    }}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>First Name</td>
                                                <td>
                                                    {{
                                                        store.userData
                                                            .first_name
                                                    }}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>Last Name</td>
                                                <td>
                                                    {{
                                                        store.userData.last_name
                                                    }}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>Email</td>
                                                <td>
                                                    {{ store.userData.email }}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>Last Login</td>
                                                <td>
                                                    {{
                                                        store.userData
                                                            .last_login_display
                                                    }}
                                                    (<TimeSince
                                                        :date="
                                                            store.userData
                                                                .last_login
                                                        "
                                                        suffix=" ago"
                                                    />)
                                                </td>
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
                                    <span class="badge bg-primary fs-6">
                                        <template
                                            v-if="
                                                store.userData.profile.district
                                            "
                                        >
                                            {{
                                                store.userData.profile.district
                                            }}
                                        </template>
                                        <template v-else
                                            >Not Yet Assigned</template
                                        ></span
                                    >
                                </p>
                            </div>
                            <div class="card-body">
                                <h5 class="card-title">Groups</h5>
                                <p class="card-text">
                                    <span
                                        v-for="group in store.userData.groups"
                                        :key="group"
                                        class="badge bg-primary me-3 fs-6"
                                        >{{ group }}</span
                                    >
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div v-else>Loading...</div>
</template>

<script>
import { useUserStore } from '@/stores/user';

import TimeSince from '@/utils/vue/TimeSince.vue';

export default {
    name: 'ProfileComponent',
    components: {
        TimeSince,
    },
    data() {
        return {
            store: useUserStore(),
        };
    },
};
</script>
