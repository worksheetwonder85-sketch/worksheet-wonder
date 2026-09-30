/* Worksheet Wonder — core/logger.js */
(function (global) {
    'use strict';
    var LEVELS = { debug: 0, info: 1, warn: 2, error: 3 };
    var current = 'info';
    function log(level, args) {
        if (LEVELS[level] >= LEVELS[current]) {
            var fn = console[level] || console.log;
            fn.apply(console, ['[WW][' + level + ']'].concat(args));
        }
    }
    global.Logger = {
        setLevel: function (l) { if (LEVELS[l] !== undefined) current = l; },
        debug: function () { log('debug', [].slice.call(arguments)); },
        info: function () { log('info', [].slice.call(arguments)); },
        warn: function () { log('warn', [].slice.call(arguments)); },
        error: function () { log('error', [].slice.call(arguments)); }
    };
})(window);
