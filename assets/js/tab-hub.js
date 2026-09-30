/* ============================================================
   Worksheet Wonder — tab-hub.js
   Powers the K5-style tab landing pages:
   reading.html, vocabulary.html, spelling.html,
   grammar.html, cursive.html
   Renders hero, browse-by-grade pills, topic groups, sample
   worksheets, bottom links and a workbooks promo from TAB_CONFIG.
   ============================================================ */
(function () {
    'use strict';

    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }
    function setText(id, text) {
        var el = document.getElementById(id);
        if (el && text !== undefined && text !== null) el.textContent = text;
    }
    function setHTML(id, html) {
        var el = document.getElementById(id);
        if (el) el.innerHTML = html;
    }

    /* Tab page configuration, keyed by page filename.
       topicSlugs must exist in DB.topics (verified at runtime; unknown slugs are skipped). */
    var TAB_CONFIG = {
        'reading.html': {
            title: 'Free Reading Worksheets',
            badge: '📖 Reading',
            intro: 'Build strong readers with free printable reading worksheets: phonics, sight words, early reading practice, stories, and reading comprehension for kindergarten through grade 5.',
            subject: 'english',
            showGradePills: true,
            topicGroups: [
                { name: 'Stories', slugs: ['stories-fables'] },
                { name: 'Early Reading', slugs: ['phonics', 'sight-words', 'alphabet', 'letter-activities', 'pre-writing'] },
                { name: 'Reading Comprehension', slugs: ['comprehension', 'comprehension-skills'] }
            ],
            bottomLinks: [
                { label: 'Stories & Fables', href: 'worksheets.html?topic=stories-fables' },
                { label: 'Sight Words', href: 'worksheets.html?topic=sight-words' },
                { label: 'Phonics', href: 'worksheets.html?topic=phonics' }
            ]
        },
        'vocabulary.html': {
            title: 'Free Vocabulary Worksheets',
            badge: '📚 Vocabulary',
            intro: 'Grow word power with free printable vocabulary worksheets: word meanings, shades of meaning, and fun word puzzles for kindergarten through grade 5.',
            subject: 'english',
            showGradePills: true,
            topicGroups: [
                { name: 'Vocabulary', slugs: ['vocabulary'] },
                { name: 'Word Puzzles', slugs: ['crossword-puzzles'] }
            ],
            bottomLinks: [
                { label: 'Vocabulary', href: 'worksheets.html?topic=vocabulary' },
                { label: 'Crossword Puzzles', href: 'worksheets.html?topic=crossword-puzzles' }
            ]
        },
        'spelling.html': {
            title: 'Free Spelling Worksheets',
            badge: '🐝 Spelling',
            intro: 'Master spelling with free printable spelling worksheets: spelling patterns, word lists, and practice activities for grades 1 through 5.',
            subject: 'english',
            showGradePills: true,
            topicGroups: [
                { name: 'Spelling', slugs: ['spelling'] }
            ],
            bottomLinks: [
                { label: 'Spelling', href: 'worksheets.html?topic=spelling' }
            ]
        },
        'grammar.html': {
            title: 'Free Grammar & Writing Worksheets',
            badge: '✍️ Grammar & Writing',
            intro: 'Learn grammar and writing with free printable worksheets: parts of speech, sentences, punctuation, capitalization, and guided writing practice for kindergarten through grade 5.',
            subject: 'english',
            showGradePills: true,
            topicGroups: [
                { name: 'Grammar', slugs: ['grammar', 'verbs', 'adjectives', 'adverbs', 'pronouns'] },
                { name: 'Writing', slugs: ['sentences', 'punctuation', 'capitalization', 'writing', 'early-writing'] }
            ],
            bottomLinks: [
                { label: 'Grammar', href: 'worksheets.html?topic=grammar' },
                { label: 'Writing', href: 'worksheets.html?topic=writing' },
                { label: 'Sentences', href: 'worksheets.html?topic=sentences' }
            ]
        },
        'cursive.html': {
            title: 'Free Cursive Writing Worksheets',
            badge: '✒️ Cursive',
            intro: 'Practice cursive handwriting with free printable worksheets: trace and write the alphabet, individual letters, letter joins, words, sentences, and short passages.',
            subject: 'english',
            showGradePills: false,
            topicGroups: [
                { name: 'Cursive Practice', slugs: ['cursive'] }
            ],
            bottomLinks: [
                { label: 'Cursive', href: 'worksheets.html?topic=cursive' }
            ]
        }
    };

    function topicBySlug(DB, slug) {
        for (var i = 0; i < DB.topics.length; i++) {
            if (DB.topics[i].slug === slug) return DB.topics[i];
        }
        return null;
    }

    /* All worksheets across the tab's topics, de-duplicated by id. */
    function tabWorksheets(DB, slugs, limit) {
        var seen = {}, out = [], i, j;
        for (i = 0; i < slugs.length; i++) {
            var ws = DB.getWorksheets({ topic: slugs[i], limit: limit });
            for (j = 0; j < ws.length; j++) {
                if (!seen[ws[j].id]) { seen[ws[j].id] = true; out.push(ws[j]); }
            }
        }
        return out;
    }

    /* 8 sample worksheets, round-robin across topics for variety. */
    function tabSamples(DB, slugs, limit) {
        var seen = {}, out = [], k, i;
        var lists = slugs.map(function (s) { return DB.getWorksheets({ topic: s, limit: 1000 }); });
        var maxLen = 0;
        for (k = 0; k < lists.length; k++) if (lists[k].length > maxLen) maxLen = lists[k].length;
        for (i = 0; i < maxLen && out.length < limit; i++) {
            for (k = 0; k < lists.length && out.length < limit; k++) {
                var w = lists[k][i];
                if (w && !seen[w.id]) { seen[w.id] = true; out.push(w); }
            }
        }
        return out;
    }

    function topicTile(t, count) {
        var link = 'worksheets.html?topic=' + encodeURIComponent(t.slug);
        return '<div class="col-6 col-md-4 col-lg-3 mb-3">' +
            '<a href="' + link + '" class="text-decoration-none text-dark">' +
            '<div class="ww-card p-3 text-center h-100"><span style="font-size:2rem">' + t.emoji + '</span>' +
            '<div class="fw-bold mt-2">' + t.name + '</div>' +
            '<div class="text-muted small mt-1">' + count + ' worksheets</div></div></a></div>';
    }

    onReady(function () {
        if (!window.WWDatabase || !window.WW) return;
        var DB = window.WWDatabase;

        var page = (location.pathname.split('/').pop() || 'reading.html').split('?')[0].toLowerCase();
        var cfg = TAB_CONFIG[page];
        if (!cfg) return;

        document.title = cfg.title + ' | Worksheet Wonder';
        setText('tab-hero-grade-badge', cfg.badge);
        setText('tab-hero-title', cfg.title);
        setText('tab-hero-desc', cfg.intro);
        var crumb = document.getElementById('tab-breadcrumb');
        if (crumb) {
            var items = crumb.querySelectorAll('.breadcrumb-item');
            if (items.length) items[items.length - 1].textContent =
                cfg.title.replace(/^Free /, '').replace(/ Worksheets$/, '');
        }

        /* Keep only topic slugs that exist in the DB. */
        var validSlugs = [];
        cfg.topicGroups.forEach(function (g) {
            g.slugs.forEach(function (s) {
                if (topicBySlug(DB, s) && validSlugs.indexOf(s) < 0) validSlugs.push(s);
            });
        });

        var allWs = tabWorksheets(DB, validSlugs, 10000);
        setText('stat-tab-topics', String(validSlugs.length));
        setText('stat-tab-worksheets', String(allWs.length));

        /* K5-style "browse by grade" pills — only grades with worksheets in this tab's topics. */
        var gsec = document.getElementById('tab-grade-section');
        if (cfg.showGradePills && gsec) {
            var grades = DB.getGrades().filter(function (g) {
                return validSlugs.some(function (s) {
                    return DB.getWorksheets({ topic: s, grade: g.slug, limit: 1 }).length > 0;
                });
            });
            if (grades.length) {
                setHTML('tab-grade-pills', grades.map(function (g) {
                    var link = 'worksheets.html?subject=' + cfg.subject + '&grade=' + g.slug;
                    return '<div class="col-6 col-md-4 col-lg-3 mb-3">' +
                        '<a href="' + link + '" class="text-decoration-none text-dark">' +
                        '<div class="ww-card p-3 text-center h-100"><span style="font-size:2rem">🎓</span>' +
                        '<div class="fw-bold mt-2">' + g.name + '</div></div></a></div>';
                }).join(''));
            } else if (gsec.parentNode) {
                gsec.parentNode.removeChild(gsec);
            }
        } else if (gsec && gsec.parentNode) {
            gsec.parentNode.removeChild(gsec);
        }

        /* Topic groups with live worksheet counts (skip empty topics). */
        setHTML('tab-topic-groups', cfg.topicGroups.map(function (g) {
            var tiles = g.slugs.map(function (s) {
                var t = topicBySlug(DB, s);
                if (!t) return '';
                var count = DB.getWorksheets({ topic: s, limit: 10000 }).length;
                if (!count) return '';
                return topicTile(t, count);
            }).join('');
            if (!tiles) return '';
            return '<div class="mb-4"><h3 class="fw-bold mb-3" style="font-size:1.25rem">' + g.name + '</h3>' +
                '<div class="row">' + tiles + '</div></div>';
        }).join(''));

        /* Sample worksheets from the tab's topics. */
        var samples = tabSamples(DB, validSlugs, 8);
        var sg = document.getElementById('tab-sample-grid');
        if (sg) {
            sg.innerHTML = samples.length ? samples.map(window.WW.worksheetCard).join('') : '';
            if (!samples.length) window.WW.emptyState(sg);
        }

        /* Bottom link chips. */
        setHTML('tab-bottom-links', cfg.bottomLinks.map(function (l) {
            return '<a href="' + l.href + '" class="btn btn-outline-secondary m-1">' + l.label + '</a>';
        }).join(''));

        /* Workbooks promo card → shop.html. */
        setHTML('tab-workbook-promo',
            '<div class="card border-0 shadow-sm p-4 text-center h-100">' +
            '<div style="font-size:3rem">📚</div>' +
            '<h4 class="fw-bold mt-2">Workbooks</h4>' +
            '<p class="text-muted">Printable workbook bundles with hundreds of ' +
            cfg.title.replace(/^Free /, '').replace(/ Worksheets$/, '').toLowerCase() + ' practice pages.</p>' +
            '<a href="shop.html" class="btn btn-rainbow mt-2">Browse Workbooks</a></div>');
    });
})();
