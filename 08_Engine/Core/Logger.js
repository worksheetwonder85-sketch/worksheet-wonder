/**
 * @file Logger.js
 * @description Singleton logger for tracking all engine actions. Never allows silent failures.
 */

export class Logger {
    /**
     * Log an informational message.
     * @param {string} module - The module logging the message (e.g., 'TemplateLoader')
     * @param {string} message - The message to log
     */
    static info(module, message) {
        console.log(`[INFO] [${new Date().toISOString()}] [${module}]: ${message}`);
    }

    /**
     * Log a successful action.
     * @param {string} module - The module logging the message
     * @param {string} message - The message to log
     */
    static success(module, message) {
        console.log(`[SUCCESS] [${new Date().toISOString()}] [${module}]: ${message}`);
    }

    /**
     * Log an error. Throws after logging to prevent silent failures.
     * @param {string} module - The module logging the message
     * @param {string} message - The error message
     * @param {Error} [error] - The actual error object
     */
    static error(module, message, error = null) {
        const errorMsg = `[ERROR] [${new Date().toISOString()}] [${module}]: ${message}`;
        console.error(errorMsg);
        if (error) console.error(error);
        throw new Error(errorMsg); // Enforce rigid failure
    }
}
