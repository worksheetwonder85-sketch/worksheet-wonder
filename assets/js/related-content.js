/*==================================================
  Worksheet Wonder
  Related Content & Worksheet Details Binding Engine
==================================================*/

document.addEventListener("DOMContentLoaded", () => {
    initWorksheetDetailsPage();
});

async function initWorksheetDetailsPage() {
    const detailsContainer = document.getElementById("worksheet-details-container");
    const breadcrumbContainer = document.getElementById("dynamic-breadcrumb");
    const relatedWorksheetsGrid = document.getElementById("related-worksheets-grid");
    const recommendedBundleContainer = document.getElementById("recommended-bundle-container");

    const urlParams = new URLSearchParams(window.location.search);
    const worksheetId = urlParams.get("id") || urlParams.get("worksheet_id") || "1";

    try {
        const worksheet = await getWorksheetById(worksheetId);
        const allWorksheets = await getAllWorksheets();
        const allProducts = await getProducts();

        if (!worksheet) {
            console.warn(`Worksheet with ID '${worksheetId}' not found. Loading default.`);
            return;
        }

        // 1. Update Breadcrumbs according to hierarchical standard:
        // Home → Worksheets → Grade → Subject → Topic → Subtopic → Worksheet
        if (breadcrumbContainer) {
            let breadcrumbHtml = `
                <li class="breadcrumb-item"><a href="index.html">Home</a></li>
                <li class="breadcrumb-item"><a href="worksheets.html">Worksheets</a></li>
            `;

            if (worksheet.grade) {
                breadcrumbHtml += `<li class="breadcrumb-item"><a href="worksheets.html?grade=${encodeURIComponent(worksheet.grade)}">${worksheet.grade}</a></li>`;
            }
            if (worksheet.subject) {
                breadcrumbHtml += `<li class="breadcrumb-item"><a href="worksheets.html?subject=${encodeURIComponent(worksheet.subject)}">${worksheet.subject}</a></li>`;
            }
            if (worksheet.topic) {
                breadcrumbHtml += `<li class="breadcrumb-item"><a href="worksheets.html?category=${encodeURIComponent(worksheet.topic)}">${worksheet.topic}</a></li>`;
            }
            // Gracefully include subtopic if available
            if (worksheet.subtopic) {
                breadcrumbHtml += `<li class="breadcrumb-item"><a href="worksheets.html?category=${encodeURIComponent(worksheet.subtopic)}">${worksheet.subtopic}</a></li>`;
            }

            breadcrumbHtml += `<li class="breadcrumb-item active" aria-current="page">${worksheet.title}</li>`;
            breadcrumbContainer.innerHTML = breadcrumbHtml;
        }

        // 2. Render Worksheet Main Details
        if (detailsContainer) {
            const isFree = worksheet.is_free || worksheet.price === 0;
            const priceBadge = isFree ? `<span class="badge bg-success fs-6">FREE</span>` : `<span class="badge bg-primary fs-6">₹${worksheet.price}</span>`;
            
            detailsContainer.innerHTML = `
                <div class="row align-items-center g-5">
                    <div class="col-lg-5 col-md-6 text-center">
                        <img src="${worksheet.thumbnail}" class="img-fluid rounded shadow border" alt="${worksheet.title}" onerror="this.src='assets/images/logo.png'; this.style.backgroundColor='#eef9ff';">
                    </div>
                    <div class="col-lg-7 col-md-6">
                        <div class="d-flex gap-2 align-items-center mb-3">
                            <span class="badge bg-warning text-dark">⭐ Bestseller</span>
                            <span class="badge bg-info text-dark">${worksheet.grade}</span>
                            <span class="badge bg-secondary">${worksheet.subject}</span>
                            <span class="badge bg-dark">${worksheet.difficulty}</span>
                            ${priceBadge}
                        </div>
                        <h1 class="fw-bold display-6">${worksheet.title}</h1>
                        <p class="lead text-muted mt-3">${worksheet.description}</p>
                        <div class="my-4 p-3 bg-light rounded border">
                            <div class="row text-center g-3">
                                <div class="col-4 border-end">
                                    <small class="text-muted d-block">Target Age</small>
                                    <strong class="text-dark">${worksheet.age || worksheet.age_group || '4-8 yrs'}</strong>
                                </div>
                                <div class="col-4 border-end">
                                    <small class="text-muted d-block">Worksheet Type</small>
                                    <strong class="text-dark">${worksheet.worksheetType || 'Printable PDF'}</strong>
                                </div>
                                <div class="col-4">
                                    <small class="text-muted d-block">Answer Key</small>
                                    <strong class="text-success"><i class="bi bi-check-circle-fill"></i> Included</strong>
                                </div>
                            </div>
                        </div>
                        <div class="d-flex gap-3">
                            <a href="${worksheet.file_path}" class="btn btn-rainbow btn-lg flex-grow-1">
                                <i class="bi bi-download me-2"></i> ${isFree ? 'Download Printable PDF' : 'Get Printable Package'}
                            </a>
                            <a href="${worksheet.file_path}" class="btn btn-outline-primary btn-lg">
                                <i class="bi bi-eye me-2"></i> Interactive Preview
                            </a>
                        </div>
                    </div>
                </div>
            `;
        }

        // 3. Render Dynamic Related Worksheets (same grade or subject)
        if (relatedWorksheetsGrid) {
            const related = allWorksheets.filter(w => 
                String(w.id) !== String(worksheet.id) && 
                (w.grade === worksheet.grade || w.subject === worksheet.subject)
            ).slice(0, 3);

            relatedWorksheetsGrid.innerHTML = "";
            related.forEach(rel => {
                const col = document.createElement("div");
                col.className = "col-md-4 mb-4";
                col.innerHTML = `
                    <div class="bundle-card h-100 shadow-sm rounded border overflow-hidden d-flex flex-column">
                        <img src="${rel.thumbnail}" class="img-fluid w-100" style="height: 180px; object-fit: cover;" alt="${rel.title}" onerror="this.src='assets/images/logo.png'; this.style.backgroundColor='#eef9ff';">
                        <div class="p-3 d-flex flex-column flex-grow-1">
                            <div class="d-flex justify-content-between mb-2">
                                <span class="badge bg-primary">${rel.grade}</span>
                                <span class="badge bg-secondary">${rel.subject}</span>
                            </div>
                            <h6 class="fw-bold">${rel.title}</h6>
                            <a href="worksheet-details.html?id=${rel.id}" class="btn btn-outline-primary btn-sm mt-auto">View Worksheet</a>
                        </div>
                    </div>
                `;
                relatedWorksheetsGrid.appendChild(col);
            });
        }

        // 4. Render Recommended Shop Bundle
        if (recommendedBundleContainer && allProducts.length > 0) {
            const product = allProducts[0];
            recommendedBundleContainer.innerHTML = `
                <div class="card bg-primary text-white border-0 shadow rounded p-4">
                    <div class="row align-items-center">
                        <div class="col-md-8">
                            <span class="badge bg-warning text-dark mb-2">Recommended Bundle</span>
                            <h3 class="fw-bold mb-2">${product.title}</h3>
                            <p class="mb-0 opacity-90">${product.description}</p>
                        </div>
                        <div class="col-md-4 text-md-end mt-3 mt-md-0">
                            <a href="shop.html" class="btn btn-light btn-lg fw-bold text-primary">Get Bundle - ₹${product.price}</a>
                        </div>
                    </div>
                </div>
            `;
        }

    } catch (err) {
        console.error("Error initializing worksheet details page:", err);
    }
}
