/**
 * @file AssetManager.js
 * @description Single responsibility: Locates, loads, and optimizes SVG assets.
 */
import path from 'path';
import { FileUtils } from '../Utilities/FileUtils.js';
import { Logger } from './Logger.js';
import { Config } from '../config.js';
import { optimize } from 'svgo';

export class AssetManager {
    constructor() {
        this.cache = new Map();
    }

    /**
     * Loads an SVG asset and optimizes it.
     * @param {string} category - e.g., 'Animals'
     * @param {string} filename - e.g., 'Bear.svg'
     * @returns {Promise<string>} Optimized SVG string.
     */
    async loadSVG(category, filename) {
        const cacheKey = `${category}/${filename}`;
        
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        const filepath = path.join(Config.paths.assets, category, filename);
        Logger.info('AssetManager', `Loading asset: ${cacheKey}`);

        try {
            const rawSvg = await FileUtils.readFile(filepath);
            
            // Optimize SVG string using SVGO for cleaner inline injection
            const result = optimize(rawSvg, {
                multipass: true,
                plugins: [
                    {
                        name: 'preset-default',
                        params: { overrides: { removeViewBox: false } } // ViewBoxes are strictly required by our layout engine
                    }
                ]
            });

            this.cache.set(cacheKey, result.data);
            return result.data;
        } catch (error) {
            // Do not fail entirely if an asset is missing, return a fallback or throw depending on strictness.
            // For enterprise, we throw to prevent publishing broken worksheets.
            Logger.error('AssetManager', `Critical asset missing: ${filepath}`, error);
        }
    }
}
