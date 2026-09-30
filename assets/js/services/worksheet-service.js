/* Worksheet Wonder — services/worksheet-service.js */
(function (global) {
    'use strict';
    var repo = null;
    function getRepo() {
        if (!repo && global.WorksheetsRepository) repo = new global.WorksheetsRepository();
        return repo;
    }
    global.WorksheetService = {
        list: function (filters) {
            var r = getRepo();
            if (r) return global.CacheManager.get('ws_list_' + JSON.stringify(filters || {}), function () { return r.all(filters); });
            return Promise.resolve([]);
        },
        get: function (id) {
            var r = getRepo();
            return r ? r.find(id) : Promise.resolve(null);
        },
        popular: function (limit) {
            var r = getRepo();
            return r ? r.popular(limit) : Promise.resolve([]);
        }
    };
})(window);
