import { NotImplementedError } from '@/utils/errors';

export default {
    /**
     * @returns {String} A document URL
     */
    temporary_document: function () {
        throw new NotImplementedError('temporary_document');
    },
    burn_plan_element: function (pk) {
        return `/api/burn-plan-element/${pk}/`;
    },
    burn_plan_elements: function () {
        return '/api/burn-plan-elements/';
    },
};
