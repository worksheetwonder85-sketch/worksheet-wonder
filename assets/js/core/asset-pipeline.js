/*==================================================
  Worksheet Wonder
  Worksheet Asset Generation Pipeline (Phase 18)
==================================================*/

class WorksheetAssetPipeline {
    constructor() {
        this.baseStoragePath = "assets/images/worksheets/";
        this.pdfStoragePath = "assets/downloads/pdfs/";
        this.manifestCache = new Map();
    }

    // STEP 1: ASSET MANIFEST GENERATOR
    createAssetManifest(worksheetId, specId, title, version = "1.0.0") {
        const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
        const manifest = {
            worksheet_id: String(worksheetId),
            spec_id: String(specId || `WS-SPEC-${worksheetId}`),
            title: title,
            version: version,
            status: "Waiting for Assets",
            paths: {
                pdf: `${this.pdfStoragePath}${slug}.pdf`,
                answer_key: `${this.pdfStoragePath}${slug}-answer-key.pdf`,
                preview: `${this.baseStoragePath}previews/${slug}-preview.png`,
                thumbnail: `${this.baseStoragePath}thumbnails/${slug}-thumb.png`,
                source: `${this.baseStoragePath}sources/${slug}-source.ai`
            },
            specs: {
                preview_dimensions: "1200x1600 (3:4 Aspect Ratio)",
                thumbnail_dimensions: "400x533",
                pdf_target_pages: 2,
                max_file_size_mb: 2.0
            },
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            version_history: [
                { version: version, timestamp: new Date().toISOString(), notes: "Initial Manifest Created" }
            ]
        };

        this.manifestCache.set(String(worksheetId), manifest);
        window.AppLogger ? window.AppLogger.info(`Asset manifest created for ${worksheetId}`) : console.log(`Asset manifest created for ${worksheetId}`);
        return manifest;
    }

    // STEP 3 & 8: ASSET VALIDATION ENGINE
    async validateAssetPackage(manifest) {
        const issues = [];
        const paths = manifest.paths;

        // Check required fields
        if (!paths.pdf) issues.push("Missing PDF asset path");
        if (!paths.preview) issues.push("Missing preview image path");
        if (!paths.thumbnail) issues.push("Missing thumbnail path");

        const isValid = issues.length === 0;
        return {
            worksheet_id: manifest.worksheet_id,
            status: isValid ? "QA Approved" : "QA Pending",
            isValid,
            issues
        };
    }

    // STEP 4: VERSION MANAGEMENT
    updateAssetVersion(worksheetId, newVersion, changeNotes) {
        const manifest = this.manifestCache.get(String(worksheetId));
        if (!manifest) return null;

        manifest.version = newVersion;
        manifest.updated_at = new Date().toISOString();
        manifest.version_history.push({
            version: newVersion,
            timestamp: new Date().toISOString(),
            notes: changeNotes || "Updated asset version"
        });

        return manifest;
    }

    // STEP 6: PUBLISHING WORKFLOW TRANSITION
    transitionStatus(worksheetId, newStatus) {
        const validStatuses = [
            "Waiting for Assets",
            "Assets Uploaded",
            "QA Pending",
            "QA Approved",
            "Scheduled",
            "Published",
            "Archived"
        ];

        if (!validStatuses.includes(newStatus)) {
            throw new Error(`Invalid status '${newStatus}'`);
        }

        const manifest = this.manifestCache.get(String(worksheetId));
        if (manifest) {
            manifest.status = newStatus;
            manifest.updated_at = new Date().toISOString();
            return manifest;
        }
        return null;
    }

    // STEP 7: BULK ASSET REGENERATION & VALIDATION
    async bulkValidateManifests(manifestList) {
        const results = [];
        for (const m of manifestList) {
            const val = await this.validateAssetPackage(m);
            results.push(val);
        }
        return results;
    }
}

// Global Asset Pipeline Singleton
window.assetPipeline = new WorksheetAssetPipeline();
