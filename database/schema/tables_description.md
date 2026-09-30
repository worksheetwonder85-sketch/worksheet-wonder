# Table Descriptions - Worksheet Wonder Database

This document lists details for each database table, defining column data types, key constraints, and descriptions of what each field represents.

---

## 1. `grades`
Contains educational grade levels from Kindergarten to Grade 6.

| Field Name | Data Type | Nullability | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `NOT NULL` | `PRIMARY KEY AUTOINCREMENT` | Unique identifier for the grade. |
| `name` | `VARCHAR(50)` | `NOT NULL` | `UNIQUE` | Display name of the grade (e.g., "Kindergarten", "Grade 1"). |
| `slug` | `VARCHAR(50)` | `NOT NULL` | `UNIQUE` | URL-safe name for the grade (e.g., "kindergarten", "grade-1"). |
| `age_range` | `VARCHAR(20)` | `NOT NULL` | | Standard age group for the grade (e.g., "4-6 years", "6-7 years"). |
| `created_at` | `TIMESTAMP` | `NOT NULL` | `DEFAULT CURRENT_TIMESTAMP` | Time when the grade record was created. |

---

## 2. `subjects`
List of subjects taught across different grades (e.g., English, Maths, Science).

| Field Name | Data Type | Nullability | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `NOT NULL` | `PRIMARY KEY AUTOINCREMENT` | Unique identifier for the subject. |
| `name` | `VARCHAR(100)` | `NOT NULL` | `UNIQUE` | Display name of the subject (e.g., "Maths", "English"). |
| `slug` | `VARCHAR(100)` | `NOT NULL` | `UNIQUE` | URL-safe name for the subject (e.g., "maths", "english"). |
| `created_at` | `TIMESTAMP` | `NOT NULL` | `DEFAULT CURRENT_TIMESTAMP` | Creation time. |

---

## 3. `categories`
Grade-wise educational categories within a subject (e.g., Kindergarten > English > Alphabet).

| Field Name | Data Type | Nullability | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `NOT NULL` | `PRIMARY KEY AUTOINCREMENT` | Unique identifier for the category. |
| `grade_id` | `INT` | `NOT NULL` | `FOREIGN KEY` (references `grades.id`) | Links category to a specific grade. |
| `subject_id` | `INT` | `NOT NULL` | `FOREIGN KEY` (references `subjects.id`) | Links category to a specific subject. |
| `name` | `VARCHAR(100)` | `NOT NULL` | | Display name of the category (e.g., "Phonics", "Fractions"). |
| `slug` | `VARCHAR(100)` | `NOT NULL` | `UNIQUE` | URL-safe slug for navigation (e.g., "kindergarten-phonics"). |
| `description` | `TEXT` | `NULL` | | Explanation of what this category teaches. |
| `created_at` | `TIMESTAMP` | `NOT NULL` | `DEFAULT CURRENT_TIMESTAMP` | Creation time. |

---

## 4. `users`
Profiles for site administrators, teachers, and parents who buy or download worksheets.

| Field Name | Data Type | Nullability | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `NOT NULL` | `PRIMARY KEY AUTOINCREMENT` | Unique identifier for the user. |
| `name` | `VARCHAR(150)` | `NOT NULL` | | Full name of the user. |
| `email` | `VARCHAR(255)` | `NOT NULL` | `UNIQUE` | Email address, used for login credentials. |
| `password_hash` | `VARCHAR(255)` | `NOT NULL` | | Secured cryptographically-hashed password. |
| `role` | `VARCHAR(50)` | `NOT NULL` | `DEFAULT 'parent'` | User role: `'parent'`, `'teacher'`, or `'admin'`. |
| `created_at` | `TIMESTAMP` | `NOT NULL` | `DEFAULT CURRENT_TIMESTAMP` | Account registration time. |
| `updated_at` | `TIMESTAMP` | `NOT NULL` | `DEFAULT CURRENT_TIMESTAMP` | Account modification time. |

---

## 5. `worksheets`
Individual worksheets metadata.

| Field Name | Data Type | Nullability | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `NOT NULL` | `PRIMARY KEY AUTOINCREMENT` | Unique identifier for the worksheet. |
| `title` | `VARCHAR(255)` | `NOT NULL` | | Title of the worksheet. |
| `description` | `TEXT` | `NULL` | | Explanation of worksheet activities. |
| `grade_id` | `INT` | `NOT NULL` | `FOREIGN KEY` (references `grades.id`) | Associated grade. |
| `subject_id` | `INT` | `NOT NULL` | `FOREIGN KEY` (references `subjects.id`) | Associated subject. |
| `category_id` | `INT` | `NOT NULL` | `FOREIGN KEY` (references `categories.id`) | Associated category. |
| `age_group` | `VARCHAR(20)` | `NOT NULL` | | Suggested age range (e.g., "5-6 years"). |
| `difficulty` | `VARCHAR(50)` | `NOT NULL` | `DEFAULT 'Medium'` | Difficulty: `'Easy'`, `'Medium'`, `'Hard'`. |
| `file_path` | `VARCHAR(512)` | `NOT NULL` | | Relative URL/path to the HTML interactive template. |
| `pdf_path` | `VARCHAR(512)` | `NULL` | | Relative URL/path to the downloadable PDF file. |
| `thumbnail` | `VARCHAR(512)` | `NULL` | | Relative URL/path to the worksheet thumbnail. |
| `price` | `DECIMAL(10,2)` | `NOT NULL` | `DEFAULT 0.00` | Price of the worksheet (0.00 if free). |
| `is_free` | `BOOLEAN` | `NOT NULL` | `DEFAULT 0` | `1` (true) if free, `0` (false) if paid/premium. |
| `created_date` | `TIMESTAMP` | `NOT NULL` | `DEFAULT CURRENT_TIMESTAMP` | Time created in database. |
| `updated_at` | `TIMESTAMP` | `NOT NULL` | `DEFAULT CURRENT_TIMESTAMP` | Time updated in database. |

---

## 6. `products`
Worksheet bundles or digital products made available for sale.

| Field Name | Data Type | Nullability | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `NOT NULL` | `PRIMARY KEY AUTOINCREMENT` | Unique identifier for the product. |
| `title` | `VARCHAR(255)` | `NOT NULL` | | Name of the product or bundle. |
| `description` | `TEXT` | `NULL` | | Product details. |
| `price` | `DECIMAL(10,2)` | `NOT NULL` | `DEFAULT 0.00` | Sale price. |
| `product_type` | `VARCHAR(100)` | `NOT NULL` | `DEFAULT 'bundle'` | Type: `'bundle'`, `'single'`, or `'subscription'`. |
| `thumbnail` | `VARCHAR(512)` | `NULL` | | Path to the cover image of the product. |
| `created_at` | `TIMESTAMP` | `NOT NULL` | `DEFAULT CURRENT_TIMESTAMP` | Creation date. |
| `updated_at` | `TIMESTAMP` | `NOT NULL` | `DEFAULT CURRENT_TIMESTAMP` | Modification date. |

---

## 7. `product_worksheets`
Many-to-Many bridge table connecting worksheets to product bundles.

| Field Name | Data Type | Nullability | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `product_id` | `INT` | `NOT NULL` | `PRIMARY KEY`, `FOREIGN KEY` (references `products.id`) | Associated product. |
| `worksheet_id` | `INT` | `NOT NULL` | `PRIMARY KEY`, `FOREIGN KEY` (references `worksheets.id`) | Associated worksheet. |

---

## 8. `orders`
Logs customer payments and download cart status.

| Field Name | Data Type | Nullability | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `NOT NULL` | `PRIMARY KEY AUTOINCREMENT` | Unique transaction ID. |
| `user_id` | `INT` | `NOT NULL` | `FOREIGN KEY` (references `users.id`) | Buyer's user ID. |
| `total_amount` | `DECIMAL(10,2)` | `NOT NULL` | | Total order amount paid. |
| `payment_status`| `VARCHAR(50)` | `NOT NULL` | `DEFAULT 'pending'` | Status: `'pending'`, `'completed'`, `'failed'`, `'refunded'`. |
| `created_at` | `TIMESTAMP` | `NOT NULL` | `DEFAULT CURRENT_TIMESTAMP` | Transaction execution time. |

---

## 9. `order_items`
Individual items purchased within an order.

| Field Name | Data Type | Nullability | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `NOT NULL` | `PRIMARY KEY AUTOINCREMENT` | Line item ID. |
| `order_id` | `INT` | `NOT NULL` | `FOREIGN KEY` (references `orders.id`) | Parent order. |
| `product_id` | `INT` | `NULL` | `FOREIGN KEY` (references `products.id`) | Purchased product (if it is a bundle). |
| `worksheet_id` | `INT` | `NULL` | `FOREIGN KEY` (references `worksheets.id`) | Purchased worksheet (if it is a single file). |
| `price` | `DECIMAL(10,2)` | `NOT NULL` | | Item price at time of purchase. |

---

## 10. `blog_posts`
Stores editorial content, resources, and activity ideas for teachers and parents.

| Field Name | Data Type | Nullability | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `NOT NULL` | `PRIMARY KEY AUTOINCREMENT` | Unique post ID. |
| `title` | `VARCHAR(255)` | `NOT NULL` | | Blog post title. |
| `content` | `TEXT` | `NOT NULL` | | Blog body content (HTML or Markdown). |
| `author_id` | `INT` | `NOT NULL` | `FOREIGN KEY` (references `users.id`) | Writer ID (must be admin or teacher). |
| `thumbnail` | `VARCHAR(512)` | `NULL` | | Cover image URL. |
| `status` | `VARCHAR(50)` | `NOT NULL` | `DEFAULT 'draft'` | Publication status: `'draft'` or `'published'`. |
| `published_date`| `TIMESTAMP` | `NULL` | | Public release date. |
| `created_at` | `TIMESTAMP` | `NOT NULL` | `DEFAULT CURRENT_TIMESTAMP` | Original write date. |
| `updated_at` | `TIMESTAMP` | `NOT NULL` | `DEFAULT CURRENT_TIMESTAMP` | Last updated date. |
