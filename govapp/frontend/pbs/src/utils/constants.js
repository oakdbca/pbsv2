module.exports = {
    DATATABLE_PROCESSING_HTML:
        '<div class="d-flex justify-content-center"><div class="d-flex spinner-border text-primary my-4" role="status"><span class="visually-hidden">Loading...</span></div></div>',

    SUPPORT_EMAIL: '?.?@dbca.wa.gov.au',

    ERRORS: {
        NETWORK_ERROR: `NETWORK ERROR: Please check your internet connection and try again. If the problem persists contact us at: ${this.SUPPORT_EMAIL}`,
        API_ERROR:
            'API ERROR: An error has occured accessing the Prescribed Burns System API. Please try again \
            in an hour and if the problem persists contact us at: ?.?@dbca.wa.gov.au',
        API_ERROR_INTERNAL:
            'API ERROR: An error has occured accessing the Prescribed Burns System API. Please try again \
            in an hour and if the problem persists contact the IT Service Desk.',
    },
};
