import { constants } from "./hooks";

/** @module GovAppBaseError */

/**
 * @classdesc A base error
 * @extends {Error} */
export class GovAppBaseError extends Error {
    /**
     * @constructor
     * @param {string} message
     */
    constructor(message) {
        super(message);
        this.name = this.constructor.name;

        /** @property {string} sender The origin call of the error */
        this.sender = new Error().stack.split("\n")[3].replace(" at ", "");

        // Error.captureStackTrace(this, this.constructor);
    }
    /**
     * Sets the error message
     * @param {string} message
     */
    setMessage(message) {
        this.message = message;

        if (message) {
            // Append the message to the error message.
            this.message += ` Message: "${message}".`;
        }

        let str = this.message;

        while (str.indexOf("  ") > -1) {
            str = str.replace("  ", " ");
        }

        this.message = str;
    }
}

/** @module NotImplementedError */

/** An error thrown when the given function isn't implemented.
 * @summary An error thrown when the given function isn't implemented.
 * @classdesc An error thrown when the given function isn't implemented.
 * @extends {GovAppBaseError} */
export class NotImplementedError extends GovAppBaseError {
    /**
     * @constructor
     * @param {string} message
     * @this {NotImplementedError}
     */
    constructor(message) {
        super(message);
        this.setMessage(`The method ${this.sender} isn't implemented.`);
        Error.captureStackTrace(this, this.constructor);
    }
}

/** @module NetworkError */

/**
 * @classdesc A network error
 */
export class NetworkError extends GovAppBaseError {
    /**
     * Creates a new NetworkError
     * @class
     * @param {string=} message  The error message
     * @this {NetworkError}
     */
    constructor(message = null) {
        if (message === null) {
            message = constants.ERRORS.NETWORK_ERROR;
        }
        super(message);
        this.setMessage(message);
        Error.captureStackTrace(this, this.constructor);
    }
}
