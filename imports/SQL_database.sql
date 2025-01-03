--Creating DATABASE
CREATE DATABASE Spend_smart;
USE DATABASE Spend_smart;
-- Users Table (for secure login and account management)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Categories Table (predefined and custom spending categories)
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    category_name VARCHAR(255) NOT NULL,
    
);
-- Expenses Table (tracks user expenses)
CREATE TABLE expenses (
    expense_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL,
    category_id INT REFERENCES categories(category_id),
    payment_method VARCHAR(50) CHECK (payment_method IN ('credit card', 'cash', 'bank transfer', 'other')),
    description TEXT,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Reports Table(used for pre-recorded reports although it can be generated through expenses)
CREATE TABLE reports (
    report_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),  -- Foreign key to Users table
    report_type ENUM('daily', 'monthly', 'yearly') NOT NULL,  -- Type of report
    start_date DATE NOT NULL,  -- Start date for the report period
    end_date DATE NOT NULL,    -- End date for the report period
    report_data JSONB,  -- The actual report data stored in JSON format
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Timestamp when the report was generated
);
-- Spending Limits Table (setting for spending limits, can be based on category, period)
CREATE TABLE spending_limits (
    limit_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    category_id INT REFERENCES categories(category_id), 
    limit_amount DECIMAL(10, 2) NOT NULL,
    period ENUM('day', 'month', 'year') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
