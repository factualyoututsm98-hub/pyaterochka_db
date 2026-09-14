CREATE DATABASE IF NOT EXISTS pyaterochka;
USE pyaterochka;

CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE subcategories (
    subcategory_id INT PRIMARY KEY AUTO_INCREMENT,
    category_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON DELETE CASCADE
);

CREATE TABLE product_groups (
    group_id INT PRIMARY KEY AUTO_INCREMENT,
    subcategory_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    FOREIGN KEY (subcategory_id) REFERENCES subcategories(subcategory_id)
        ON DELETE CASCADE
);

CREATE TABLE product_types (
    type_id INT PRIMARY KEY AUTO_INCREMENT,
    group_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    FOREIGN KEY (group_id) REFERENCES product_groups(group_id)
        ON DELETE CASCADE
);

CREATE TABLE brands (
    brand_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(100)
);

CREATE TABLE units (
    unit_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    type_id INT NOT NULL,
    brand_id INT,
    unit_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    weight_volume DECIMAL(10,3),
    price DECIMAL(10,2),
    cost DECIMAL(10,2),
    nds DECIMAL(5,2),
    barcode VARCHAR(20),
    FOREIGN KEY (type_id) REFERENCES product_types(type_id)
        ON DELETE CASCADE,
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
        ON DELETE SET NULL,
    FOREIGN KEY (unit_id) REFERENCES units(unit_id)
        ON DELETE CASCADE
);