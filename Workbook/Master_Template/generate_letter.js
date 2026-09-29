/**
 * WORKSHEET WONDER - MASTER LETTER WORKSHEET GENERATOR
 * Node.js automation script to generate publication-ready alphabet worksheets.
 * 
 * Usage:
 *   node generate_letter.js [path/to/config.json] [output/path.html]
 * 
 * Example:
 *   node generate_letter.js alphabet_template.json Letter_B.html
 */

const fs = require('fs');
const path = require('path');

// ── 1. Parse Command Line Arguments & File Paths ──
const scriptDir = __dirname;
const configArg = process.argv[2] || path.join(scriptDir, 'alphabet_template.json');

if (!fs.existsSync(configArg)) {
  console.error(`❌ Error: Configuration file not found at "${configArg}"`);
  process.exit(1);
}

const configData = JSON.parse(fs.readFileSync(configArg, 'utf8'));
const letterUpper = (configData.uppercase || configData.letter || 'A').toUpperCase();
const letterLower = configData.lowercase || letterUpper.toLowerCase();

const defaultOutputName = `Letter_${letterUpper}.html`;
const outputArg = process.argv[3] || path.join(scriptDir, defaultOutputName);
const templatePath = path.join(scriptDir, 'master_alphabet_template.html');

if (!fs.existsSync(templatePath)) {
  console.error(`❌ Error: Master template HTML not found at "${templatePath}"`);
  process.exit(1);
}

// ── 2. Read Template ──
let htmlContent = fs.readFileSync(templatePath, 'utf8');

// ── 3. Extract Words & Rest Strings ──
const words = configData.words || ['Word1', 'Word2', 'Word3'];
const word1 = words[0] || 'Word1';
const word2 = words[1] || 'Word2';
const word3 = words[2] || 'Word3';

const word1Rest = word1.length > 1 ? word1.substring(1) : '';
const word2Rest = word2.length > 1 ? word2.substring(1) : '';
const word3Rest = word3.length > 1 ? word3.substring(1) : '';

// ── 4. Extract SVGs ──
const illust = configData.illustrations || {};
const svg1 = illust.svg1 || '<svg width="72" height="72" viewBox="0 0 80 80"><circle cx="40" cy="40" r="30" fill="#5B9BD5"/></svg>';
const svg2 = illust.svg2 || '<svg width="72" height="72" viewBox="0 0 80 80"><circle cx="40" cy="40" r="30" fill="#3A6FA0"/></svg>';
const svg3 = illust.svg3 || '<svg width="72" height="72" viewBox="0 0 80 80"><circle cx="40" cy="40" r="30" fill="#EAF4FB"/></svg>';

// ── 5. Define Replacement Map ──
const replacements = {
  '{{LETTER}}': letterUpper,
  '{{LOWERCASE}}': letterLower,
  '{{WORKSHEET_TITLE}}': configData.worksheetTitle || `The Letter ${letterUpper} (Uppercase)`,
  '{{SUBTITLE}}': configData.subtitle || 'Uppercase · Trace · Write · Learn',
  '{{GRADE_TAG}}': configData.gradeTag || 'Kindergarten',
  '{{AGE_TAG}}': configData.ageTag || 'Ages 4–6',
  '{{THEME_COLOR}}': configData.themeColor || '#5B9BD5',
  '{{THEME_COLOR_SECONDARY}}': configData.themeColorSecondary || '#3A6FA0',
  '{{THEME_COLOR_LIGHT}}': configData.themeColorLight || '#EAF4FB',
  '{{THEME_COLOR_BORDER}}': configData.themeColorBorder || '#C8DFF0',
  '{{WORD1}}': word1,
  '{{WORD2}}': word2,
  '{{WORD3}}': word3,
  '{{WORD1_REST}}': word1Rest,
  '{{WORD2_REST}}': word2Rest,
  '{{WORD3_REST}}': word3Rest,
  '{{SVG1}}': svg1,
  '{{SVG2}}': svg2,
  '{{SVG3}}': svg3,
  '{{DOC_CODE}}': configData.docCode || `WW-KG-LTR-${letterUpper}-01`,
  '{{YEAR}}': configData.year || '2026'
};

// ── 6. Execute Placeholder Replacement ──
for (const [placeholder, value] of Object.entries(replacements)) {
  const regex = new RegExp(placeholder.replace(/[{}]/g, '\\$&'), 'g');
  htmlContent = htmlContent.replace(regex, value);
}

// ── 7. Quality Check for Unreplaced Placeholders ──
const unreplacedMatches = htmlContent.match(/\{\{[A-Z0-9_]+\}\}/g);
if (unreplacedMatches) {
  console.warn(`⚠️ Warning: Found unreplaced placeholders in output: ${[...new Set(unreplacedMatches)].join(', ')}`);
}

// ── 8. Write Generated HTML File ──
fs.writeFileSync(outputArg, htmlContent, 'utf8');

console.log(`✨ Success! Generated worksheet for Letter "${letterUpper}"`);
console.log(`📄 Saved to: ${outputArg}`);
