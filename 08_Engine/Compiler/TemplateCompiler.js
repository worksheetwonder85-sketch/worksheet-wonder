/**
 * @file TemplateCompiler.js
 * @description Single responsibility: Uses Handlebars to merge JSON payloads with HTML fragments.
 */
import Handlebars from 'handlebars';
import { Logger } from '../Core/Logger.js';

export class TemplateCompiler {
    /**
     * @param {TemplateLoader} templateLoader - Injected dependency
     */
    constructor(templateLoader) {
        this.templateLoader = templateLoader;
        this.isReady = false;
    }

    /**
     * Registers all preloaded partials with Handlebars.
     */
    registerPartials() {
        try {
            for (const [name, content] of this.templateLoader.cache.entries()) {
                if (name !== 'master_template') {
                    Handlebars.registerPartial(name, content);
                }
            }
            this.isReady = true;
            Logger.success('TemplateCompiler', 'All HTML partials successfully registered with Handlebars.');
        } catch (error) {
            Logger.error('TemplateCompiler', 'Failed to register Handlebars partials', error);
        }
    }

    /**
     * Compiles a worksheet payload into final HTML.
     * @param {Object} payload - The validated JSON data.
     * @returns {string} Fully compiled HTML string.
     */
    compile(payload) {
        if (!this.isReady) {
            this.registerPartials();
        }

        const masterTemplateStr = this.templateLoader.cache.get('master_template');
        if (!masterTemplateStr) {
            Logger.error('TemplateCompiler', 'master_template is missing from cache. Cannot compile.');
        }

        try {
            Logger.info('TemplateCompiler', `Compiling worksheet: ${payload.title || payload.letter || 'Unknown'}`);
            const template = Handlebars.compile(masterTemplateStr, { strict: true });
            
            // Generate the final HTML by injecting the payload
            const finalHTML = template(payload);
            Logger.success('TemplateCompiler', 'Worksheet successfully compiled to HTML string.');
            
            return finalHTML;
        } catch (error) {
            Logger.error('TemplateCompiler', 'Handlebars compilation failed. Check payload variables.', error);
        }
    }
}
