/**
 * @file TemplateLoader.js
 * @description Single responsibility: Loads and caches HTML template fragments from disk.
 */
import path from 'path';
import { FileUtils } from '../Utilities/FileUtils.js';
import { Logger } from './Logger.js';
import { Config } from '../config.js';

export class TemplateLoader {
    constructor() {
        this.cache = new Map();
    }

    /**
     * Loads a template from disk or returns cached version.
     * @param {string} templateName - Name of the template (e.g., 'header')
     * @returns {Promise<string>} The HTML string.
     */
    async load(templateName) {
        if (this.cache.has(templateName)) {
            return this.cache.get(templateName);
        }

        const ext = templateName.endsWith('.html') ? '' : '.html';
        const filepath = path.join(Config.paths.html, `${templateName}${ext}`);

        Logger.info('TemplateLoader', `Loading template: ${templateName}`);
        
        try {
            const content = await FileUtils.readFile(filepath);
            if (!content) {
                Logger.error('TemplateLoader', `Template file is empty or missing: ${filepath}`);
            }
            this.cache.set(templateName, content);
            return content;
        } catch (error) {
            Logger.error('TemplateLoader', `Failed to load template: ${templateName}`, error);
        }
    }

    /**
     * Pre-load multiple templates into cache simultaneously.
     * @param {string[]} templates - Array of template names.
     */
    async preloadAll(templates) {
        await Promise.all(templates.map(t => this.load(t)));
        Logger.success('TemplateLoader', `Preloaded ${templates.length} templates.`);
    }
}
