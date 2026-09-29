/**
 * @file Validator.js
 * @description Single responsibility: Validates JSON payloads against JSON Schemas.
 */
import Ajv from 'ajv';
import { Logger } from './Logger.js';

export class Validator {
    constructor() {
        // Strict mode off because draft-07 has some loosely defined formats by default
        this.ajv = new Ajv({ allErrors: true, strict: false });
    }

    /**
     * Compile a JSON Schema.
     * @param {string} schemaName - Name for reference.
     * @param {Object} schemaObj - The JSON Schema object.
     */
    addSchema(schemaName, schemaObj) {
        try {
            this.ajv.addSchema(schemaObj, schemaName);
            Logger.info('Validator', `Compiled schema: ${schemaName}`);
        } catch (error) {
            Logger.error('Validator', `Failed to compile schema: ${schemaName}`, error);
        }
    }

    /**
     * Validates data against a pre-compiled schema.
     * @param {string} schemaName - Name of the registered schema.
     * @param {Object} data - The JSON payload to validate.
     * @returns {boolean} True if valid, throws error if invalid.
     */
    validate(schemaName, data) {
        const validateFn = this.ajv.getSchema(schemaName);
        if (!validateFn) {
            Logger.error('Validator', `Schema not found: ${schemaName}`);
        }

        const valid = validateFn(data);
        if (!valid) {
            const errors = this.ajv.errorsText(validateFn.errors);
            Logger.error('Validator', `JSON validation failed for schema ${schemaName}: ${errors}`);
        }

        Logger.success('Validator', `Payload passed validation for ${schemaName}`);
        return true;
    }
}
