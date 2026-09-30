/* Worksheet Wonder — repositories/base-repository.js */
(function (global) {
    'use strict';
    function BaseRepository(adapter) { this.adapter = adapter || new global.BaseAdapter(); }
    BaseRepository.prototype.all = function (filters) { return this.adapter.list(filters); };
    BaseRepository.prototype.find = function (id) { return this.adapter.get(id); };
    global.BaseRepository = BaseRepository;
})(window);
