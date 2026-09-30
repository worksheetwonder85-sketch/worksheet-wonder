# Worksheet Wonder - Publishing Database

Welcome to the **Worksheet Wonder** publishing database. This folder structure organizes worksheet templates, printable PDFs, image assets, blog articles, shopping transactions, and user accounts. It is designed to scale to **10,000+ worksheets** and integrates easily with both relational databases (SQL) and lightweight client-side applications (JSON).

---

## 📂 Folder Structure & Usage

* **`schema/`**
  * `database_schema.sql`: ANSI SQL definitions for creating tables, primary keys, foreign keys, and indexes. Compatible with SQLite, PostgreSQL, and MySQL.
  * `tables_description.md`: Detailed documentation of each column, data type, nullability, and description.
  * `relationships.md`: Entity-Relationship details and a Mermaid visual diagram mapping constraints.
* **`data/`**
  * Contains structured JSON seed files representing the main database tables. Ideal for local mock setups, frontend dev servers, or populating the SQL server.
  * Files included: `grades.json`, `categories.json`, `subjects.json`, `worksheets.json`, `products.json`, `users.json`, `orders.json`, and `blog_posts.json`.
* **`worksheets/`**
  * Houses interactive HTML worksheets, grouped by grades (e.g., `kindergarten/maths/`, `grade-1/` to `grade-6/`). Keep files structured here.
* **`images/`**
  * `worksheet-thumbnails/`: Thumbnails used on catalog/search pages.
  * `product-images/`: Cover art for bundle packages or subscriptions.
  * `category-images/`: Graphics representing specific subjects/skills.
* **`pdf/`**
  * Storage for direct printable files. Divided into `free-worksheets/` and `paid-worksheets/`.
* **`backups/`**
  * Target folder for scheduled SQL dumps and JSON data backups.

---

## 📝 How to Add New Worksheets

To insert a new worksheet into the Worksheet Wonder library:

### Step 1: Save Files
1. Save the interactive HTML file inside the appropriate subfolder in `database/worksheets/` (e.g., `database/worksheets/kindergarten/maths/counting_stars.html`).
2. Save the downloadable PDF version inside `database/pdf/free-worksheets/` or `database/pdf/paid-worksheets/`.
3. Save the thumbnail image (PNG or JPG) inside `database/images/worksheet-thumbnails/`.

### Step 2: Register in Database (JSON/SQL)
Add a entry to `database/data/worksheets.json` or insert a record into the SQL `worksheets` table.

**Example JSON Entry:**
```json
{
  "id": 12,
  "title": "Counting Stars",
  "grade": "Kindergarten",
  "age_group": "4-6 years",
  "subject": "Maths",
  "category": "Numbers",
  "description": "Practice counting objects from 1 to 10 with interactive stars.",
  "difficulty": "Easy",
  "file_path": "worksheets/kindergarten/maths/counting_stars.html",
  "thumbnail": "database/images/worksheet-thumbnails/counting_stars.png",
  "price": 0.00,
  "is_free": true,
  "created_date": "2026-07-17T14:00:00Z"
}
```

**Example SQL Insertion:**
```sql
INSERT INTO worksheets (title, description, grade_id, subject_id, category_id, age_group, difficulty, file_path, pdf_path, thumbnail, price, is_free)
VALUES (
  'Counting Stars',
  'Practice counting objects from 1 to 10 with interactive stars.',
  1, -- Kindergarten (grades.id)
  2, -- Maths (subjects.id)
  3, -- Numbers (categories.id)
  '4-6 years',
  'Easy',
  'worksheets/kindergarten/maths/counting_stars.html',
  'pdf/free-worksheets/counting_stars.pdf',
  'images/worksheet-thumbnails/counting_stars.png',
  0.00,
  1
);
```

---

## 🌐 Website Integration & Backend Connection

Initially, the Worksheet Wonder website can run entirely serverless or static by reading directly from the files inside `database/data/`. When transitioning to a fully dynamic backend, here is how the pages will connect:

### 1. Catalog & Search Pages (`shop.html`, `freebies.html`)
* **Client-Side JS**: Performs a `fetch('database/data/worksheets.json')`, parsing the worksheets list into memory. It filters by `grade`, `subject`, `category`, and `is_free` to render matching cards.
* **Backend Connection**: The backend (e.g., Node.js Express, Python Flask, or Go) exposes a REST API (e.g., `/api/worksheets?grade=kindergarten`). The server executes an optimized SQL query leveraging index `idx_worksheets_grade_subject` for sub-second retrieval.

### 2. Worksheet Detail Page (`worksheet-details.html`)
* **Client-Side JS**: Reads the query string `?id=X`. It fetches the JSON dataset and loads metadata for matching ID `X`, rendering description, thumbnail, and the preview iframe pointing to `file_path`.
* **Backend Connection**: API endpoint `/api/worksheets/:id` queries the database by primary key (`id`) and returns the record dynamically.

### 3. Shopping Cart and Purchase Flow (`cart.html`, `checkout.html`)
* **Client-Side JS**: Stores selected worksheet/bundle IDs in `localStorage`. During checkout, it posts the cart array to the backend.
* **Backend Connection**: The backend creates an order record in the `orders` table, verifies transaction amounts, and populates `order_items` listing purchased product IDs. Once complete, it unlocks access to the corresponding `pdf_path` for download.

### 4. Admin Dashboard (`admin/`)
* Form interfaces make CRUD operations directly to database APIs, allowing admins to upload new assets and automatically write entries, bypassing manual JSON editing.
