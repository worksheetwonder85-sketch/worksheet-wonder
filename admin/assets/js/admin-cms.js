/*==================================================
  Worksheet Wonder - Admin CMS UI Controller
==================================================*/

document.addEventListener("DOMContentLoaded", () => {
    initAdminDashboard();
    initAdminWorksheetsManager();
});

async function initAdminDashboard() {
    const statWs = document.getElementById("admin-stat-worksheets");
    const statGrades = document.getElementById("admin-stat-grades");
    const statSubjects = document.getElementById("admin-stat-subjects");
    const statTopics = document.getElementById("admin-stat-topics");
    const statSubtopics = document.getElementById("admin-stat-subtopics");
    const statCollections = document.getElementById("admin-stat-collections");
    const statProducts = document.getElementById("admin-stat-products");
    const statBlogs = document.getElementById("admin-stat-blogs");

    if (!statWs) return;

    try {
        const stats = await window.adminDb.getDatabaseStats();
        if (statWs) statWs.innerText = stats.worksheetsCount;
        if (statGrades) statGrades.innerText = stats.gradesCount;
        if (statSubjects) statSubjects.innerText = stats.subjectsCount;
        if (statTopics) statTopics.innerText = stats.topicsCount;
        if (statSubtopics) statSubtopics.innerText = stats.subtopicsCount;
        if (statCollections) statCollections.innerText = stats.collectionsCount;
        if (statProducts) statProducts.innerText = stats.productsCount;
        if (statBlogs) statBlogs.innerText = stats.blogPostsCount;
    } catch (err) {
        console.error("Error initializing Admin Dashboard:", err);
    }
}

async function initAdminWorksheetsManager() {
    const tableBody = document.getElementById("admin-worksheets-table-body");
    const searchInput = document.getElementById("admin-search-input");
    const gradeFilter = document.getElementById("admin-filter-grade");
    const subjectFilter = document.getElementById("admin-filter-subject");
    const paginationContainer = document.getElementById("admin-pagination");

    if (!tableBody) return;

    let currentPage = 1;

    async function loadTableData() {
        const filters = {
            search: searchInput ? searchInput.value : "",
            grade: gradeFilter ? gradeFilter.value : "All",
            subject: subjectFilter ? subjectFilter.value : "All"
        };

        const result = await window.adminDb.getWorksheets(filters, currentPage, 10);
        tableBody.innerHTML = "";

        if (result.data.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-muted">No worksheet records found.</td></tr>`;
            return;
        }

        result.data.forEach(w => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><input type="checkbox" class="form-check-input ws-select-item" value="${w.id}"></td>
                <td><strong>#${w.id}</strong></td>
                <td>
                    <div class="d-flex align-items-center">
                        <img src="../${w.thumbnail}" class="rounded me-2" style="width: 40px; height: 40px; object-fit: cover;" onerror="this.src='../assets/images/logo.png';">
                        <div>
                            <div class="fw-bold">${w.title}</div>
                            <small class="text-muted">${w.worksheetType || 'Printable PDF'}</small>
                        </div>
                    </div>
                </td>
                <td><span class="badge bg-info text-dark">${w.grade}</span></td>
                <td><span class="badge bg-secondary">${w.subject}</span></td>
                <td>${w.is_free ? '<span class="badge bg-success">FREE</span>' : '<span class="badge bg-primary">₹' + w.price + '</span>'}</td>
                <td>
                    <div class="btn-group btn-group-sm">
                        <a href="worksheet-editor.html?id=${w.id}" class="btn btn-outline-primary" title="Edit"><i class="bi bi-pencil"></i></a>
                        <button class="btn btn-outline-danger btn-delete-ws" data-id="${w.id}" title="Soft Delete"><i class="bi bi-trash"></i></button>
                    </div>
                </td>
            `;
            tableBody.appendChild(tr);
        });

        // Bind delete listeners
        document.querySelectorAll(".btn-delete-ws").forEach(btn => {
            btn.addEventListener("click", async (e) => {
                const id = e.currentTarget.getAttribute("data-id");
                if (confirm(`Are you sure you want to delete worksheet #${id}?`)) {
                    await window.adminDb.softDeleteWorksheet(id);
                    await loadTableData();
                }
            });
        });

        // Render Pagination
        if (paginationContainer) {
            paginationContainer.innerHTML = "";
            for (let i = 1; i <= result.totalPages; i++) {
                const btn = document.createElement("button");
                btn.className = `btn btn-sm ${i === currentPage ? 'btn-primary' : 'btn-outline-secondary'} me-1`;
                btn.innerText = i;
                btn.addEventListener("click", async () => {
                    currentPage = i;
                    await loadTableData();
                });
                paginationContainer.appendChild(btn);
            }
        }
    }

    if (searchInput) searchInput.addEventListener("input", () => { currentPage = 1; loadTableData(); });
    if (gradeFilter) gradeFilter.addEventListener("change", () => { currentPage = 1; loadTableData(); });
    if (subjectFilter) subjectFilter.addEventListener("change", () => { currentPage = 1; loadTableData(); });

    await loadTableData();
}
