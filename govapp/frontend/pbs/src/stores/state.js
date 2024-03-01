import { defineStore } from 'pinia';
import { useSessionStorage } from '@vueuse/core';
import { apiEndpoints } from '@/utils/hooks';

export const useStore = defineStore('main', {
    state: () => ({
        userData: useSessionStorage('userData', {
            id: '',
            username: '',
            first_name: '',
            last_name: '',
            full_name: '',
            email: '',
            profile: {
                district: '',
            },
            groups: [],
        }),
    }),
    actions: {
        async fetchUserData() {
            fetch(apiEndpoints.userData())
                .then(async (response) => {
                    const data = await response.json();
                    if (!response.ok) {
                        const error =
                            (data && data.message) || response.statusText;
                        console.log(error);
                        return Promise.reject(error);
                    }
                    this.userData = data;
                })
                .catch((error) => {
                    console.error('Error fetching user data!', error);
                });
        },
    },
});
