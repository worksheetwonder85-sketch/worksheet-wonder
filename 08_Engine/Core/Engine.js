import path from 'path';
import fs from 'fs/promises';
import { Config } from '../config.js';
import { Logger } from './Logger.js';
import { Validator } from './Validator.js';
import { TemplateLoader } from './TemplateLoader.js';
import { FileUtils } from '../Utilities/FileUtils.js';
import { TemplateCompiler } from '../Compiler/TemplateCompiler.js';
import { PDFExporter } from '../Exporter/PDFExporter.js';

export class Engine {
    constructor() {
        this.validator = new Validator();
        this.templateLoader = new TemplateLoader();
        this.isInitialized = false;
    }

    /**
     * Bootstraps the engine. Preloads templates and schemas.
     */
    async initialize() {
        Logger.info('Engine', 'Initializing publishing engine...');
        
        // 1. Preload common templates
        const coreTemplates = [
            'master_template', 'header', 'hero_letter', 
            'vocabulary', 'finger_trace', 'tracing_section', 
            'writing_section', 'colouring_section', 'footer'
        ];
        await this.templateLoader.preloadAll(coreTemplates);

        Logger.info('Engine', 'Skipping strict schema validation (05_JSON_Schemas pending generation)');

        this.isInitialized = true;
        Logger.success('Engine', 'Initialization complete.');
    }

    /**
     * Compiles and exports a specific worksheet.
     * @param {string} subject - e.g., 'Alphabet'
     * @param {string} id - e.g., 'A'
     */
    async compileAndExport(subject, id) {
        if (!this.isInitialized) Logger.error('Engine', 'Engine must be initialized before compiling.');

        const jsonPath = path.join(Config.paths.content, subject, `${id}.json`);
        Logger.info('Engine', `Loading JSON payload from ${jsonPath}`);
        
        const payload = await FileUtils.readJSON(jsonPath);
        if (!payload) {
            Logger.error('Engine', `Failed to load payload for ${subject}/${id}`);
            return;
        }

        Logger.info('Engine', `JSON Payload loaded successfully for ${id}. Passing to compilers...`);

        // 0. Transform payload into flattened Handlebars context
        const viewData = {
            TITLE: `Letter ${payload.uppercase}`,
            HERO_CONTENT: `${payload.uppercase}${payload.lowercase}`,
            TRACING_ROWS: payload.tracingRows || [],
            BLANK_ROWS: [{}],
            WRITING_ROWS_COUNT: 1, // Satisfies strict parsing in HTML comments
            PARENT_TIP: payload.parentTips || "Practice tracing the letter!",
            PAGE_NUMBER: "2",
            WORKBOOK_TITLE: "Worksheet Wonder Alphabet",
            VERSION: "1.0"
        };

        const { AssetManager } = await import('./AssetManager.js');
        const assetManager = new AssetManager();

        // Load Finger Trace SVG using AssetManager
        const traceSvg = await assetManager.loadSVG('Alphabet', `${payload.uppercase}_trace.svg`);
        viewData.FINGER_TRACE_SVG = traceSvg || `<!-- Missing ${payload.uppercase}_trace.svg -->`;

        const findSVG = async (word, outline = false) => {
            const categories = ['Animals', 'Objects', 'Transport', 'Food', 'General'];
            const fileName = outline ? `${word}_outline.svg` : `${word}.svg`;
            for (const cat of categories) {
                // Read directly first to avoid AssetManager logging missing files continuously
                const tryPath = path.join(Config.paths.assets, cat, fileName);
                try {
                    await fs.access(tryPath);
                    // Use AssetManager to actually load and optimize it once we know it exists
                    return await assetManager.loadSVG(cat, fileName);
                } catch(e) {
                    continue;
                }
            }
            return `<!-- Missing ${fileName} -->`;
        };

        // Inject Vocabulary
        if (payload.vocabulary && payload.vocabulary.length >= 3) {
            for (let i = 0; i < 3; i++) {
                const v = payload.vocabulary[i];
                viewData[`WORD${i+1}`] = v.word;
                viewData[`SVG${i+1}`] = await findSVG(v.word);
            }
            viewData['COLORING_SVG'] = await findSVG(payload.vocabulary[0].word, true);
        }

        // 1. TemplateCompiler merges payload with HTML
        const compiler = new TemplateCompiler(this.templateLoader);
        let finalHTML = compiler.compile(viewData);

        // 2. Inject CSS inline so Puppeteer renders it correctly locally
        const cssFiles = [
            'master_variables.css', 'master_layout.css', 
            'master_components.css', 'master_typography.css',
            'master_handwriting.css', 'master_utilities.css', 'master_print.css'
        ];
        let injectedCSS = '';
        const cssDir = path.join(process.cwd(), '..', '07_CSS_Framework');
        for (const cssFile of cssFiles) {
            try {
                const cssPath = path.join(cssDir, cssFile);
                const content = await fs.readFile(cssPath, 'utf8');
                injectedCSS += `\n/* ${cssFile} */\n${content}\n`;
            } catch (e) {
                Logger.info('Engine', `Could not load CSS: ${cssFile}`);
            }
        }
        
        // Remove link tags and append injected styles
        finalHTML = finalHTML.replace(/<link rel="stylesheet".*?>/g, '');
        finalHTML = finalHTML.replace('</head>', `<style>\n${injectedCSS}\n</style>\n</head>`);

        // 3. Save raw HTML
        const outputDir = path.join(process.cwd(), 'output');
        await fs.mkdir(outputDir, { recursive: true });
        const htmlPath = path.join(outputDir, `Letter_${id}.html`);
        await fs.writeFile(htmlPath, finalHTML, 'utf8');
        Logger.success('Engine', `HTML saved to ${htmlPath}`);

        // 4. PDFExporter spins up Puppeteer and saves PDF/PNG to /output
        await PDFExporter.export(finalHTML, outputDir, `Letter_${id}`);

        Logger.success('Engine', `Compilation & Export complete for ${id}.`);
    }
}
