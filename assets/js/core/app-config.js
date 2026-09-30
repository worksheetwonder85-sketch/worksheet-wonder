/* Worksheet Wonder — core/app-config.js */
(function (global) {
    'use strict';
    global.AppConfig = {
        appName: 'Worksheet Wonder',
        version: '2.0.0',
        currency: 'USD',
        apiBase: '/api',
        cacheTtlMs: 10 * 60 * 1000
    };
})(window);
