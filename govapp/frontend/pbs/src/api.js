import { NotImplementedError } from '@/utils/errors';

export default {
    /**
     * @returns {String} A document URL
     */
    temporary_document: function () {
        throw new NotImplementedError('temporary_document');
    },
    burnPlanElements: function (pk) {
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
    burnPlanningUnits: function (pk = null) {
        return this.endPoint('burn-planning-units', pk);
    },
    userData: function () {
        return this.endPoint('users/me', null);
    },
    operationalPlans: function (pk = null) {
        return this.endPoint('operational-plans', pk);
    },
    actions: function (pk = null) {
        return this.endPoint('actions', pk);
    },
    communications: function (pk = null) {
        return this.endPoint('communications', pk);
    },
    assignableUsers: function () {
        return this.endPoint('assignable-users', null);
    },
    assignToMe: function () {
        return this.endPoint('assign-to-me', null);
    },
    assignTo: function () {
        return this.endPoint('assign-to', null);
    },
    search: function (query = null) {
        return `/api/search/?q=${query}`;
    },
    latestMessages: function () {
        return this.endPoint('messages/latest', null);
    },
    dismissMessage: function (pk) {
        var endPoint = this.endPoint('messages', pk);
        return `${endPoint}dismiss/`;
    },
    assignedItems: function () {
        return this.endPoint('assigned-items', null);
    },
    endorsmentItems: function () {
        return this.endPoint('items-requiring-endorsement', null);
    },
};
