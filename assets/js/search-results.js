/* Worksheet Wonder — search-results.js
   Compatibility shim: rendering lives in search-engine.js.
   This file re-applies the last search if loaded separately. */
(function () {
    'use strict';
    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }
    onReady(function () {
        // search-engine.js owns the search lifecycle; nothing extra needed here.
        if (window.WWSearch && typeof window.WWSearch.search === 'function') {
            window.WWSearch.search();
        }
    });
})();
