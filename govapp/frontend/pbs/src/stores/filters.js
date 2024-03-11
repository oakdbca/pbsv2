import { defineStore } from 'pinia';
import { useLocalStorage } from '@vueuse/core';

export const useFilterStore = defineStore('filter', {
    state: () => ({
        filterData: useLocalStorage('filterData', {}),
    }),
});
