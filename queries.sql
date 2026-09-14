USE pyaterochka;

-- 1. Все товары с брендами и ценами
SELECT p.name AS product, b.name AS brand, p.price
FROM products p
JOIN brands b ON p.brand_id = b.brand_id;

-- 2. Количество товаров в каждой категории
SELECT c.name AS category, COUNT(p.product_id) AS product_count
FROM categories c
JOIN subcategories s ON c.category_id = s.category_id
JOIN product_groups g ON s.subcategory_id = g.subcategory_id
JOIN product_types t ON g.group_id = t.group_id
JOIN products p ON t.type_id = p.type_id
GROUP BY c.name;

-- 3. Товары дороже 150 рублей
SELECT name, price
FROM products
WHERE price > 150;