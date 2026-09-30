/*==================================================
  Worksheet Wonder - Future Firebase Firestore Adapter Stub
==================================================*/

class FirebaseDataAdapter extends BaseDataAdapter {
    constructor() {
        super();
        window.AppLogger.info("FirebaseDataAdapter initialized stub (Ready for SDK connection).");
    }

    async findAll(resourceName) {
        window.AppLogger.info(`[Firebase Stub] collection('${resourceName}').get()`);
        return [];
    }

    async findById(resourceName, id) {
        window.AppLogger.info(`[Firebase Stub] collection('${resourceName}').doc('${id}').get()`);
        return null;
    }

    async findByQuery(resourceName, queryObj) {
        window.AppLogger.info(`[Firebase Stub] collection('${resourceName}').where(...)`);
        return [];
    }

    async create(resourceName, data) { return data; }
    async update(resourceName, id, data) { return data; }
    async delete(resourceName, id) { return true; }
}

window.FirebaseDataAdapter = FirebaseDataAdapter;
