import { defineStore } from 'pinia';
import { useLocalStorage } from '@vueuse/core';

export const useAccordionStore = defineStore('accordion', {
    state: () => ({
        accordionData: useLocalStorage('accordionData', {}),
    }),
});
