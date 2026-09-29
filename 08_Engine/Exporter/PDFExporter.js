/**
 * @file PDFExporter.js
 * @description Single responsibility: Uses Puppeteer to render HTML strings and export 300-DPI A4 PDFs and PNG previews.
 */
import puppeteer from 'puppeteer';
import path from 'path';
import { Logger } from '../Core/Logger.js';
import { Config } from '../config.js';
import { FileUtils } from '../Utilities/FileUtils.js';

export class PDFExporter {
    /**
     * Launches a headless browser, renders the HTML, and saves a PDF and PNG.
     * @param {string} htmlContent - The fully compiled HTML string.
     * @param {string} outputDir - Directory to save the file.
     * @param {string} filename - e.g., 'Letter_A'
     */
    static async export(htmlContent, outputDir, filename) {
        Logger.info('PDFExporter', `Initializing headless browser for ${filename}...`);
        let browser;

        try {
            await FileUtils.writeFile(path.join(outputDir, '.keep'), '');

            browser = await puppeteer.launch({
                headless: 'new',
                args: ['--no-sandbox', '--disable-setuid-sandbox']
            });

            const page = await browser.newPage();
            
            // Set Viewport for PNG accurate rendering (A4 is 210x297mm, at 300dpi approx 2480x3508 pixels)
            await page.setViewport({ width: 1240, height: 1754, deviceScaleFactor: 2 });
            
            // Wait for svgs and fonts
            await page.setContent(htmlContent, { waitUntil: 'networkidle0' });

            const pdfPath = path.join(outputDir, `${filename}.pdf`);
            const pngPath = path.join(outputDir, `${filename}.png`);
            
            // Export strictly to A4 specs
            await page.pdf({
                path: pdfPath,
                format: 'A4',
                printBackground: true,
                preferCSSPageSize: true,
                margin: { top: 0, right: 0, bottom: 0, left: 0 }
            });
            Logger.success('PDFExporter', `Successfully exported PDF: ${pdfPath}`);

            // Take a PNG screenshot
            await page.screenshot({ path: pngPath, fullPage: true });
            Logger.success('PDFExporter', `Successfully exported PNG: ${pngPath}`);

        } catch (error) {
            Logger.error('PDFExporter', `Failed to export media for ${filename}`, error);
        } finally {
            if (browser) {
                await browser.close();
                Logger.info('PDFExporter', 'Headless browser closed.');
            }
        }
    }
}
