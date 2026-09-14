USE pyaterochka;

-- 1. Количество записей в каждой таблице
SELECT 'categories' AS table_name, COUNT(*) AS count FROM categories
UNION ALL
SELECT 'subcategories', COUNT(*) FROM subcategories
UNION ALL
SELECT 'product_groups', COUNT(*) FROM product_groups
UNION ALL
SELECT 'product_types', COUNT(*) FROM product_types
UNION ALL
SELECT 'brands', COUNT(*) FROM brands
UNION ALL
SELECT 'units', COUNT(*) FROM units
UNION ALL
SELECT 'products', COUNT(*) FROM products;

-- 2. Товары с брендами и ценами
SELECT p.product_id, p.name AS product, b.name AS brand, u.name AS unit, p.price
FROM products p
JOIN brands b ON p.brand_id = b.brand_id
JOIN units u ON p.unit_id = u.unit_id
LIMIT 20;

-- 3. Полная иерархия товаров
SELECT c.name AS category, s.name AS subcategory, g.name AS group_name, t.name AS type, p.name AS product, p.price
FROM products p
JOIN product_types t ON p.type_id = t.type_id
JOIN product_groups g ON t.group_id = g.group_id
JOIN subcategories s ON g.subcategory_id = s.subcategory_id
JOIN categories c ON s.category_id = c.category_id
LIMIT 20;

-- 4. Количество товаров в каждой категории
SELECT c.name AS category, COUNT(p.product_id) AS product_count
FROM categories c
JOIN subcategories s ON c.category_id = s.category_id
JOIN product_groups g ON s.subcategory_id = g.subcategory_id
JOIN product_types t ON g.group_id = t.group_id
JOIN products p ON t.type_id = p.type_id
GROUP BY c.name
ORDER BY product_count DESC;

-- 5. Товары дороже 500 рублей
SELECT name, price FROM products WHERE price > 500 ORDER BY price DESC;