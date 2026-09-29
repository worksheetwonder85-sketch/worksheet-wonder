# Worksheet Wonder: The Node.js Publishing Engine

This repository (`08_Engine`) contains the bespoke Node.js application responsible for parsing the JSON database, injecting data into the HTML framework, resolving SVG vectors, applying the CSS grid layout, and compiling production-ready, CMYK-safe A4 PDFs.

## Architecture

The engine strictly adheres to the Single Responsibility Principle (SRP):
- **Core**: Orchestration (`Engine.js`), logging (`Logger.js`), schema validation (`Validator.js`), and caching layers (`TemplateLoader.js`, `AssetManager.js`).
- **Compiler**: Uses `Handlebars` to bind JSON payloads to the HTML partials.
- **Renderer / Exporter**: Spins up a headless `Puppeteer` Chrome instance to accurately render the CSS math and output raw PDF/PNG files.
- **Config**: Relies on `.env` and `config.js` for flexible environment paths.

## Installation
Ensure you are running Node v18+.
```bash
cd 08_Engine
npm install
```

## CLI Usage
The engine uses `commander` to expose a simple CLI:

**Generate a specific worksheet:**
```bash
node build.js alphabet A
node build.js numbers 5
```

**Run Development Watcher:**
```bash
node generate.js --watch
```

## Error Handling
The `Logger.js` module explicitly forbids silent failures. If a JSON file violates a schema, or an HTML template is missing, the engine will halt and throw a descriptive error, ensuring corrupted worksheets are never sent to print.
