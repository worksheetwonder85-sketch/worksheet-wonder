/* Worksheet Wonder — worksheets-data.js (worksheets.html listing) */
(function () {
    'use strict';
    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }
    function params() {
        var p = {};
        location.search.replace(/^\?/, '').split('&').forEach(function (kv) {
            var parts = kv.split('=');
            if (parts[0]) p[decodeURIComponent(parts[0])] = decodeURIComponent(parts[1] || '');
        });
        return p;
    }
    onReady(function () {
        var loading = document.getElementById('worksheets-loading');
        var errBox = document.getElementById('worksheets-error');
        function finishLoading() {
            if (loading) loading.style.display = 'none';
        }
        function showError() {
            finishLoading();
            if (errBox) errBox.classList.remove('d-none');
        }
        if (!window.WWDatabase || !window.WW) { showError(); return; }
        var DB = window.WWDatabase;
        var grid = document.getElementById('worksheets-grid');
        if (!grid) { finishLoading(); return; }
        var q = params();
        var input = document.getElementById('search-input');
        var moreBtn = document.getElementById('load-more-btn');
        var STEP = 24, shown = STEP;

        function activeLevel() {
            var lv = String(q.level || '').toLowerCase();
            return (lv === 'easy' || lv === 'medium' || lv === 'hard') ? lv : '';
        }

        function currentFilters() {
            return {
                grade: q.grade || '',
                subject: q.subject || '',
                topic: q.topic || '',
                limit: activeLevel() ? 10000 : 1000
            };
        }

        function render() {
            var all = DB.searchWorksheets(input ? input.value : '', currentFilters());
            var lv = activeLevel();
            if (lv) {
                all = all.filter(function (w) { return String(w.level || '').toLowerCase() === lv; });
            }
            var list = all.slice(0, shown);
            var title = document.getElementById('results-title');
            if (title) {
                var bits = [];
                if (q.grade) { var g = DB.getGradeBySlug(q.grade); if (g) bits.push(g.name); }
                if (q.subject) { var s = DB.getSubjectBySlug(q.subject); if (s) bits.push(s.name); }
                if (lv) bits.push(lv.charAt(0).toUpperCase() + lv.slice(1));
                title.textContent = bits.length ? bits.join(' · ') + ' Worksheets' : 'All Worksheets';
            }
            var count = document.getElementById('results-count');
            if (count) count.textContent = all.length ?
                'Showing ' + list.length + ' of ' + all.length + ' worksheets' : '';
            grid.classList.remove('d-none');
            grid.innerHTML = list.length ? list.map(window.WW.worksheetCard).join('') : '';
            if (!list.length) window.WW.emptyState(grid, 'No worksheets match your filters yet.');
            if (moreBtn) moreBtn.style.display = all.length > shown ? '' : 'none';
            finishLoading();
        }

        if (moreBtn) {
            moreBtn.addEventListener('click', function () {
                shown += STEP;
                render();
            });
        }

        if (input) {
            if (q.q) input.value = q.q;
            var t;
            input.addEventListener('input', function () {
                clearTimeout(t);
                t = setTimeout(function () {
                    shown = STEP;
                    render();
                }, 250);
            });
        }

        var levelSel = document.getElementById('level-filter');
        if (levelSel) {
            var curLevel = activeLevel();
            if (curLevel) levelSel.value = curLevel;
            levelSel.addEventListener('change', function () {
                var p = params();
                if (levelSel.value) p.level = levelSel.value; else delete p.level;
                var qs = Object.keys(p).map(function (k) {
                    return encodeURIComponent(k) + '=' + encodeURIComponent(p[k]);
                }).join('&');
                location.href = location.pathname + (qs ? '?' + qs : '');
            });
        }

        render();
    });
})();
