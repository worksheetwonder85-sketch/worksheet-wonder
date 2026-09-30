-- Worksheet Wonder - SQL Database Schema (Relational Database Design)
-- Target: SQLite / PostgreSQL / MySQL Compatible (Standard ANSI SQL)

-- Enable foreign key support (specifically for SQLite engines)
PRAGMA foreign_keys = ON;

-- -----------------------------------------------------
-- Table: grades
-- Description: Stores grade levels from Kindergarten to Grade 6.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    slug VARCHAR(50) NOT NULL UNIQUE,
    age_range VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Table: subjects
-- Description: Stores subjects (English, Maths, Science, EVS, etc.)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Table: categories
-- Description: Stores categories mapped to grades and subjects.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade_id INT NOT NULL,
    subject_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grade_id) REFERENCES grades(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- Table: users
-- Description: Store user profiles (parents, teachers, and administrators)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'parent', -- e.g., 'parent', 'teacher', 'admin'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Table: worksheets
-- Description: Detailed metadata for worksheets.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS worksheets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    grade_id INT NOT NULL,
    subject_id INT NOT NULL,
    category_id INT NOT NULL,
    age_group VARCHAR(20) NOT NULL,
    difficulty VARCHAR(50) NOT NULL DEFAULT 'Medium', -- e.g., 'Easy', 'Medium', 'Hard'
    file_path VARCHAR(512) NOT NULL, -- Relative path to HTML template
    pdf_path VARCHAR(512), -- Relative path to printable PDF file
    thumbnail VARCHAR(512), -- Relative path to thumbnail image
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    is_free BOOLEAN NOT NULL DEFAULT 0, -- 0 for paid, 1 for free
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grade_id) REFERENCES grades(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- -----------------------------------------------------
-- Table: products
-- Description: Printable worksheet bundles, physical booklets, or items.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    product_type VARCHAR(100) NOT NULL DEFAULT 'bundle', -- 'bundle', 'single', 'subscription'
    thumbnail VARCHAR(512),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Table: product_worksheets (Many-to-Many Bridge Table)
-- Description: Links worksheets to product bundles.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS product_worksheets (
    product_id INT NOT NULL,
    worksheet_id INT NOT NULL,
    PRIMARY KEY (product_id, worksheet_id),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (worksheet_id) REFERENCES worksheets(id) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- Table: orders
-- Description: Stores customer transaction details.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_status VARCHAR(50) NOT NULL DEFAULT 'pending', -- 'pending', 'completed', 'failed', 'refunded'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
);

-- -----------------------------------------------------
-- Table: order_items
-- Description: Stores individual line items for orders.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INT NOT NULL,
    product_id INT, -- Mapped if purchasing a bundle product
    worksheet_id INT, -- Mapped if purchasing a single worksheet directly
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL,
    FOREIGN KEY (worksheet_id) REFERENCES worksheets(id) ON DELETE SET NULL
);

-- -----------------------------------------------------
-- Table: blog_posts
-- Description: Stores articles for educational blog.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS blog_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author_id INT NOT NULL,
    thumbnail VARCHAR(512),
    status VARCHAR(50) NOT NULL DEFAULT 'draft', -- 'draft', 'published'
    published_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id)
);

-- -----------------------------------------------------
-- Indexes for performance optimization (Scalable to 10,000+ worksheets)
-- -----------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_worksheets_grade_subject ON worksheets(grade_id, subject_id);
CREATE INDEX IF NOT EXISTS idx_worksheets_category ON worksheets(category_id);
CREATE INDEX IF NOT EXISTS idx_worksheets_is_free ON worksheets(is_free);
CREATE INDEX IF NOT EXISTS idx_categories_slug ON categories(slug);
CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_blog_posts_published ON blog_posts(status, published_date);
