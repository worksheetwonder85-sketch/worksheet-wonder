/* Worksheet Wonder — categories.js (categories.html) */
(function () {
    'use strict';
    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }
    onReady(function () {
        if (!window.WWDatabase || !window.WW) return;
        var DB = window.WWDatabase;
        var grid = document.getElementById('categories-grid');
        if (!grid) return;
        var loading = document.getElementById('categories-loading');
        if (loading) loading.style.display = 'none';
        var html = '<div class="col-12 mb-2"><h4 class="fw-bold">Shop by Grade</h4></div>';
        html += DB.getGrades().map(window.WW.gradeCard).join('');
        html += '<div class="col-12 mb-2 mt-3"><h4 class="fw-bold">Shop by Subject</h4></div>';
        html += DB.getSubjects().map(window.WW.subjectCard).join('');
        grid.innerHTML = html;
    });
})();
