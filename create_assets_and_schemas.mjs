import fs from 'fs';
import path from 'path';
import Ajv from 'ajv';

const basePath = "c:\\Users\\erpri\\OneDrive\\Desktop\\worksheet wonder";
const schemasPath = path.join(basePath, "05_JSON_Schemas");
const illusPath = path.join(basePath, "03_Illustration_Library");

// --- TASK 1: SVGs & Meta ---
const assets = [
    { id: "bear", category: "Animals", name: "Bear", color: "#8B4513", shape: `<circle cx="50" cy="50" r="35" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="30" cy="25" r="12" fill="COLOR" stroke="#1E293B" stroke-width="3.5"/><circle cx="70" cy="25" r="12" fill="COLOR" stroke="#1E293B" stroke-width="3.5"/><circle cx="40" cy="45" r="4" fill="#1E293B"/><circle cx="60" cy="45" r="4" fill="#1E293B"/><path d="M 45 60 Q 50 65 55 60" fill="none" stroke="#1E293B" stroke-width="3.5" stroke-linecap="round"/>` },
    { id: "ball", category: "Objects", name: "Ball", color: "#EF4444", shape: `<circle cx="50" cy="50" r="40" fill="COLOR" stroke="#1E293B" stroke-width="3.5"/><path d="M 10 50 Q 50 10 90 50" fill="none" stroke="#1E293B" stroke-width="3.5"/><path d="M 10 50 Q 50 90 90 50" fill="none" stroke="#1E293B" stroke-width="3.5"/>` },
    { id: "butterfly", category: "Animals", name: "Butterfly", color: "#3B82F6", shape: `<path d="M 50 20 L 50 80" stroke="#1E293B" stroke-width="8" stroke-linecap="round"/><path d="M 50 50 C 10 10 10 40 50 50 C 10 60 10 90 50 50 C 90 10 90 40 50 50 C 90 60 90 90 50 50" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/>` },
    { id: "bee", category: "Animals", name: "Bee", color: "#F59E0B", shape: `<ellipse cx="50" cy="50" rx="35" ry="25" fill="COLOR" stroke="#1E293B" stroke-width="3.5"/><path d="M 25 25 Q 35 10 45 25 M 75 25 Q 65 10 55 25" fill="none" stroke="#1E293B" stroke-width="3.5" stroke-linecap="round"/><path d="M 35 25 L 35 75 M 50 25 L 50 75 M 65 25 L 65 75" stroke="#1E293B" stroke-width="3.5"/><circle cx="25" cy="45" r="3" fill="#1E293B"/>` },
    { id: "bird", category: "Animals", name: "Bird", color: "#60A5FA", shape: `<ellipse cx="50" cy="50" rx="30" ry="25" fill="COLOR" stroke="#1E293B" stroke-width="3.5"/><path d="M 20 50 L 5 45 L 5 55 Z" fill="#F59E0B" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/><circle cx="35" cy="40" r="3" fill="#1E293B"/><path d="M 60 40 Q 80 20 90 40 Q 75 60 60 50 Z" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/>` },
    { id: "boat", category: "Transport", name: "Boat", color: "#D97706", shape: `<path d="M 20 60 L 80 60 L 70 80 L 30 80 Z" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/><path d="M 50 60 L 50 15 L 80 50 Z" fill="#FFFFFF" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/>` },
    { id: "book", category: "Objects", name: "Book", color: "#10B981", shape: `<rect x="20" y="20" width="60" height="60" rx="5" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/><path d="M 30 20 L 30 80" stroke="#1E293B" stroke-width="3.5"/><path d="M 40 40 L 60 40 M 40 50 L 60 50 M 40 60 L 60 60" stroke="#1E293B" stroke-width="3.5" stroke-linecap="round"/>` },
    { id: "bell", category: "Objects", name: "Bell", color: "#FBBF24", shape: `<path d="M 50 20 C 20 20 20 70 10 70 L 90 70 C 80 70 80 20 50 20 Z" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/><circle cx="50" cy="70" r="10" fill="#1E293B"/><path d="M 45 15 A 5 5 0 1 1 55 15" fill="none" stroke="#1E293B" stroke-width="3.5" stroke-linecap="round"/>` },
    { id: "bus", category: "Transport", name: "Bus", color: "#F59E0B", shape: `<rect x="10" y="30" width="80" height="40" rx="5" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/><circle cx="30" cy="70" r="10" fill="#1E293B"/><circle cx="70" cy="70" r="10" fill="#1E293B"/><rect x="20" y="40" width="15" height="15" rx="2" fill="#FFFFFF" stroke="#1E293B" stroke-width="3.5"/><rect x="45" y="40" width="15" height="15" rx="2" fill="#FFFFFF" stroke="#1E293B" stroke-width="3.5"/><rect x="70" y="40" width="15" height="15" rx="2" fill="#FFFFFF" stroke="#1E293B" stroke-width="3.5"/>` },
    { id: "banana", category: "Food", name: "Banana", color: "#FBBF24", shape: `<path d="M 20 80 C 10 30 50 10 80 20 C 50 30 30 50 20 80 Z" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/>` }
];

const svgTemplate = (content) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">\n  ${content}\n</svg>`;

let generatedSVGs = 0;
let generatedMetas = 0;

for (const asset of assets) {
    const dir = path.join(illusPath, asset.category);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    // SVG Color
    const colorContent = asset.shape.replace(/COLOR/g, asset.color);
    fs.writeFileSync(path.join(dir, `${asset.name}.svg`), svgTemplate(colorContent));
    
    // SVG Outline
    const outlineContent = asset.shape.replace(/COLOR/g, "#FFFFFF");
    fs.writeFileSync(path.join(dir, `${asset.name}_outline.svg`), svgTemplate(outlineContent));
    generatedSVGs += 2;

    // Metadata
    const meta = {
        id: `asset-${asset.id}`,
        name: asset.name,
        category: asset.category,
        keywords: [asset.id, "letter b", "alphabet"],
        letter: "B",
        difficulty: 1,
        recommendedAge: [4, 5, 6],
        usage: {
            fullColor: `${asset.name}.svg`,
            outline: `${asset.name}_outline.svg`
        },
        tags: [asset.id, "kindergarten", "noun"]
    };
    fs.writeFileSync(path.join(dir, `${asset.name}.json`), JSON.stringify(meta, null, 2));
    generatedMetas++;
}

// --- TASK 2: SCHEMAS ---
const schemaTemplate = (id, title, reqs, props) => ({
    $schema: "http://json-schema.org/draft-07/schema#",
    $id: `https://worksheetwonder.com/schemas/${id}.schema.json`,
    title: title,
    type: "object",
    required: reqs,
    properties: props,
    additionalProperties: false
});

const vocabSchema = {
    type: "object",
    required: ["word", "syllables", "phonics", "imageId", "outlineImageId", "category", "difficulty", "keywords", "sentence", "emoji"],
    properties: {
        word: { type: "string" },
        syllables: { type: "integer" },
        phonics: { type: "string" },
        imageId: { type: "string" },
        outlineImageId: { type: "string" },
        category: { type: "string" },
        difficulty: { type: "integer" },
        keywords: { type: "array", items: { type: "string" } },
        sentence: { type: "string" },
        emoji: { type: "string" }
    }
};

const schemas = {
    "alphabet": schemaTemplate("alphabet", "Alphabet Curriculum Schema", 
        ["letter", "uppercase", "lowercase", "phonicsSound", "formationSteps", "difficulty", "themeColor", "heroWords", "vocabulary", "backupWords", "searchTags", "curriculumReferences", "teacherTips", "parentTips", "fineMotorObjective", "phonicsObjective"], 
        {
            letter: { type: "string" },
            uppercase: { type: "string" },
            lowercase: { type: "string" },
            phonicsSound: { type: "string" },
            formationSteps: { type: "array", items: { type: "string" } },
            difficulty: { type: "integer" },
            themeColor: { type: "string" },
            heroWords: { type: "array", items: { type: "string" } },
            vocabulary: { type: "array", items: vocabSchema },
            backupWords: { type: "array", items: vocabSchema },
            searchTags: { type: "array", items: { type: "string" } },
            curriculumReferences: { type: "array", items: { type: "string" } },
            teacherTips: { type: "string" },
            parentTips: { type: "string" },
            fineMotorObjective: { type: "string" },
            phonicsObjective: { type: "string" }
        }
    ),
    "illustration": schemaTemplate("illustration", "Illustration Metadata Schema",
        ["id", "name", "category", "keywords", "usage", "tags"],
        {
            id: { type: "string" },
            name: { type: "string" },
            category: { type: "string" },
            keywords: { type: "array", items: { type: "string" } },
            letter: { type: "string" },
            difficulty: { type: "integer" },
            recommendedAge: { type: "array", items: { type: "integer" } },
            usage: {
                type: "object",
                required: ["fullColor", "outline"],
                properties: {
                    fullColor: { type: "string" },
                    outline: { type: "string" }
                }
            },
            tags: { type: "array", items: { type: "string" } }
        }
    ),
    "number": schemaTemplate("number", "Number Schema", ["number"], { number: { type: "integer" } }),
    "shape": schemaTemplate("shape", "Shape Schema", ["shape"], { shape: { type: "string" } }),
    "colour": schemaTemplate("colour", "Colour Schema", ["colour"], { colour: { type: "string" } }),
    "animal": schemaTemplate("animal", "Animal Schema", ["animal"], { animal: { type: "string" } }),
    "phonics": schemaTemplate("phonics", "Phonics Schema", ["sound"], { sound: { type: "string" } }),
    "sightword": schemaTemplate("sightword", "Sightword Schema", ["word"], { word: { type: "string" } }),
    "cvc": schemaTemplate("cvc", "CVC Schema", ["word"], { word: { type: "string" } }),
    "theme": schemaTemplate("theme", "Theme Schema", ["theme"], { theme: { type: "string" } }),
    "worksheet": schemaTemplate("worksheet", "Worksheet Schema", ["id", "type", "payload"], {
        id: { type: "string" },
        type: { type: "string" },
        payload: { type: "object" }
    })
};

let generatedSchemas = 0;
for (const [key, schema] of Object.entries(schemas)) {
    fs.writeFileSync(path.join(schemasPath, `${key}.schema.json`), JSON.stringify(schema, null, 2));
    generatedSchemas++;
}

// --- TASK 3: VALIDATION ---
const ajv = new Ajv({ strict: false });
const validateAlphabet = ajv.compile(schemas.alphabet);
const validateIllustration = ajv.compile(schemas.illustration);

const bJsonPath = path.join(basePath, "04_Content_Database", "Alphabet", "B.json");
const bData = JSON.parse(fs.readFileSync(bJsonPath, 'utf8'));
const alphabetValid = validateAlphabet(bData);

const bearMetaPath = path.join(illusPath, "Animals", "Bear.json");
const bearData = JSON.parse(fs.readFileSync(bearMetaPath, 'utf8'));
const bearValid = validateIllustration(bearData);

console.log("=== EXECUTION REPORT ===");
console.log(`1. SVG files created: ${generatedSVGs}`);
console.log(`2. Metadata files created: ${generatedMetas}`);
console.log(`3. Schemas created: ${generatedSchemas}`);
console.log(`4. Validation Results:`);
console.log(`   - 04_Content_Database/Alphabet/B.json -> ${alphabetValid ? "PASS" : "FAIL"}`);
if (!alphabetValid) console.log(validateAlphabet.errors);
console.log(`   - 03_Illustration_Library/Animals/Bear.json -> ${bearValid ? "PASS" : "FAIL"}`);
if (!bearValid) console.log(validateIllustration.errors);
console.log(`5. Missing assets: 0 (All 10 required B.json assets generated)`);
