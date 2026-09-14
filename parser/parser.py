import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'database': 'pyaterochka'
}

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

cache = {
    'category': {},
    'subcategory': {},
    'group': {},
    'type': {},
    'brand': {},
    'unit': {}
}

def get_or_create(table, name_field, name_value, extra_fields=None, extra_values=None):
    """Возвращает ID записи, создаёт, если её нет."""
    if name_value in cache[table]:
        return cache[table][name_value]
    fields = [name_field] + (extra_fields or [])
    values = [name_value] + (extra_values or [])
    placeholders = ', '.join(['%s'] * len(values))
    sql = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})"
    cursor.execute(sql, values)
    conn.commit()
    new_id = cursor.lastrowid
    cache[table][name_value] = new_id
    return new_id

current_category = None
current_subcategory = None
current_group = None
current_type = None

with open('parsed_data.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip()
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip())
        content = line.strip()

        # Категория
        if content.startswith('КАТЕГОРИЯ:'):
            name = content.replace('КАТЕГОРИЯ:', '').strip()
            current_category = get_or_create('categories', 'name', name)
            current_subcategory = current_group = current_type = None

        # Подкатегория
        elif content.startswith('ПОДКАТЕГОРИЯ:'):
            name = content.replace('ПОДКАТЕГОРИЯ:', '').strip()
            current_subcategory = get_or_create(
                'subcategories', 'name', name,
                ['category_id'], [current_category]
            )
            current_group = current_type = None

        # Группа
        elif content.startswith('ГРУППА:'):
            name = content.replace('ГРУППА:', '').strip()
            current_group = get_or_create(
                'product_groups', 'name', name,
                ['subcategory_id'], [current_subcategory]
            )
            current_type = None

        # Вид
        elif content.startswith('ВИД:'):
            name = content.replace('ВИД:', '').strip()
            current_type = get_or_create(
                'product_types', 'name', name,
                ['group_id'], [current_group]
            )

        # Бренд
        elif content.startswith('БРЕНД:'):
            brand_name = content.replace('БРЕНД:', '').strip()
            current_brand = get_or_create('brands', 'name', brand_name)

        # Единица
        elif content.startswith('ЕДИНИЦА:'):
            unit_name = content.replace('ЕДИНИЦА:', '').strip()
            current_unit = get_or_create('units', 'name', unit_name)

        # Товар
        elif content.startswith('ТОВАР:'):
            data = content.replace('ТОВАР:', '').strip().split('|')
            if len(data) != 6:
                print(f"Пропущена строка (неверный формат): {content}")
                continue
            name = data[0].strip()
            weight = float(data[1].strip())
            price = float(data[2].strip())
            cost = float(data[3].strip())
            nds = float(data[4].strip())
            barcode = data[5].strip()

            sql = """
                INSERT INTO products 
                (type_id, brand_id, unit_id, name, weight_volume, price, cost, nds, barcode)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                current_type, current_brand, current_unit,
                name, weight, price, cost, nds, barcode
            ))
            conn.commit()

print("Готово! Данные залиты.")
cursor.close()
conn.close()