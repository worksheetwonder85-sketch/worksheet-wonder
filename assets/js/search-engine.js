/* Worksheet Wonder — search-engine.js + search-results.js (search.html)
   search-engine.js: builds filter dropdowns + runs queries.
   search-results.js: renders result cards into the grid. */
(function () {
    'use strict';
    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }

    /* ---------- Engine: filter options + query execution ---------- */
    function fillSelect(id, options, label) {
        var el = document.getElementById(id);
        if (!el) return;
        el.innerHTML = '<option value="">' + label + '</option>' + options.map(function (o) {
            return '<option value="' + o.value + '">' + o.label + '</option>';
        }).join('');
    }

    var Engine = {
        filters: { grade: '', subject: '', type: '', difficulty: '', sort: 'popular', access: '' },
        run: function (query) {
            if (!window.WWDatabase) return [];
            var DB = window.WWDatabase;
            var list = DB.searchWorksheets(query || '', {
                grade: this.filters.grade,
                subject: this.filters.subject,
                limit: 500
            });
            if (this.filters.access === 'free') list = list.filter(function (w) { return w.price === 0; });
            if (this.filters.access === 'premium') list = list.filter(function (w) { return w.price > 0; });
            if (this.filters.sort === 'rating') list.sort(function (a, b) { return b.rating - a.rating; });
            else if (this.filters.sort === 'az') list.sort(function (a, b) { return a.title.localeCompare(b.title); });
            else list.sort(function (a, b) { return b.downloads - a.downloads; });
            return list;
        }
    };

    /* ---------- Results renderer ---------- */
    function renderResults(list, query) {
        var grid = document.getElementById('search-results-grid');
        if (!grid) return;
        var title = document.getElementById('search-query-title');
        var count = document.getElementById('search-total-count');
        if (title) title.textContent = query ? 'Results for "' + query + '"' : 'Browse worksheets';
        if (count) count.textContent = list.length + ' found';
        if (!window.WW) return;
        grid.innerHTML = list.length ? list.map(window.WW.worksheetCard).join('') : '';
        if (!list.length) window.WW.emptyState(grid, 'Try different keywords or clear the filters.');
    }

    onReady(function () {
        if (!window.WWDatabase) return;
        var DB = window.WWDatabase;

        fillSelect('search-filter-grade', DB.getGrades().map(function (g) { return { value: g.slug, label: g.name }; }), 'All Grades');
        fillSelect('search-filter-subject', DB.getSubjects().map(function (s) { return { value: s.slug, label: s.name }; }), 'All Subjects');
        fillSelect('search-filter-type', [{ value: 'worksheet', label: 'Worksheet' }, { value: 'bundle', label: 'Bundle' }], 'All Types');
        fillSelect('search-filter-difficulty', [{ value: 'easy', label: 'Easy' }, { value: 'medium', label: 'Medium' }, { value: 'hard', label: 'Hard' }], 'Any Difficulty');
        fillSelect('search-filter-sort', [{ value: 'popular', label: 'Most Popular' }, { value: 'rating', label: 'Top Rated' }, { value: 'az', label: 'A to Z' }], 'Sort by');
        fillSelect('search-filter-access', [{ value: 'free', label: 'Free' }, { value: 'premium', label: 'Premium' }], 'Free & Premium');

        var input = document.getElementById('search-page-input');
        var btn = document.getElementById('search-page-btn');

        function doSearch() {
            ['grade', 'subject', 'type', 'difficulty', 'sort', 'access'].forEach(function (k) {
                var el = document.getElementById('search-filter-' + k);
                if (el) Engine.filters[k] = el.value;
            });
            var q = input ? input.value.trim() : '';
            renderResults(Engine.run(q), q);
        }

        ['grade', 'subject', 'type', 'difficulty', 'sort', 'access'].forEach(function (k) {
            var el = document.getElementById('search-filter-' + k);
            if (el) el.addEventListener('change', doSearch);
        });
        if (btn) btn.addEventListener('click', doSearch);
        if (input) input.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); doSearch(); } });

        // Initial: honor ?q= param, else show popular
        var m = location.search.match(/[?&]q=([^&]+)/);
        if (m && input) input.value = decodeURIComponent(m[1]);
        doSearch();

        window.WWSearch = { engine: Engine, render: renderResults, search: doSearch };
    });
})();
