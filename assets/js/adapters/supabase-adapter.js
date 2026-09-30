/*==================================================
  Worksheet Wonder - Future Supabase PostgreSQL Adapter Stub
==================================================*/

class SupabaseDataAdapter extends BaseDataAdapter {
    constructor() {
        super();
        window.AppLogger.info("SupabaseDataAdapter initialized stub (Ready for connection).");
    }

    async findAll(resourceName) {
        window.AppLogger.info(`[Supabase Stub] supabase.from('${resourceName}').select('*')`);
        return [];
    }

    async findById(resourceName, id) { return null; }
    async findByQuery(resourceName, queryObj) { return []; }
    async create(resourceName, data) { return data; }
    async update(resourceName, id, data) { return data; }
    async delete(resourceName, id) { return true; }
}

window.SupabaseDataAdapter = SupabaseDataAdapter;
