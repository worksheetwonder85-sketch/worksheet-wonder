/* Worksheet Wonder — repositories/worksheets-repository.js */
(function (global) {
    'use strict';
    function WorksheetsRepository() {
        global.BaseRepository.call(this, new global.JsonAdapter());
    }
    WorksheetsRepository.prototype = Object.create(global.BaseRepository.prototype);
    WorksheetsRepository.prototype.constructor = WorksheetsRepository;
    WorksheetsRepository.prototype.popular = function (limit) {
        return this.all({ limit: limit || 12 }).then(function (list) {
            return list.slice().sort(function (a, b) { return b.downloads - a.downloads; });
        });
    };
    global.WorksheetsRepository = WorksheetsRepository;
    global.worksheetsRepository = new WorksheetsRepository();
})(window);
