/* Worksheet Wonder — adapters/base-adapter.js */
(function (global) {
    'use strict';
    function BaseAdapter() {}
    BaseAdapter.prototype.list = function () { return Promise.resolve([]); };
    BaseAdapter.prototype.get = function () { return Promise.resolve(null); };
    global.BaseAdapter = BaseAdapter;
})(window);
