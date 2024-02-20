import { NotImplementedError } from '@/utils/errors';

export default {
    /**
     * @returns {String} A document URL
     */
    temporary_document: function () {
        throw new NotImplementedError('temporary_document');
    },
    burn_plan_elements: function (pk) {
        if (pk) {
            return `/api/burn-plan-elements/${pk}/`;
        }
        return '/api/burn-plan-elements/';
    },
    endPoint: function (slug, pk = null) {
        if (pk) {
            return `/api/${slug}/${pk}/`;
        }
        return `/api/${slug}/`;
    },
    operationalPlans: function (pk = null) {
        return this.endPoint('operational-plans', pk);
    },
};
