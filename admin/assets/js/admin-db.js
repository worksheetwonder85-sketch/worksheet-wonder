/*==================================================
  Worksheet Wonder - Admin CMS Data Access Layer
  Modular Adapter (Abstracted for future Firebase/Supabase migration)
==================================================*/

class AdminDatabaseAdapter {
    constructor() {
        this.cache = new Map();
    }

    // Generic Fetcher
    async fetchCollection(collectionName) {
        if (this.cache.has(collectionName)) {
            return this.cache.get(collectionName);
        }

        try {
            const res = await fetch(`../database/data/${collectionName}.json`);
            if (!res.ok) throw new Error(`HTTP error ${res.status}`);
            const data = await res.json();
            this.cache.set(collectionName, data);
            return data;
        } catch (err) {
            console.error(`Error loading collection ${collectionName}:`, err);
            return [];
        }
    }

    // Dynamic Database Stats Engine
    async getDatabaseStats() {
        const [worksheets, grades, subjects, topics, subtopics, worksheetTypes, products, bundles, blogPosts] = await Promise.all([
            this.fetchCollection("worksheets"),
            this.fetchCollection("grades"),
            this.fetchCollection("subjects"),
            this.fetchCollection("topics"),
            this.fetchCollection("subtopics"),
            this.fetchCollection("worksheet-types"),
            this.fetchCollection("products"),
            this.fetchCollection("bundles"),
            this.fetchCollection("blog_posts")
        ]);

        return {
            worksheetsCount: worksheets.length,
            gradesCount: grades.length,
            subjectsCount: subjects.length,
            topicsCount: topics.length,
            subtopicsCount: subtopics.length,
            collectionsCount: worksheetTypes.length,
            productsCount: products.length,
            bundlesCount: bundles.length,
            blogPostsCount: blogPosts.length
        };
    }

    // CRUD Methods (Soft Delete & In-Memory Mutation Simulation)
    async getWorksheets(filters = {}, page = 1, pageSize = 10) {
        let worksheets = await this.fetchCollection("worksheets");

        // Filter out soft-deleted items
        worksheets = worksheets.filter(w => !w.is_deleted);

        if (filters.search) {
            const term = filters.search.toLowerCase();
            worksheets = worksheets.filter(w => 
                w.title.toLowerCase().includes(term) || 
                (w.description && w.description.toLowerCase().includes(term))
            );
        }

        if (filters.grade && filters.grade !== "All") {
            worksheets = worksheets.filter(w => w.grade === filters.grade);
        }

        if (filters.subject && filters.subject !== "All") {
            worksheets = worksheets.filter(w => w.subject === filters.subject);
        }

        const totalItems = worksheets.length;
        const totalPages = Math.ceil(totalItems / pageSize) || 1;
        const startIndex = (page - 1) * pageSize;
        const paginated = worksheets.slice(startIndex, startIndex + pageSize);

        return {
            data: paginated,
            totalItems,
            totalPages,
            currentPage: page
        };
    }

    // Save/Update Worksheet Record
    async saveWorksheet(record) {
        const worksheets = await this.fetchCollection("worksheets");
        const existingIndex = worksheets.findIndex(w => String(w.id) === String(record.id));

        if (existingIndex >= 0) {
            worksheets[existingIndex] = { ...worksheets[existingIndex], ...record, updated_at: new Date().toISOString() };
        } else {
            const newId = worksheets.length > 0 ? Math.max(...worksheets.map(w => parseInt(w.id) || 0)) + 1 : 1;
            const newRecord = { id: newId, created_at: new Date().toISOString(), ...record };
            worksheets.push(newRecord);
        }

        this.cache.set("worksheets", worksheets);
        return true;
    }

    // Soft Delete Record
    async softDeleteWorksheet(id) {
        const worksheets = await this.fetchCollection("worksheets");
        const record = worksheets.find(w => String(w.id) === String(id));
        if (record) {
            record.is_deleted = true;
            this.cache.set("worksheets", worksheets);
            return true;
        }
        return false;
    }
}

// Global Admin DB Singleton
window.adminDb = new AdminDatabaseAdapter();
