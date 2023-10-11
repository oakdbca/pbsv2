/**
 * @namespace typedefs
 */

/**
 * @template T generic type parameter
 * @typedef {T extends (undefined | null) ? never : T} NonUndefinedType<T>
 * @memberof typedefs
 */
/**
 * @typedef {NonUndefinedType<string>} DateStr
 * @memberof typedefs
 */

// Allows for typedef import in jsdoc comment: `@param {import('./typedefs').DateStr} date_str`
// export default {}; // Not needed because typedefs are included with jsconfig.json
