import requests
import time

COOKIES_RAW = """
5ka_store_id=335Y;
5ka_store_id_store=35XY;
encryptedSessionId=241d6118c77c27091e8ec8409ce73193b4d3c63dcfaf1c5674a00fe4c01744e7;
server_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0b2tlbiIsInNlc3Npb25JZCI6Ijg5Yjk1Y2RkMDk2Mzc4ZWY1ZjdiMGQwMTVjN2E2NDBmOTIwN2I1YzBmNGM1NDkxNTA1NjYxYjlhY2M2YTc0MTciLCJleHAiOjE3ODk0Njk0MzUsImlhdCI6MTc4OTM4MzAzNSwianRpIjoiMmNkNDI0MWUtNWY5OC00NzhkLWI4NTQtNzEwYmEwMGNlNDYxIn0.Nw0ud4QGL3_SSH5OLToAxpswBGLywEpxyum9yQua3D0;
session_token_timestamp=1789469435604;
spid=1789383011838_9c5f06e7ad7268b03be4908409535091_75ogprimwshpde4t;
spjs=1789383011838_176c7570_0f8be3d2_5b4edc1128a17b5e551230df395a8631_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;
spsc=1789383032153_4281e4a6f956dedba14e63475c384823_6elnZ3f98nN8LEccpjxzlc3eQB3JD7adevluBXtm63syQ4Kce3ecqruwHLMwtX6fZ;
tc5_catalog_mode=delivery
"""

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://5ka.ru/',
    'Origin': 'https://5ka.ru'
}

def parse_cookie_string(raw):
    cookies = {}
    for part in raw.strip().split(';'):
        if '=' in part:
            k, v = part.strip().split('=', 1)
            cookies[k] = v
    return cookies

COOKIES = parse_cookie_string(COOKIES_RAW)

def fetch_products(category_id, offset=0, limit=12):
    url = f'https://5d.5ka.ru/api/catalog/v2/stores/35XY/categories/{category_id}/products?mode=delivery&include_restrict=true&limit={limit}&offset={offset}'
    r = requests.get(url, headers=HEADERS, cookies=COOKIES)
    if r.status_code != 200:
        print(f'HTTP {r.status_code}: {r.text[:200]}')
        return []
    data = r.json()
    return data.get('products', [])

def write_to_txt(category, subcategory, products):
    with open('parsed_data.txt', 'a', encoding='utf-8') as f:
        f.write(f"КАТЕГОРИЯ: {category}\n")
        f.write(f"  ПОДКАТЕГОРИЯ: {subcategory}\n")
        f.write("    ГРУППА: Разное\n")
        f.write("      ВИД: Разное\n")
        f.write("        БРЕНД: Без бренда\n")
        f.write("        ЕДИНИЦА: шт\n")
        for p in products:
            name = p.get('name', '').replace('|', ' ')
            price = p.get('prices', {}).get('regular', '0')
            weight = p.get('property_clarification', '') or ''
            f.write(f"        ТОВАР: {name} | {weight} | {price} | 0 | 20 | 0\n")
        f.write("\n")

if __name__ == '__main__':
    open('parsed_data.txt', 'w', encoding='utf-8').close()
    CATEGORY_ID = '251C52952'
    CATEGORY_NAME = 'Бакалея'
    SUBCATEGORY_NAME = 'Макароны, крупы'

    all_products = []
    offset = 0
    limit = 12
    while True:
        chunk = fetch_products(CATEGORY_ID, offset, limit)
        if not chunk:
            break
        all_products.extend(chunk)
        offset += limit
        time.sleep(1)

    print(f'Собрано товаров: {len(all_products)}')
    write_to_txt(CATEGORY_NAME, SUBCATEGORY_NAME, all_products)
    print('Готово.')