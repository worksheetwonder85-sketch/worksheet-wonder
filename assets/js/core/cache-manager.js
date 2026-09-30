/* Worksheet Wonder — core/cache-manager.js (in-memory + localStorage) */
(function (global) {
    'use strict';
    var mem = {};
    function read(key) {
        if (mem[key] && mem[key].exp > Date.now()) return mem[key].val;
        try {
            var raw = localStorage.getItem('ww_cache_' + key);
            if (!raw) return null;
            var o = JSON.parse(raw);
            if (o.exp > Date.now()) { mem[key] = o; return o.val; }
            localStorage.removeItem('ww_cache_' + key);
        } catch (e) {}
        return null;
    }
    global.CacheManager = {
        get: function (key, loader, ttlMs) {
            var hit = read(key);
            if (hit !== null && hit !== undefined) return Promise.resolve(hit);
            return Promise.resolve(loader()).then(function (val) {
                global.CacheManager.set(key, val, ttlMs);
                return val;
            });
        },
        set: function (key, val, ttlMs) {
            var o = { val: val, exp: Date.now() + (ttlMs || (global.AppConfig && global.AppConfig.cacheTtlMs) || 600000) };
            mem[key] = o;
            try { localStorage.setItem('ww_cache_' + key, JSON.stringify(o)); } catch (e) {}
        },
        clear: function (key) {
            delete mem[key];
            try { localStorage.removeItem('ww_cache_' + key); } catch (e) {}
        }
    };
})(window);
