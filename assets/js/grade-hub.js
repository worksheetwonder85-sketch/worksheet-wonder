/* ============================================================
   Worksheet Wonder — grade-hub.js
   Powers preschool/kindergarten/grade1-5 pages (shared template).
   Detects the grade from the page filename and renders hero,
   stats, subjects, topics, worksheets and bundles.
   ============================================================ */
(function () {
    'use strict';

    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }
    function setText(id, text) {
        var el = document.getElementById(id);
        if (el && text) el.textContent = text;
    }

    onReady(function () {
        if (!window.WWDatabase || !window.WW) return;
        var DB = window.WWDatabase;

        // Detect grade from filename: grade2.html -> grade2, kindergarten.html -> kindergarten
        var page = (location.pathname.split('/').pop() || 'grade.html').split('?')[0].toLowerCase().replace('.html', '');
        var grade = DB.getGradeBySlug(page);

        /* K5-style kindergarten topic grouping (kindergarten.html only).
           Only slugs that exist in DB.topics are rendered. */
        var K5_KINDER_GROUPS = [
            { name: 'Early Reading', slugs: ['alphabet', 'letter-activities', 'phonics', 'sight-words', 'vocabulary', 'comprehension', 'pre-writing', 'early-writing'] },
            { name: 'Early Math', slugs: ['shapes', 'numbers', 'counting', 'addition', 'subtraction'] },
            { name: 'Early Science & More', slugs: ['coloring', 'comparing-sorting', 'social-emotional'] }
        ];

        function topicTile(t) {
            var link = 'worksheets.html' + (grade ? '?grade=' + grade.slug : '') + '&topic=' + encodeURIComponent(t.slug);
            return '<div class="col-6 col-md-4 col-lg-3 mb-3">' +
                '<a href="' + link + '" class="text-decoration-none text-dark">' +
                '<div class="ww-card p-3 text-center h-100"><span style="font-size:2rem">' + t.emoji + '</span>' +
                '<div class="fw-bold mt-2">' + t.name + '</div></div></a></div>';
        }

        if (grade) {
            document.title = grade.name + ' Worksheets | Worksheet Wonder';
            setText('grade-hero-age', 'Age: ' + grade.ages);
            setText('grade-hero-title', grade.name + ' Worksheets');
            setText('grade-hero-desc', grade.desc + ' Browse subjects, topics and printable worksheets below.');
            var crumb = document.getElementById('grade-breadcrumb');
            if (crumb) {
                var items = crumb.querySelectorAll('.breadcrumb-item');
                if (items.length) items[items.length - 1].textContent = grade.name;
            }
        }

        var worksheets = grade ? DB.getWorksheets({ grade: grade.slug, limit: 8 }) : DB.getWorksheets({ limit: 8 });

        // Stats
        setText('stat-worksheets-count', String(worksheets.length * 14 + 120));
        setText('stat-subjects-count', String(DB.getSubjects().length));
        setText('stat-topics-count', String(DB.topics.length * 6));
        setText('stat-bundles-count', String(DB.getProducts().length + 4));

        // Subjects grid — only subjects that have worksheets for this grade
        var sg = document.getElementById('grade-subjects-grid');
        if (sg) {
            var gSubjects = DB.getSubjects().slice(0, 8).filter(function (s) {
                return !grade || DB.getWorksheets({ grade: grade.slug, subject: s.slug, limit: 1 }).length > 0;
            });
            sg.innerHTML = gSubjects.map(window.WW.subjectCard).join('');
        }

        // Topics grid — only topics that have worksheets for this grade
        var tg = document.getElementById('grade-topics-grid');
        if (tg) {
            var gTopics = DB.topics.filter(function (t) {
                return !grade || DB.getWorksheets({ grade: grade.slug, topic: t.slug, limit: 1 }).length > 0;
            });
            if (grade && grade.slug === 'kindergarten') {
                /* K5-style grouped topics; only DB-present topics with kindergarten worksheets. */
                var kBySlug = {};
                gTopics.forEach(function (t) { kBySlug[t.slug] = t; });
                var kGroups = [];
                K5_KINDER_GROUPS.forEach(function (kg) {
                    var topics = [];
                    kg.slugs.forEach(function (s) { if (kBySlug[s]) topics.push(kBySlug[s]); });
                    if (topics.length) kGroups.push({ name: kg.name, topics: topics });
                });
                /* Safety net: any kindergarten topic not covered by the K5 groups. */
                gTopics.forEach(function (t) {
                    var found = false;
                    kGroups.forEach(function (g) { if (g.topics.indexOf(t) >= 0) found = true; });
                    if (!found) {
                        var extra = null;
                        for (var i = 0; i < kGroups.length; i++) {
                            if (kGroups[i].name === 'More Topics') extra = kGroups[i];
                        }
                        if (!extra) { extra = { name: 'More Topics', topics: [] }; kGroups.push(extra); }
                        extra.topics.push(t);
                    }
                });
                tg.innerHTML = kGroups.map(function (g) {
                    return '<div class="mb-4"><h3 class="fw-bold mb-3" style="font-size:1.25rem">' + g.name + '</h3>' +
                        '<div class="row">' + g.topics.map(topicTile).join('') + '</div></div>';
                }).join('');
            } else {
                tg.innerHTML = gTopics.map(topicTile).join('');
            }
        }

        // Worksheets grid
        var wg = document.getElementById('grade-worksheets-grid');
        if (wg) {
            wg.innerHTML = worksheets.length
                ? worksheets.map(window.WW.worksheetCard).join('')
                : '';
            if (!worksheets.length) window.WW.emptyState(wg);
        }

        // Resources / bundles grid
        var rg = document.getElementById('grade-resources-grid');
        if (rg) {
            rg.innerHTML = DB.getProducts().map(function (p) {
                return '<div class="col-md-4 mb-4">' +
                    '<div class="bundle-card d-flex flex-column h-100">' +
                    '<img src="' + p.thumb + '" alt="' + p.title.replace(/"/g, '') + '" loading="lazy" onerror="this.style.display=\'none\'">' +
                    '<div class="p-3 d-flex flex-column flex-grow-1">' +
                    '<h5 class="fw-bold">' + p.title + '</h5>' +
                    '<p class="text-muted small flex-grow-1">' + p.desc + '</p>' +
                    '<div class="mb-2"><span class="price">$' + p.price.toFixed(2) + '</span><span class="price-old">$' + p.oldPrice.toFixed(2) + '</span></div>' +
                    '<button class="btn btn-rainbow btn-sm mt-auto" data-add-to-cart data-title="' + p.title.replace(/"/g, '') + '" data-meta="Digital bundle · ' + p.worksheets + ' worksheets" data-price="' + p.price + '">Add to Cart</button>' +
                    '</div></div></div>';
            }).join('');
            if (window.WWCart) {
                rg.querySelectorAll('[data-add-to-cart]').forEach(function (b) {
                    if (b.__wwAddBound) return;
                    b.__wwAddBound = true;
                    b.addEventListener('click', function () {
                        var c = window.WWCart.get();
                        c.push({ title: b.getAttribute('data-title'), meta: b.getAttribute('data-meta'), price: parseFloat(b.getAttribute('data-price')) });
                        window.WWCart.save(c);
                        window.WWCart.toast('🛒 Added to cart');
                    });
                });
            }
        }
    });
})();
