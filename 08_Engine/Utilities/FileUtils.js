/**
 * @file FileUtils.js
 * @description Provides robust, promise-based file system operations.
 */
import fs from 'fs-extra';
import { Logger } from '../Core/Logger.js';

export class FileUtils {
    /**
     * Reads a file asynchronously.
     * @param {string} filepath - Path to the file.
     * @returns {Promise<string>} File contents as string.
     */
    static async readFile(filepath) {
        try {
            return await fs.readFile(filepath, 'utf8');
        } catch (error) {
            Logger.error('FileUtils', `Failed to read file: ${filepath}`, error);
        }
    }

    /**
     * Reads and parses a JSON file.
     * @param {string} filepath - Path to the JSON file.
     * @returns {Promise<Object>} Parsed JSON object.
     */
    static async readJSON(filepath) {
        try {
            return await fs.readJson(filepath);
        } catch (error) {
            Logger.error('FileUtils', `Failed to parse JSON file: ${filepath}`, error);
        }
    }

    /**
     * Writes content to a file, creating directories if needed.
     * @param {string} filepath - Destination path.
     * @param {string|Buffer} content - Content to write.
     */
    static async writeFile(filepath, content) {
        try {
            await fs.ensureFile(filepath);
            await fs.writeFile(filepath, content);
        } catch (error) {
            Logger.error('FileUtils', `Failed to write file: ${filepath}`, error);
        }
    }
}
