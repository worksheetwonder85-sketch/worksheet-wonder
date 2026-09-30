/* ============================================================
   Worksheet Wonder — subject-hub.js
   Powers subject.html and subject-*.html (shared template).
   Detects the subject from the page filename and renders hero,
   stats, topics, worksheets, resources and blog grids.
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

    // subject-maths.html -> mathematics, subject-art-craft.html -> art-craft
    var FILE_TO_SLUG = {
        'subject-maths': 'mathematics',
        'subject-english': 'english',
        'subject-science': 'science',
        'subject-evs': 'evs',
        'subject-computer': 'computer',
        'subject-art-craft': 'art-craft',
        'subject-gk': 'gk'
    };

    /* K5's exact math tab topic grouping (mathematics only).
       Only slugs that exist in DB.topics are rendered. */
    var K5_MATH_GROUPS = [
        { name: 'Numbers', slugs: ['numbers', 'counting', 'comparing-numbers', 'place-value', 'rounding', 'roman-numerals', 'number-patterns'] },
        { name: 'Fractions & Decimals', slugs: ['fractions', 'decimals'] },
        { name: '4 Operations', slugs: ['addition', 'subtraction', 'multiplication', 'division', 'order-of-operations', 'math-drills'] },
        { name: 'Measurement', slugs: ['measurement', 'money', 'time'] },
        { name: 'Advanced', slugs: ['factoring', 'exponents', 'proportions', 'percents', 'integers', 'algebra'] },
        { name: 'More', slugs: ['geometry', 'shapes', 'data-graphing', 'word-problems', 'comparing-sorting'] }
    ];

    onReady(function () {
        if (!window.WWDatabase || !window.WW) return;
        var DB = window.WWDatabase;

        var page = (location.pathname.split('/').pop() || 'subject.html').split('?')[0].toLowerCase().replace('.html', '');
        var subject = DB.getSubjectBySlug(FILE_TO_SLUG[page] || '');

        if (subject) {
            document.title = subject.name + ' Worksheets | Worksheet Wonder';
            setText('subject-hero-grade-badge', subject.emoji + ' ' + subject.name);
            setText('subject-hero-title', subject.name + ' Worksheets');
            setText('subject-hero-desc', subject.desc + ' Explore topics and printable worksheets below.');
            var crumb = document.getElementById('subject-breadcrumb');
            if (crumb) {
                var items = crumb.querySelectorAll('.breadcrumb-item');
                if (items.length) items[items.length - 1].textContent = subject.name;
            }
        }

        var worksheets = subject ? DB.getWorksheets({ subject: subject.slug, limit: 8 }) : DB.getWorksheets({ limit: 8 });

        setText('stat-subject-topics', String(DB.topics.length));
        setText('stat-subject-worksheets', String(worksheets.length * 12 + 80));
        setText('stat-subject-bundles', String(DB.getProducts().length + 2));

        var tg = document.getElementById('subject-topics-grid');
        if (tg) {
            // Only topics that actually have worksheets for this subject,
            // grouped K5-style (e.g. Math: Numbers, 4 Operations, Measurement…)
            var subjTopics = DB.topics.filter(function (t) {
                return !subject || DB.getWorksheets({ subject: subject.slug, topic: t.slug, limit: 1 }).length > 0;
            });
            var gradeOrder = {};
            DB.getGrades().forEach(function (g, i) { gradeOrder[g.slug] = i; });
            function topicMeta(t) {
                var ws = DB.getWorksheets({ subject: subject ? subject.slug : undefined, topic: t.slug, limit: 10000 });
                var grades = ws.map(function (w) { return w.grade; })
                    .filter(function (g, i, a) { return a.indexOf(g) === i; })
                    .sort(function (a, b) { return (gradeOrder[a] || 0) - (gradeOrder[b] || 0); });
                var names = grades.map(function (g) { var gr = DB.getGradeBySlug(g); return gr ? gr.name : g; });
                var range = names.length > 1 ? names[0] + '–' + names[names.length - 1] : (names[0] || '');
                return { count: ws.length, range: range };
            }
            var groups = [];
            if (subject && subject.slug === 'mathematics') {
                /* K5's exact math grouping; only topics present in the DB. */
                var bySlug = {};
                subjTopics.forEach(function (t) { bySlug[t.slug] = t; });
                K5_MATH_GROUPS.forEach(function (kg) {
                    var topics = [];
                    kg.slugs.forEach(function (s) { if (bySlug[s]) topics.push(bySlug[s]); });
                    if (topics.length) groups.push({ name: kg.name, topics: topics });
                });
                /* Safety net: any subject topic not covered by the K5 groups. */
                subjTopics.forEach(function (t) {
                    var found = false;
                    groups.forEach(function (g) { if (g.topics.indexOf(t) >= 0) found = true; });
                    if (!found) {
                        var extra = null;
                        for (var i = 0; i < groups.length; i++) {
                            if (groups[i].name === 'More Topics') extra = groups[i];
                        }
                        if (!extra) { extra = { name: 'More Topics', topics: [] }; groups.push(extra); }
                        extra.topics.push(t);
                    }
                });
            } else {
                subjTopics.forEach(function (t) {
                    var gname = t.group || 'Topics';
                    var g = null;
                    for (var i = 0; i < groups.length; i++) if (groups[i].name === gname) g = groups[i];
                    if (!g) { g = { name: gname, topics: [] }; groups.push(g); }
                    g.topics.push(t);
                });
            }
            tg.innerHTML = groups.map(function (g) {
                return '<div class="mb-4"><h3 class="fw-bold mb-3" style="font-size:1.25rem">' + g.name + '</h3>' +
                    '<div class="row">' + g.topics.map(function (t) {
                        var meta = topicMeta(t);
                        var link = 'worksheets.html' + (subject ? '?subject=' + subject.slug : '') + '&topic=' + encodeURIComponent(t.slug);
                        return '<div class="col-6 col-md-4 col-lg-3 mb-3">' +
                            '<a href="' + link + '" class="text-decoration-none text-dark">' +
                            '<div class="ww-card p-3 text-center h-100"><span style="font-size:2rem">' + t.emoji + '</span>' +
                            '<div class="fw-bold mt-2">' + t.name + '</div>' +
                            '<div class="text-muted small mt-1">' + meta.count + ' worksheets' +
                            (meta.range ? ' · ' + meta.range : '') + '</div></div></a></div>';
                    }).join('') + '</div></div>';
            }).join('');
            /* K5-style bottom link chips for the math tab. (No Math Flashcards chip:
               the DB has no flashcards topic and worksheets.html supports no search param.) */
            if (subject && subject.slug === 'mathematics' && tg.parentNode) {
                var chips = document.createElement('div');
                chips.className = 'mt-2 mb-4';
                chips.innerHTML = '<a href="worksheets.html?topic=math-drills" class="btn btn-outline-secondary m-1">Math Drills</a>';
                tg.parentNode.appendChild(chips);
            }
        }

        // K5-style: "browse by grade" row above the topics (only grades with worksheets)
        if (subject && tg) {
            var gradeChips = DB.getGrades().filter(function (g) {
                return DB.getWorksheets({ subject: subject.slug, grade: g.slug, limit: 1 }).length > 0;
            });
            var tsec = tg.closest ? tg.closest('section') : null;
            if (tsec && gradeChips.length) {
                var gsec = document.createElement('section');
                gsec.className = 'py-5 bg-white';
                gsec.innerHTML = '<div class="container"><h2 class="fw-bold mb-4">Browse by Grade</h2><div class="row">' +
                    gradeChips.map(function (g) {
                        var link = 'worksheets.html?subject=' + subject.slug + '&grade=' + g.slug;
                        return '<div class="col-6 col-md-4 col-lg-3 mb-3">' +
                            '<a href="' + link + '" class="text-decoration-none text-dark">' +
                            '<div class="ww-card p-3 text-center h-100"><span style="font-size:2rem">🎓</span>' +
                            '<div class="fw-bold mt-2">' + g.name + '</div></div></a></div>';
                    }).join('') + '</div></div>';
                tsec.parentNode.insertBefore(gsec, tsec);
            }
        }

        var wg = document.getElementById('subject-worksheets-grid');
        if (wg) {
            wg.innerHTML = worksheets.length ? worksheets.map(window.WW.worksheetCard).join('') : '';
            if (!worksheets.length) window.WW.emptyState(wg);
        }

        var rg = document.getElementById('subject-resources-grid');
        if (rg) {
            rg.innerHTML = DB.getProducts().slice(0, 3).map(function (p) {
                return '<div class="col-md-4 mb-4">' +
                    '<div class="bundle-card d-flex flex-column h-100">' +
                    '<img src="' + p.thumb + '" alt="' + p.title.replace(/"/g, '') + '" loading="lazy" onerror="this.style.display=\'none\'">' +
                    '<div class="p-3"><h5 class="fw-bold">' + p.title + '</h5>' +
                    '<div><span class="price">$' + p.price.toFixed(2) + '</span></div>' +
                    '<a href="shop.html" class="btn btn-rainbow btn-sm mt-2">View in Shop</a></div>' +
                    '</div></div>';
            }).join('');
        }

        var bg = document.getElementById('subject-blog-grid');
        if (bg) {
            bg.innerHTML = DB.getArticles().slice(0, 3).map(function (a) {
                return '<div class="col-md-4 mb-4">' +
                    '<div class="blog-card d-flex flex-column h-100">' +
                    '<img src="' + a.img + '" alt="' + a.title.replace(/"/g, '') + '" loading="lazy" onerror="this.style.display=\'none\'">' +
                    '<div class="p-3"><span class="badge bg-light text-primary mb-2">' + a.category + '</span>' +
                    '<h6 class="fw-bold">' + a.title + '</h6>' +
                    '<a href="blog.html" class="btn btn-link btn-sm p-0">Read article →</a></div>' +
                    '</div></div>';
            }).join('');
        }
    });
})();
