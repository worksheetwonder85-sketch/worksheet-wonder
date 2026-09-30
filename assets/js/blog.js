/* Worksheet Wonder — blog.js (blog.html) */
(function () {
    'use strict';
    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }
    onReady(function () {
        if (!window.WWDatabase) return;
        var DB = window.WWDatabase;
        var articles = DB.getArticles();

        function articleCard(a) {
            return '<div class="col-md-6 col-lg-4 mb-4">' +
                '<div class="blog-card d-flex flex-column h-100">' +
                '<a href="blog-single.html?id=' + a.id + '"><img src="' + a.img + '" alt="' + a.title.replace(/"/g, '') + '" loading="lazy" onerror="this.style.display=\'none\'"></a>' +
                '<div class="p-3 d-flex flex-column flex-grow-1">' +
                '<div class="blog-meta mb-2"><span class="badge bg-light text-primary">' + a.category + '</span> <span class="ms-2">📅 ' + a.date + ' · ' + a.readTime + '</span></div>' +
                '<h5 class="fw-bold"><a href="blog-single.html?id=' + a.id + '" class="text-decoration-none text-dark">' + a.title + '</a></h5>' +
                '<p class="text-muted small flex-grow-1">' + a.excerpt + '</p>' +
                '<a href="blog-single.html?id=' + a.id + '" class="text-primary fw-bold small text-decoration-none">Read article →</a>' +
                '</div></div></div>';
        }

        var feat = document.getElementById('blog-featured-article');
        if (feat && articles.length) {
            var a = articles[0];
            feat.innerHTML = '<div class="blog-card mb-4"><div class="row g-0">' +
                '<div class="col-md-6"><img src="' + a.img + '" class="w-100 h-100" style="object-fit:cover;min-height:260px" alt="' + a.title.replace(/"/g, '') + '" onerror="this.style.display=\'none\'"></div>' +
                '<div class="col-md-6 p-4 d-flex flex-column justify-content-center">' +
                '<span class="badge bg-primary mb-2 align-self-start">Featured</span>' +
                '<h3 class="fw-bold"><a href="blog-single.html?id=' + a.id + '" class="text-decoration-none text-dark">' + a.title + '</a></h3>' +
                '<p class="text-muted">' + a.excerpt + '</p>' +
                '<div class="blog-meta mb-3">📅 ' + a.date + ' · ' + a.readTime + '</div>' +
                '<a href="blog-single.html?id=' + a.id + '" class="btn btn-primary align-self-start">Read Full Article <i class="bi bi-arrow-right ms-1"></i></a>' +
                '</div></div></div>';
        }

        var grid = document.getElementById('blog-articles-grid');
        if (grid) grid.innerHTML = articles.slice(1).map(articleCard).join('');

        var cats = document.getElementById('blog-categories-list');
        if (cats) {
            var seen = {};
            articles.forEach(function (a) { seen[a.category] = (seen[a.category] || 0) + 1; });
            cats.innerHTML = Object.keys(seen).map(function (c) {
                return '<button class="list-group-item list-group-item-action d-flex justify-content-between align-items-center blog-category" data-cat="' + c + '">' +
                    c + '<span class="badge bg-primary rounded-pill">' + seen[c] + '</span></button>';
            }).join('');
            cats.querySelectorAll('[data-cat]').forEach(function (b) {
                b.addEventListener('click', function () {
                    cats.querySelectorAll('.blog-category').forEach(function (x) { x.classList.remove('active'); });
                    b.classList.add('active');
                    var cat = b.getAttribute('data-cat');
                    var list = articles.filter(function (a) { return a.category === cat; });
                    if (grid) grid.innerHTML = list.map(articleCard).join('');
                    if (feat) feat.style.display = 'none';
                });
            });
        }
    });
})();
