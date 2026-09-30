/* ============================================================
   Worksheet Wonder — main.js (shared site behavior)
   Loaded by data-driven pages alongside database.js.
   Safe: every feature guards for missing elements/libs.
   ============================================================ */
(function () {
    'use strict';

    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }

    /* ---------- Card builders (shared by page scripts) ---------- */
    function stars(rating) {
        var full = Math.round(rating || 0), out = '';
        for (var i = 0; i < 5; i++) out += i < full ? '★' : '☆';
        return '<span class="rating" aria-label="Rated ' + rating + ' out of 5">' + out + '</span>';
    }

    /* K5-style listing row: blue underlined title left, thumbnail right, dotted divider */
    function worksheetCard(w) {
        var badge = w.price > 0
            ? '<span class="badge bg-warning text-dark">$' + w.price.toFixed(2) + '</span>'
            : '<span class="badge bg-success">FREE</span>';
        var detailsUrl = 'worksheet-details.html?id=' + w.id;
        var thumb = w.thumb
            ? '<a href="' + detailsUrl + '"><img src="' + w.thumb + '" class="k5-thumb" alt="' +
              w.title.replace(/"/g, '') + '" loading="lazy" onerror="this.style.display=\'none\'"></a>'
            : '';
        return '' +
        '<div class="col-12">' +
            '<div class="k5-listing-row">' +
                '<div class="flex-grow-1">' +
                    '<a class="k5-title" href="' + detailsUrl + '">' + w.title + '</a>' +
                    '<div class="k5-meta mt-1">' + w.pages + ' page' + (w.pages > 1 ? 's' : '') +
                        ' &middot; ' + w.topic + ' &middot; ' + badge + '</div>' +
                    '<div class="mt-1">' + stars(w.rating) +
                        ' <small class="text-muted">' + w.rating.toFixed(1) + '</small></div>' +
                    '<div class="mt-2"><a href="' + detailsUrl +
                        '" class="btn btn-outline-primary btn-sm">View Worksheet</a></div>' +
                '</div>' +
                thumb +
            '</div>' +
        '</div>';
    }

    function subjectCard(s) {
        return '' +
        '<div class="col-md-6 col-lg-3 mb-4">' +
            '<a href="' + s.page + '" class="text-decoration-none text-dark">' +
                '<div class="ww-card category-card d-flex flex-column h-100 p-4 text-center">' +
                    '<span class="card-emoji mx-auto" style="background:' + s.color + '22">' + s.emoji + '</span>' +
                    '<h5 class="fw-bold">' + s.name + '</h5>' +
                    '<p class="text-muted small flex-grow-1">' + s.desc + '</p>' +
                    '<span class="btn btn-rainbow btn-sm mt-auto">Explore</span>' +
                '</div>' +
            '</a>' +
        '</div>';
    }

    function gradeCard(g) {
        return '' +
        '<div class="col-md-6 col-lg-3 mb-4">' +
            '<a href="' + g.slug + '.html" class="text-decoration-none text-dark">' +
                '<div class="ww-card grade-card d-flex flex-column h-100 p-4 text-center">' +
                    '<span class="card-emoji mx-auto" style="background:' + g.color + '22">' + g.emoji + '</span>' +
                    '<h5 class="fw-bold">' + g.name + '</h5>' +
                    '<span class="badge mb-2" style="background:' + g.color + '22;color:' + g.color + '">' + g.ages + '</span>' +
                    '<p class="text-muted small flex-grow-1">' + g.desc + '</p>' +
                    '<span class="btn btn-rainbow btn-sm mt-auto">View Worksheets</span>' +
                '</div>' +
            '</a>' +
        '</div>';
    }

    function emptyState(grid, message) {
        grid.innerHTML = '<div class="col-12"><div class="empty-state">' +
            '<span class="empty-icon">🔍</span>' +
            '<h5 class="fw-bold">Nothing here yet</h5>' +
            '<p>' + (message || 'Try a different search or filter.') + '</p>' +
            '<a href="worksheets.html" class="btn btn-rainbow btn-sm mt-2">Browse all worksheets</a>' +
            '</div></div>';
    }

    /* ---------- Shared chrome behaviors ---------- */
    function initChrome() {
        // Active nav link
        var page = (location.pathname.split('/').pop() || 'index.html').split('?')[0].toLowerCase();
        document.querySelectorAll('.navbar-nav .nav-link').forEach(function (a) {
            var href = (a.getAttribute('href') || '').toLowerCase();
            if (href && href === page) a.classList.add('active');
        });

        // Back-to-top
        var btn = document.getElementById('backToTop');
        if (!btn) {
            btn = document.createElement('button');
            btn.id = 'backToTop';
            btn.setAttribute('aria-label', 'Back to top');
            btn.innerHTML = '↑';
            document.body.appendChild(btn);
        }
        window.addEventListener('scroll', function () {
            btn.classList.toggle('show', window.scrollY > 400);
        }, { passive: true });
        btn.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        // Footer year
        document.querySelectorAll('[data-year]').forEach(function (el) {
            el.textContent = new Date().getFullYear();
        });

        // AOS guard (pages call AOS.init inline; this keeps it safe if CDN fails)
        if (typeof AOS !== 'undefined' && AOS && AOS.init && !window.__aosInit) {
            try { AOS.init({ duration: 900, once: true }); window.__aosInit = true; } catch (e) {}
        }

        // Newsletter demo handler
        document.querySelectorAll('.newsletter-form').forEach(function (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                var input = form.querySelector('input[type="email"]');
                if (input && input.value) {
                    form.innerHTML = '<div class="alert alert-success mb-0">🎉 You are subscribed! Check your inbox for a welcome gift.</div>';
                }
            });
        });
    }

    onReady(initChrome);

    // Expose helpers for page scripts
    window.WW = window.WW || {};
    window.WW.worksheetCard = worksheetCard;
    window.WW.subjectCard = subjectCard;
    window.WW.gradeCard = gradeCard;
    window.WW.emptyState = emptyState;
    window.WW.stars = stars;
})();

/* ============================================================
   K5 chrome — top utility bar, K5-style nav tabs, footer columns
   Runs on DOMContentLoaded. Guards for missing elements.
   Idempotent: skips when body[data-ww-chrome] is already set.
   ============================================================ */
(function () {
    'use strict';

    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }

    function esc(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
            .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    /* ---------- Nav data ---------- */
    var GRADES = [
        ['Preschool', 'preschool'], ['Kindergarten', 'kindergarten'],
        ['Grade 1', 'grade1'], ['Grade 2', 'grade2'], ['Grade 3', 'grade3'],
        ['Grade 4', 'grade4'], ['Grade 5', 'grade5'], ['Grade 6', 'grade6']
    ];
    var K6 = GRADES.slice(1);        // Kindergarten – Grade 6
    var K5G = GRADES.slice(1, 7);    // Kindergarten – Grade 5
    var G15 = GRADES.slice(2, 7);    // Grade 1 – Grade 5

    function byGrade(subject, grades) {
        return {
            header: 'By Grade',
            links: grades.map(function (g) {
                return [g[0], 'worksheets.html?subject=' + subject + '&grade=' + g[1]];
            })
        };
    }
    function topics(pairs) {
        return pairs.map(function (t) { return [t[0], 'worksheets.html?topic=' + t[1]]; });
    }

    var NAV = [
        { label: 'Math', href: 'subject-maths.html', groups: [
            byGrade('mathematics', K6),
            { header: 'Numbers', links: topics([
                ['Numbers', 'numbers'], ['Counting', 'counting'],
                ['Comparing Numbers', 'comparing-numbers'], ['Place Value', 'place-value'],
                ['Rounding', 'rounding'], ['Roman Numerals', 'roman-numerals']]) },
            { header: 'Fractions & Decimals', links: topics([
                ['Fractions', 'fractions'], ['Decimals', 'decimals']]) },
            { header: '4 Operations', links: topics([
                ['Addition', 'addition'], ['Subtraction', 'subtraction'],
                ['Multiplication', 'multiplication'], ['Division', 'division'],
                ['Order of Operations', 'order-of-operations'], ['Math Drills', 'math-drills']]) },
            { header: 'Measurement', links: topics([
                ['Measurement', 'measurement'], ['Money', 'money'], ['Time', 'time']]) },
            { header: 'Advanced', links: topics([
                ['Factoring', 'factoring'], ['Exponents', 'exponents'],
                ['Proportions', 'proportions'], ['Percents', 'percents'],
                ['Integers', 'integers'], ['Algebra', 'algebra']]) },
            { header: 'More', links: topics([
                ['Geometry', 'geometry'], ['Shapes', 'shapes'],
                ['Data & Graphing', 'data-graphing'], ['Word Problems', 'word-problems'],
                ['Comparing & Sorting', 'comparing-sorting']]) }
        ]},
        { label: 'Reading', href: 'reading.html', groups: [
            byGrade('english', K5G),
            { header: 'Stories', links: topics([['Stories & Fables', 'stories-fables']]) },
            { header: 'Early Reading', links: topics([
                ['Phonics', 'phonics'], ['Sight Words', 'sight-words'],
                ['Alphabet', 'alphabet'], ['Letter Activities', 'letter-activities']]) },
            { header: 'Reading Comprehension', links: topics([
                ['Comprehension', 'comprehension'], ['Comprehension Skills', 'comprehension-skills']]) }
        ]},
        { label: 'Kindergarten', href: 'kindergarten.html', groups: [
            { header: 'Early Reading', links: topics([
                ['Alphabet', 'alphabet'], ['Phonics', 'phonics'], ['Sight Words', 'sight-words'],
                ['Vocabulary', 'vocabulary'], ['Pre-writing', 'pre-writing'],
                ['Early Writing', 'early-writing'], ['Letter Activities', 'letter-activities'],
                ['Comprehension', 'comprehension']]) },
            { header: 'Early Math', links: topics([
                ['Shapes', 'shapes'], ['Numbers', 'numbers'], ['Counting', 'counting'],
                ['Addition', 'addition'], ['Subtraction', 'subtraction']]) },
            { header: 'Early Science & More', links: topics([
                ['Coloring', 'coloring'], ['Comparing & Sorting', 'comparing-sorting'],
                ['Social & Emotional', 'social-emotional']]) }
        ]},
        { label: 'Vocabulary', href: 'vocabulary.html', groups: [
            byGrade('english', K5G),
            { header: 'Topics', links: topics([
                ['Vocabulary', 'vocabulary'], ['Crossword Puzzles', 'crossword-puzzles']]) }
        ]},
        { label: 'Spelling', href: 'spelling.html', groups: [
            byGrade('english', G15),
            { header: 'Topics', links: topics([['Spelling', 'spelling']]) }
        ]},
        { label: 'Grammar & Writing', href: 'grammar.html', groups: [
            byGrade('english', K5G),
            { header: 'Grammar', links: topics([
                ['Grammar', 'grammar'], ['Verbs', 'verbs'], ['Adjectives', 'adjectives'],
                ['Adverbs', 'adverbs'], ['Pronouns', 'pronouns']]) },
            { header: 'Writing', links: topics([
                ['Sentences', 'sentences'], ['Punctuation', 'punctuation'],
                ['Capitalization', 'capitalization'], ['Writing', 'writing'],
                ['Early Writing', 'early-writing']]) }
        ]},
        { label: 'Science', href: 'subject-science.html', groups: [
            byGrade('science', K6),
            { header: 'Life Science', links: topics([
                ['Biology', 'biology'], ['Living Things', 'living-things'],
                ['Food & Nutrition', 'food-nutrition']]) },
            { header: 'Earth Science', links: topics([
                ['Earth Science', 'earth-science'], ['Space', 'space'],
                ['Weather & Seasons', 'weather-seasons'], ['Environment', 'environment']]) },
            { header: 'Physical Science', links: topics([
                ['Matter', 'matter'], ['Energy', 'energy'], ['Pushes & Pulls', 'pushes-pulls']]) }
        ]},
        { label: 'Cursive', href: 'cursive.html', groups: [
            { header: 'Topics', links: topics([['Cursive', 'cursive']]) }
        ]},
        { label: 'Bookstore', href: 'shop.html' },
        { label: 'Grades', href: 'grade.html', groups: [
            { header: 'By Grade', links: GRADES.map(function (g) { return [g[0], g[1] + '.html']; }) }
        ]},
        { label: 'Worksheets', href: 'worksheets.html' },
        { label: 'Freebies', href: 'freebies.html' },
        { label: 'Blog', href: 'blog.html' }
    ];

    var ACTIVE_TAB = {
        'subject-maths.html': 'Math', 'reading.html': 'Reading',
        'kindergarten.html': 'Kindergarten', 'vocabulary.html': 'Vocabulary',
        'spelling.html': 'Spelling', 'grammar.html': 'Grammar & Writing',
        'subject-science.html': 'Science', 'cursive.html': 'Cursive',
        'shop.html': 'Bookstore', 'worksheets.html': 'Worksheets',
        'freebies.html': 'Freebies', 'blog.html': 'Blog',
        'preschool.html': 'Grades', 'grade1.html': 'Grades', 'grade2.html': 'Grades',
        'grade3.html': 'Grades', 'grade4.html': 'Grades', 'grade5.html': 'Grades',
        'grade6.html': 'Grades', 'grade.html': 'Grades'
    };

    /* ---------- Footer data ---------- */
    var FOOT_COLS = [
        { title: 'Subjects', links: [
            ['Math', 'subject-maths.html'], ['Reading', 'reading.html'],
            ['Kindergarten', 'kindergarten.html'], ['Grammar & Writing', 'grammar.html'],
            ['Vocabulary', 'vocabulary.html'], ['Spelling', 'spelling.html'],
            ['Science', 'subject-science.html'], ['Cursive', 'cursive.html']] },
        { title: 'Resources', links: [
            ['Worksheets', 'worksheets.html'], ['Bookstore', 'shop.html'],
            ['Freebies', 'freebies.html'], ['Blog', 'blog.html']] },
        { title: 'About', links: [
            ['About Us', 'about.html'], ['FAQs', 'faq.html'], ['Contact Us', 'contact.html']] },
        { title: 'Other', links: [
            ['Privacy', 'privacy.html'], ['Terms of Use', 'terms.html']] }
    ];

    /* ---------- CSS ---------- */
    function injectCSS() {
        if (document.getElementById('ww-chrome-css')) return;
        var st = document.createElement('style');
        st.id = 'ww-chrome-css';
        st.textContent =
            '.ww-subject-tabs{display:none!important}' +
            '.top-bar:not(.ww-utility-bar){display:none!important}' +
            '.ww-utility-bar{border-bottom:1px solid rgba(255,255,255,.12)}' +
            '.ww-utility-tagline{font-size:.8rem;letter-spacing:.3px}' +
            '.ww-utility-search .form-control{width:170px}' +
            '.ww-utility-link{color:#fff;text-decoration:none;font-size:.82rem;font-weight:600;white-space:nowrap}' +
            '.ww-utility-link:hover{color:#F26A21}' +
            '.ww-utility-sep{color:rgba(255,255,255,.35);font-size:.8rem}' +
            '.ww-nav-drop{display:flex;align-items:center}' +
            '.ww-nav-caret{background:none;border:0;padding:.5rem .2rem;font-size:.65rem;color:inherit;line-height:1;cursor:pointer}' +
            '.ww-nav-caret:focus{outline:none;box-shadow:none}' +
            '.ww-nav-drop .dropdown-menu{max-height:72vh;overflow-y:auto}' +
            '.ww-k5-tabbar{background:#16305b}' +
            '.ww-k5-tabs{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;align-items:stretch}' +
            '.ww-k5-tab{display:flex;align-items:stretch;position:relative}' +
            '.ww-k5-tab>a{color:#fff;text-decoration:none;font-weight:600;font-size:.88rem;padding:.72rem .95rem;display:flex;align-items:center;white-space:nowrap}' +
            '.ww-k5-tab>a:hover{color:#F5A623}' +
            '.ww-k5-tab.active>a{color:#F5A623;box-shadow:inset 0 -3px 0 #F26A21}' +
            '.ww-k5-tab .dropdown-menu{margin-top:0;max-height:72vh;overflow-y:auto}' +
            '.ww-k5-caret{background:none;border:0;color:#fff;font-size:.6rem;padding:.72rem .3rem;cursor:pointer;line-height:1}' +
            '.ww-k5-caret:hover,.ww-k5-caret:focus{color:#F5A623;outline:none;box-shadow:none}';
        document.head.appendChild(st);
    }

    /* ---------- Utility bar ---------- */
    function buildUtilityBar() {
        if (document.querySelector('.ww-utility-bar')) return;
        var bar = document.createElement('div');
        bar.className = 'ww-utility-bar top-bar';
        bar.innerHTML =
            '<div class="container d-flex flex-wrap align-items-center justify-content-between gap-2">' +
                '<span class="ww-utility-tagline">Free Printable Worksheets &bull; Preschool &ndash; Grade 6</span>' +
                '<div class="d-flex align-items-center gap-2 flex-wrap">' +
                    '<form class="ww-utility-search d-flex" action="search.html" method="get" role="search">' +
                        '<input class="form-control form-control-sm" type="search" name="q" ' +
                            'placeholder="Search worksheets&hellip;" aria-label="Search worksheets">' +
                        '<button class="btn btn-sm btn-light ms-1" type="submit" aria-label="Search">' +
                            '<i class="bi bi-search"></i></button>' +
                    '</form>' +
                    '<a class="ww-utility-link" href="register.html">Sign Up</a>' +
                    '<span class="ww-utility-sep">|</span>' +
                    '<a class="ww-utility-link" href="login.html">Log In</a>' +
                '</div>' +
            '</div>';
        document.body.insertBefore(bar, document.body.firstChild);
    }

    /* ---------- Nav tabs ---------- */
    function navItem(tab, i) {
        var label = esc(tab.label);
        if (!tab.groups) {
            return '<li class="nav-item"><a class="nav-link" href="' + tab.href + '">' +
                label + '</a></li>';
        }
        var id = 'wwNavMenu' + i;
        var menu = tab.groups.map(function (g) {
            return '<li><h6 class="dropdown-header">' + esc(g.header) + '</h6></li>' +
                g.links.map(function (l) {
                    return '<li><a class="dropdown-item" href="' + l[1] + '">' +
                        esc(l[0]) + '</a></li>';
                }).join('');
        }).join('<li><hr class="dropdown-divider"></li>');
        return '<li class="nav-item dropdown ww-nav-drop">' +
            '<a class="nav-link" href="' + tab.href + '">' + label + '</a>' +
            '<button class="ww-nav-caret nav-link" type="button" id="' + id + '" ' +
                'data-bs-toggle="dropdown" aria-expanded="false" aria-label="' + label + ' menu">' +
                '<i class="bi bi-chevron-down"></i></button>' +
            '<ul class="dropdown-menu shadow-sm" aria-labelledby="' + id + '">' + menu + '</ul></li>';
    }

    /* Slim white navbar menu (brand row keeps Grades / Worksheets / Freebies / Blog).
       The 9 K5 tabs live in their own navy tab bar below the navbar. */
    var MENU = [
        { label: 'Grades', href: 'grade.html', groups: [
            { header: 'By Grade', links: GRADES.map(function (g) { return [g[0], g[1] + '.html']; }) }
        ]},
        { label: 'Worksheets', href: 'worksheets.html' },
        { label: 'Freebies', href: 'freebies.html' },
        { label: 'Blog', href: 'blog.html' }
    ];
    var TABS = NAV.slice(0, 9); // Math … Bookstore

    function tabItem(tab, i) {
        var label = esc(tab.label);
        if (!tab.groups) {
            return '<li class="ww-k5-tab"><a href="' + tab.href + '">' + label + '</a></li>';
        }
        var id = 'wwTabMenu' + i;
        var menu = tab.groups.map(function (g) {
            return '<li><h6 class="dropdown-header">' + esc(g.header) + '</h6></li>' +
                g.links.map(function (l) {
                    return '<li><a class="dropdown-item" href="' + l[1] + '">' +
                        esc(l[0]) + '</a></li>';
                }).join('');
        }).join('<li><hr class="dropdown-divider"></li>');
        return '<li class="ww-k5-tab dropdown">' +
            '<a href="' + tab.href + '">' + label + '</a>' +
            '<button class="ww-k5-caret" type="button" id="' + id + '" ' +
                'data-bs-toggle="dropdown" aria-expanded="false" aria-label="' + label + ' menu">' +
                '<i class="bi bi-chevron-down"></i></button>' +
            '<ul class="dropdown-menu shadow-sm" aria-labelledby="' + id + '">' + menu + '</ul></li>';
    }

    function markActive(root, label) {
        if (!root || !label) return;
        var links = root.querySelectorAll('a');
        for (var k = 0; k < links.length; k++) {
            if (links[k].textContent.trim() === label) {
                var li = links[k].closest('li');
                if (li) li.classList.add('active');
                links[k].setAttribute('aria-current', 'page');
                break;
            }
        }
    }

    function buildNav() {
        var nav = document.querySelector('#mainMenu .navbar-nav');
        if (nav && !nav.getAttribute('data-ww-nav')) {
            nav.setAttribute('data-ww-nav', '1');
            nav.innerHTML = MENU.map(function (tab, i) { return navItem(tab, i); }).join('');
        }
        var bar = document.querySelector('.ww-k5-tabbar');
        if (!bar) {
            bar = document.createElement('div');
            bar.className = 'ww-k5-tabbar';
            bar.innerHTML = '<div class="container"><ul class="ww-k5-tabs">' +
                TABS.map(function (tab, i) { return tabItem(tab, i); }).join('') +
                '</ul></div>';
            var navbar = document.querySelector('nav.navbar');
            if (navbar && navbar.parentNode) navbar.parentNode.insertBefore(bar, navbar.nextSibling);
            else document.body.insertBefore(bar, document.body.firstChild);
        }
        var page = (location.pathname.split('/').pop() || 'index.html').split('?')[0].toLowerCase();
        var label = ACTIVE_TAB[page];
        if (label) {
            markActive(bar, label);
            if (nav) markActive(nav, label);
        }
    }

    /* ---------- Footer columns ---------- */
    function rebuildFooter() {
        var footer = document.querySelector('footer');
        if (!footer || footer.getAttribute('data-ww-foot')) return;
        var row = footer.querySelector('.row');
        if (!row) return;
        var cols = [];
        for (var i = 0; i < row.children.length; i++) {
            if (row.children[i].nodeType === 1) cols.push(row.children[i]);
        }
        if (cols.length < 2) return; // nothing sensible to rebuild
        footer.setAttribute('data-ww-foot', '1');
        for (var j = cols.length - 1; j >= 1; j--) row.removeChild(cols[j]);
        var html = FOOT_COLS.map(function (c) {
            var items = c.links.map(function (l) {
                return '<li class="mb-2"><a href="' + l[1] + '" class="text-decoration-none">' +
                    esc(l[0]) + '</a></li>';
            }).join('');
            return '<div class="col-md-6 col-lg-2">' +
                '<h5 class="footer-heading text-rainbow mb-3">' + esc(c.title) + '</h5>' +
                '<ul class="footer-links list-unstyled text-muted small">' + items + '</ul></div>';
        }).join('');
        cols[0].insertAdjacentHTML('afterend', html);
    }

    onReady(function () {
        if (document.body.getAttribute('data-ww-chrome')) return;
        document.body.setAttribute('data-ww-chrome', '1');
        injectCSS();
        buildUtilityBar();
        buildNav();
        rebuildFooter();
    });
})();
