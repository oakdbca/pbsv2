import { NotImplementedError } from '@/utils/errors';

export default {
    /**
     * @returns {String} A document URL
     */
    temporary_document: function () {
        throw new NotImplementedError('temporary_document');
    },
};
