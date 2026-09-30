/*==================================================
  Worksheet Wonder
  Content Production Engine & Bulk Import/Export System
==================================================*/

class ContentProductionEngine {
    constructor() {
        this.records = [];
        this.healthMetrics = {
            totalWorksheets: 0,
            drafts: 0,
            published: 0,
            missingSeo: 0,
            missingPdfs: 0,
            missingImages: 0,
            duplicates: 0
        };
    }

    // STEP 1: BULK IMPORT MODULE (JSON & CSV Parser)
    async importBulkJSON(jsonString) {
        try {
            const data = typeof jsonString === 'string' ? JSON.parse(jsonString) : jsonString;
            if (!Array.isArray(data)) throw new Error("Import payload must be a JSON array.");

            let importedCount = 0;
            let errors = [];

            for (const item of data) {
                const validation = this.validateRecord(item);
                if (validation.isValid) {
                    item.status = item.status || "Draft";
                    item.slug = item.slug || this.generateSlug(item.title);
                    item.seo = item.seo || this.generateAutoSEO(item);
                    await window.WorksheetsRepository.create(item);
                    importedCount++;
                } else {
                    errors.push({ item: item.title || 'Untitled', errors: validation.errors });
                }
            }

            return { success: true, importedCount, errors };
        } catch (err) {
            return { success: false, error: err.message };
        }
    }

    // STEP 2: BULK EXPORT MODULE
    async exportCollectionToJSON(resourceName = "worksheets") {
        const repo = new window.BaseRepository(resourceName);
        const data = await repo.getAll();
        return JSON.stringify(data, null, 2);
    }

    async exportCollectionToCSV(resourceName = "worksheets") {
        const repo = new window.BaseRepository(resourceName);
        const data = await repo.getAll();
        if (data.length === 0) return "";

        const headers = Object.keys(data[0]);
        const csvRows = [headers.join(",")];

        data.forEach(item => {
            const values = headers.map(header => {
                const val = item[header] !== undefined ? item[header] : "";
                return `"${String(val).replace(/"/g, '""')}"`;
            });
            csvRows.push(values.join(","));
        });

        return csvRows.join("\n");
    }

    // STEP 3 & 9: CONTENT VALIDATION & DUPLICATE DETECTION
    validateRecord(record) {
        const errors = [];
        if (!record.title) errors.push("Missing title");
        if (!record.grade) errors.push("Missing grade assignment");
        if (!record.subject) errors.push("Missing subject assignment");

        return {
            isValid: errors.length === 0,
            errors
        };
    }

    async scanContentHealth() {
        const worksheets = await window.WorksheetService.fetchAllWorksheets();
        this.healthMetrics = {
            totalWorksheets: worksheets.length,
            drafts: 0,
            published: 0,
            missingSeo: 0,
            missingPdfs: 0,
            missingImages: 0,
            duplicates: 0
        };

        const slugs = new Set();

        worksheets.forEach(w => {
            if (w.status === "Draft") this.healthMetrics.drafts++;
            else this.healthMetrics.published++;

            if (!w.seo || !w.seo.meta_title) this.healthMetrics.missingSeo++;
            if (!w.file_path || w.file_path === "#") this.healthMetrics.missingPdfs++;
            if (!w.thumbnail) this.healthMetrics.missingImages++;

            if (slugs.has(w.slug)) this.healthMetrics.duplicates++;
            else if (w.slug) slugs.add(w.slug);
        });

        return this.healthMetrics;
    }

    // STEP 4: AUTO SLUG GENERATION
    generateSlug(title) {
        if (!title) return "worksheet-" + Date.now();
        return title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
    }

    // STEP 5: AUTO SEO GENERATION
    generateAutoSEO(record) {
        const title = record.title || "Printable Worksheet";
        const grade = record.grade || "Elementary";
        const subject = record.subject || "Learning";

        return {
            meta_title: `${title} | ${grade} ${subject} Worksheet`,
            meta_description: `Download free printable ${title} worksheet for ${grade} ${subject}. High quality PDF with answer key included.`,
            canonical: `https://worksheetwonder.com/worksheet-details.html?id=${record.id || '1'}`,
            og_title: `${title} - Worksheet Wonder`,
            og_description: `Printable ${title} learning activity for ${grade} students.`
        };
    }

    // STEP 7: BULK OPERATIONS
    async bulkUpdateStatus(ids, newStatus) {
        const worksheets = await window.WorksheetService.fetchAllWorksheets();
        let updatedCount = 0;

        for (const w of worksheets) {
            if (ids.includes(String(w.id))) {
                w.status = newStatus;
                await window.WorksheetsRepository.update(w.id, w);
                updatedCount++;
            }
        }
        return updatedCount;
    }
}

// Global Content Engine Singleton
window.contentEngine = new ContentProductionEngine();
