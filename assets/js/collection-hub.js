/* Worksheet Wonder — collection-hub.js / subtopic-hub.js / topic-hub.js
   Generic hub renderer: fills *-worksheets-grid, *-resources-grid,
   *-collections-grid, *-subtopics-grid, *-related-grid and *-blog-grid
   from the built-in catalog. Safe on pages missing any container. */
(function () {
    'use strict';
    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }
    function fill(id, html) {
        var el = document.getElementById(id);
        if (el) el.innerHTML = html;
    }
    onReady(function () {
        if (!window.WWDatabase || !window.WW) return;
        var DB = window.WWDatabase;
        var prefixes = ['collection', 'subtopic', 'topic'];

        prefixes.forEach(function (p) {
            var wg = document.getElementById(p + '-worksheets-grid');
            if (wg) {
                var list = DB.getWorksheets({ limit: 8 });
                wg.innerHTML = list.map(window.WW.worksheetCard).join('');
            }
            var rg = document.getElementById(p + '-resources-grid');
            if (rg) {
                rg.innerHTML = DB.getProducts().map(function (prod) {
                    return '<div class="col-md-4 mb-4"><div class="bundle-card d-flex flex-column h-100">' +
                        '<img src="' + prod.thumb + '" alt="' + prod.title.replace(/"/g, '') + '" loading="lazy" onerror="this.style.display=\'none\'">' +
                        '<div class="p-3"><h5 class="fw-bold">' + prod.title + '</h5>' +
                        '<div><span class="price">$' + prod.price.toFixed(2) + '</span></div>' +
                        '<a href="shop.html" class="btn btn-rainbow btn-sm mt-2">View in Shop</a></div></div></div>';
                }).join('');
            }
            var cg = document.getElementById(p + '-collections-grid');
            if (cg) {
                cg.innerHTML = DB.topics.slice(0, 4).map(function (t) {
                    return '<div class="col-md-6 col-lg-3 mb-4"><div class="ww-card p-4 text-center h-100">' +
                        '<span style="font-size:2.5rem">' + t.emoji + '</span>' +
                        '<h6 class="fw-bold mt-2">' + t.name + ' Collection</h6>' +
                        '<a href="worksheets.html?topic=' + encodeURIComponent(t.slug) + '" class="btn btn-rainbow btn-sm mt-2">Explore</a></div></div>';
                }).join('');
            }
            var stg = document.getElementById(p + '-subtopics-grid');
            if (stg) {
                stg.innerHTML = DB.topics.map(function (t) {
                    return '<div class="col-6 col-md-4 col-lg-3 mb-3">' +
                        '<a href="worksheets.html?topic=' + encodeURIComponent(t.slug) + '" class="text-decoration-none text-dark">' +
                        '<div class="ww-card p-3 text-center h-100"><span style="font-size:2rem">' + t.emoji + '</span>' +
                        '<div class="fw-bold mt-2">' + t.name + '</div></div></a></div>';
                }).join('');
            }
            var rtg = document.getElementById(p + '-related-grid') || document.getElementById(p + '-related-topics-grid');
            if (rtg) {
                rtg.innerHTML = DB.getSubjects().slice(0, 4).map(window.WW.subjectCard).join('');
            }
            var bg = document.getElementById(p + '-blog-grid');
            if (bg) {
                bg.innerHTML = DB.getArticles().slice(0, 3).map(function (a) {
                    return '<div class="col-md-4 mb-4"><div class="blog-card d-flex flex-column h-100">' +
                        '<img src="' + a.img + '" alt="' + a.title.replace(/"/g, '') + '" loading="lazy" onerror="this.style.display=\'none\'">' +
                        '<div class="p-3"><span class="badge bg-light text-primary mb-2">' + a.category + '</span>' +
                        '<h6 class="fw-bold">' + a.title + '</h6>' +
                        '<a href="blog.html" class="btn btn-link btn-sm p-0">Read article →</a></div></div></div>';
                }).join('');
            }
        });
        // Silence unused helper warning in strict environments
        fill('__noop', '');
    });
})();
