/*==================================================
  Worksheet Wonder - Admin Editor Controller
==================================================*/

document.addEventListener("DOMContentLoaded", () => {
    initWorksheetEditor();
});

async function initWorksheetEditor() {
    const editorForm = document.getElementById("admin-worksheet-form");
    if (!editorForm) return;

    const titleInput = document.getElementById("field-title");
    const slugInput = document.getElementById("field-slug");
    const gradeSelect = document.getElementById("field-grade");
    const subjectSelect = document.getElementById("field-subject");
    const topicSelect = document.getElementById("field-topic");
    const subtopicSelect = document.getElementById("field-subtopic");
    const typeSelect = document.getElementById("field-type");
    const difficultySelect = document.getElementById("field-difficulty");
    const priceInput = document.getElementById("field-price");
    const freeCheck = document.getElementById("field-is-free");
    const descInput = document.getElementById("field-description");
    const saveBtn = document.getElementById("admin-save-btn");

    const urlParams = new URLSearchParams(window.location.search);
    const editId = urlParams.get("id");

    // Populate dropdown options from database
    try {
        const [grades, subjects, topics, subtopics, types] = await Promise.all([
            window.adminDb.fetchCollection("grades"),
            window.adminDb.fetchCollection("subjects"),
            window.adminDb.fetchCollection("topics"),
            window.adminDb.fetchCollection("subtopics"),
            window.adminDb.fetchCollection("worksheet-types")
        ]);

        if (gradeSelect) {
            gradeSelect.innerHTML = grades.map(g => `<option value="${g.name}">${g.name}</option>`).join("");
        }
        if (subjectSelect) {
            subjectSelect.innerHTML = subjects.map(s => `<option value="${s.name}">${s.name}</option>`).join("");
        }
        if (topicSelect) {
            topicSelect.innerHTML = topics.map(t => `<option value="${t.name}">${t.name}</option>`).join("");
        }
        if (subtopicSelect) {
            subtopicSelect.innerHTML = subtopics.map(st => `<option value="${st.name}">${st.name}</option>`).join("");
        }
        if (typeSelect) {
            typeSelect.innerHTML = types.map(t => `<option value="${t.name}">${t.name}</option>`).join("");
        }

        // Load existing record if editing
        if (editId) {
            const worksheets = await window.adminDb.fetchCollection("worksheets");
            const record = worksheets.find(w => String(w.id) === String(editId));
            if (record) {
                if (titleInput) titleInput.value = record.title || "";
                if (slugInput) slugInput.value = record.slug || titleInput.value.toLowerCase().replace(/\s+/g, "-");
                if (gradeSelect) gradeSelect.value = record.grade || grades[0].name;
                if (subjectSelect) subjectSelect.value = record.subject || subjects[0].name;
                if (topicSelect) topicSelect.value = record.topic || topics[0].name;
                if (subtopicSelect) subtopicSelect.value = record.subtopic || subtopics[0].name;
                if (typeSelect) typeSelect.value = record.worksheetType || types[0].name;
                if (difficultySelect) difficultySelect.value = record.difficulty || "Beginner";
                if (priceInput) priceInput.value = record.price || 0;
                if (freeCheck) freeCheck.checked = record.is_free || false;
                if (descInput) descInput.value = record.description || "";
            }
        }
    } catch (err) {
        console.error("Error populating editor dropdowns:", err);
    }

    // Auto-slug generator
    if (titleInput && slugInput) {
        titleInput.addEventListener("input", () => {
            if (!editId) {
                slugInput.value = titleInput.value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
            }
        });
    }

    // Form Save Listener
    if (editorForm) {
        editorForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const recordData = {
                id: editId || null,
                title: titleInput.value,
                slug: slugInput.value,
                grade: gradeSelect.value,
                subject: subjectSelect.value,
                topic: topicSelect.value,
                subtopic: subtopicSelect.value,
                worksheetType: typeSelect.value,
                difficulty: difficultySelect.value,
                price: parseFloat(priceInput.value) || 0,
                is_free: freeCheck ? freeCheck.checked : false,
                description: descInput.value,
                thumbnail: "assets/images/worksheets/bundles/alphabet.png"
            };

            await window.adminDb.saveWorksheet(recordData);
            alert("Worksheet record saved successfully!");
            window.location.href = "worksheets.html";
        });
    }
}
