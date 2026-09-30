/* Worksheet Wonder — services/recommendation-engine.js */
(function (global) {
    'use strict';
    global.recommendationEngine = {
        getPersonalizedRecommendations: function (user, limit) {
            limit = limit || 3;
            var DB = global.WWDatabase;
            if (!DB) return Promise.resolve([]);
            var seen = {};
            (user && user.download_history || []).forEach(function (d) { seen[d.worksheet_id] = true; });
            (user && user.favorites || []).forEach(function (id) { seen[id] = true; });
            var pool = DB.getWorksheets({ limit: 40 }).filter(function (w) { return !seen[w.id]; });
            pool.sort(function (a, b) { return b.rating - a.rating; });
            var picks = pool.slice(0, limit).map(function (w) {
                var g = DB.getGradeBySlug(w.grade);
                return { id: w.id, title: w.title, thumbnail: w.thumb, grade: g ? g.name : '' };
            });
            return Promise.resolve(picks);
        }
    };
})(window);
