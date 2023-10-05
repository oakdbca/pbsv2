import { NetworkError } from '@/utils/errors';

export default {
    /**
     * Generic function to fetch data from an endpoint
     * @param {String} url The url endpoint to fetch data from
     * @param {Object} options The options to pass to the fetch function (optional)
     * @returns a Promise
     * @todo Items for future:
     * 1) Best practice way to deal with the resolve and reject from calling code.
     * 2) Does our !response.ok block act appropriately for all possible error response formats that django and drf can respond with.
     * 3) Doesn't handle the fact that 500 errors from django often aren't formatted as json. Therefor is falling
     *      into the network error catch block for 500 errors that don't send a valid response.
     */
    fetchUrl: async function (url, options) {
        return new Promise((resolve, reject) => {
            let f = options === undefined ? fetch(url) : fetch(url, options);
            f.then(async (response) => {
                const contentType = response.headers.get('content-type');
                if (contentType === null) return Promise.resolve(null);

                let data;
                if (contentType === 'application/vnd.ogc.wms_xml') {
                    // KMI WMS returns XML
                    data = await response.text();
                } else {
                    data = await response.json();
                    if (!response.ok) {
                        let error =
                            (data.constructor.name === 'Array' && data) ||
                            (data && data.message) ||
                            response.statusText;
                        console.error(error);
                        reject(error);
                    }
                }
                resolve(data);
            }).catch((error) => {
                console.error(`There was an error fetching from ${url}`, error);
                reject(new NetworkError());
            });
        });
    },
};
