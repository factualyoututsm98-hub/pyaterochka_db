import time
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

OUTPUT = 'parsed_data.txt'
CATEGORY_URL = 'https://5ka.ru/catalog/makarony-krupy--251C52952'
CATEGORY_NAME = 'Бакалея'
SUBCATEGORY_NAME = 'Макароны, крупы'
SCROLL_PAUSE = 2
MAX_SCROLLS = 10

driver = uc.Chrome()
driver.get(CATEGORY_URL)
time.sleep(60)

def scroll_and_collect():
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(MAX_SCROLLS):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    products = []
    cards = driver.find_elements(By.CSS_SELECTOR, '[data-qa^="product-card-"]')
    print(f"Найдено карточек: {len(cards)}")
    for card in cards:
        try:
            name = card.find_element(By.CSS_SELECTOR, '[data-qa="product-card-title"]').text.strip()
            rubles = card.find_element(By.CSS_SELECTOR, '[data-qa="price-tag-rubles"]').text.strip()
            pennies = card.find_element(By.CSS_SELECTOR, '[data-qa="price-tag-pennies"]').text.strip()
            price = f"{rubles}.{pennies}"

            ps = card.find_elements(By.TAG_NAME, 'p')
            weight = ''
            for p in ps:
                t = p.text.strip()
                if re.match(r'^\d+([.,]\d+)?\s*(г|кг|мл|л|шт)$', t):
                    weight = t
                    break

            products.append({'name': name, 'price': price, 'weight': weight})
        except Exception as e:
            print(f"Пропущена карточка: {e}")
    return products

def write_to_txt(category, subcategory, products):
    with open(OUTPUT, 'a', encoding='utf-8') as f:
        f.write(f"КАТЕГОРИЯ: {category}\n")
        f.write(f"  ПОДКАТЕГОРИЯ: {subcategory}\n")
        f.write("    ГРУППА: Разное\n")
        f.write("      ВИД: Разное\n")
        f.write("        БРЕНД: Без бренда\n")
        f.write("        ЕДИНИЦА: шт\n")
        for p in products:
            f.write(f"        ТОВАР: {p['name']} | {p['weight']} | {p['price']} | 0 | 20 | 0\n")
        f.write("\n")

if __name__ == '__main__':
    products = scroll_and_collect()
    print(f"Собрано товаров: {len(products)}")
    write_to_txt(CATEGORY_NAME, SUBCATEGORY_NAME, products)
    driver.quit()
    print("Готово! Данные в parsed_data.txt")