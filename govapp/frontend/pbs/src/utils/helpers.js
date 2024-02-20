export default {
    /**
     * Formats an error object into a string
     * @param {Error|any} err An error object
     */
    formatError: function (err) {
        let returnStr = '';
        // object {}
        if (
            typeof err.body === 'object' &&
            !Object.prototype.hasOwnProperty.call(err.body, 'length')
        ) {
            for (const key of Object.keys(err.body)) {
                returnStr += `${key}: ${err.body[key]} <br/>`;
            }
            // array
        } else if (typeof err.body === 'object') {
            returnStr = err.body[0];
            // string
        } else {
            returnStr = err.body;
        }
        return returnStr;
    },
    /**
     *
     * @param {Error} errors
     */
    formatErrorV2: function (errors) {
        if (typeof errors === 'string') {
            return errors;
        }
        if (Array.isArray(errors)) {
            if (1 == errors.length) {
                return errors[0];
            } else {
                let errors_str = '';
                for (let i = 0; i < errors.length; i++) {
                    errors_str += errors[i] + '<br/>';
                }
                return errors_str;
            }
        }
        if (typeof errors === 'object') {
            if (1 == Object.keys(errors).length) {
                return Object.values(errors)[0];
            } else {
                let errors_str = '<ul class="list-group text-start">';
                for (const key of Object.keys(errors)) {
                    errors_str += `<li class="list-group-item"><span class="fw-bold">${key}:</span> ${module.exports.escapeHtml(
                        errors[key],
                    )}</li>`;
                }
                return errors_str + '</ul>';
            }
        }
    },
    /**
     * Escape HTML special characters
     * @param {String} htmlStr The string to escape
     */
    escapeHtml: function (htmlStr) {
        return htmlStr
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    },
    /**
     * Returns a cookie value by name
     * @param {String} name The name of the cookie
     */
    getCookie: function (name) {
        let value = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (
                    cookie.substring(0, name.length + 1).trim() ===
                    name + '='
                ) {
                    value = decodeURIComponent(
                        cookie.substring(name.length + 1),
                    );
                    break;
                }
            }
        }
        return value;
    },
    /**
     *
     * @param {string} api_string
     * @param {string} addition
     */
    add_endpoint_join: function (api_string, addition) {
        // assumes api_string has trailing forward slash '/' character required for POST
        let endpoint = api_string + addition;
        endpoint = endpoint.replace('//', '/'); // Remove duplicated '/' just in case
        // if the last character is not a forward slash then add one
        if (endpoint.slice(-1) != '/') {
            endpoint += '/';
        }
        return endpoint;
    },
    enablePopovers: function () {
        const popoverTriggerList = [].slice.call(
            document.querySelectorAll('[data-bs-toggle="popover"]'),
        );
        popoverTriggerList.map(function (popoverTriggerEl) {
            // @ts-expect-error - bootstrap is already loaded via script in the html from webtemplate_dbca
            new bootstrap.Popover(popoverTriggerEl); // eslint-disable-line no-undef
        });
    },
    /**
     *
     * @param {string} filepath
     * @param {string[]=} additional_class_names
     */
    getFileIconClass: function (filepath, additional_class_names = []) {
        const ext = filepath.split('.').pop().toLowerCase();
        const classname = additional_class_names;

        if (['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif'].includes(ext)) {
            classname.push('bi-file-image-fill');
        } else if (['pdf'].includes(ext)) {
            classname.push('bi-file-pdf-fill');
        } else if (['doc', 'docx'].includes(ext)) {
            classname.push('bi-file-word-fill');
        } else if (['xls', 'xlsx'].includes(ext)) {
            classname.push('bi-file-excel-fill');
        } else if (['txt', 'text'].includes(ext)) {
            classname.push('bi-file-text-fill');
        } else if (['rtf'].includes(ext)) {
            classname.push('bi-file-richtext-fill');
        } else if (['mp3', 'mp4'].includes(ext)) {
            classname.push('bi-file-play-fill');
        } else {
            classname.push('bi-file_fill');
        }

        return classname.join(' ');
    },
    replaceUnderscores: function (/** @type {string} */ str) {
        return str.replace(/_/g, ' ');
    },
    bootstrapBadgesFromList: function (/** @type {string[]} */ list) {
        return list.map((item) => {
            return `<span class="badge bg-primary">${item}</span>`;
        });
    },
};
