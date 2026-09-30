/* Worksheet Wonder — adapters/json-adapter.js
   Serves the built-in WWDatabase catalog through the adapter interface. */
(function (global) {
    'use strict';
    function JsonAdapter() { global.BaseAdapter.call(this); }
    JsonAdapter.prototype = Object.create(global.BaseAdapter.prototype);
    JsonAdapter.prototype.constructor = JsonAdapter;
    JsonAdapter.prototype.list = function (filters) {
        var DB = global.WWDatabase;
        if (!DB) return Promise.resolve([]);
        return Promise.resolve(DB.getWorksheets(filters || {}));
    };
    JsonAdapter.prototype.get = function (id) {
        var DB = global.WWDatabase;
        if (!DB) return Promise.resolve(null);
        return Promise.resolve(DB.getWorksheetById(id));
    };
    global.JsonAdapter = JsonAdapter;
})(window);
