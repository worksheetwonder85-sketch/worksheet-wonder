import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

// Setup __dirname for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config({ path: path.resolve(__dirname, '.env') });

/**
 * Global Configuration for the Publishing Engine
 */
export const Config = {
    paths: {
        content: path.resolve(__dirname, process.env.CONTENT_DATABASE_PATH || '../04_Content_Database'),
        schemas: path.resolve(__dirname, process.env.SCHEMA_PATH || '../05_JSON_Schemas'),
        html: path.resolve(__dirname, process.env.HTML_FRAMEWORK_PATH || '../06_HTML_Framework'),
        css: path.resolve(__dirname, process.env.CSS_FRAMEWORK_PATH || '../07_CSS_Framework'),
        assets: path.resolve(__dirname, process.env.ILLUSTRATION_LIBRARY_PATH || '../03_Illustration_Library'),
        output: path.resolve(__dirname, process.env.OUTPUT_DIR || './output')
    },
    exportSettings: {
        pdf: process.env.ENABLE_PDF_EXPORT !== 'false',
        png: process.env.ENABLE_PNG_EXPORT !== 'false',
        dpi: parseInt(process.env.PDF_DPI) || 300
    }
};
