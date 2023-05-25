from selenium import webdriver
from bs4 import BeautifulSoup
import json

browser = webdriver.Chrome()
# browser = webdriver.Firefox()

data = []
json_data = {}
end = True
count = 1
category_link = 'https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/'
# category_link = 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/'
# category_link = 'https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/'
# category_link = 'https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/'

while end:
    dns_shop_url = f'{category_link}?p={count}'
    browser.get(dns_shop_url)
    text_data = browser.page_source
    class_ = 'catalog-product ui-button-widget'
    soup = BeautifulSoup(text_data, 'lxml')
    if len(soup.find_all('div', {'class': class_})) == 0:
        end = not end
        break
    for i in soup.find_all('div', {'class': class_}):
        data.append(i)
    count += 1


for j, i in enumerate(data):
    name = str(i.find('a', {'class': 'catalog-product__name ui-link ui-link_black'}).contents[0].text).replace('\n', '').replace('\t', '').replace('\"', '')
    link = str(f"https://www.dns-shop.ru{i.find('a')['href']}").replace('\n', '').replace('\t', '').replace('\"', '')
    link_image = str(i.find('a').find('img')['data-src']).replace('\n', '').replace('\t', '').replace('\"', '')
    rating = str(i.find('a', 'catalog-product__rating ui-link ui-link_black')['data-rating']).replace('\n', '').replace('\t', '').replace('\"', '')
    try:
        availability = str(i.find('span', 'available').text + \
                       i.find('a', 'order-avail-wrap__link ui-link ui-link_blue')['data-mobile-text']).replace('\n', '').replace('\t', '').replace('\"', '')
    except:
        availability = str(i.find('div', 'order-avail-wrap order-avail-wrap_not-avail').text).replace('\n', '').replace('\t', '').replace('\"', '')
    price = str(i.find('div', 'product-buy__price').text).replace('₽', 'A')
    price_split = price.encode('utf-8').decode('utf-8').split('A')
    price_split[0] = price_split[0].replace('\xa0', '').replace(' ', '')
    price_split[1] = price_split[1].replace('\xa0', '').replace(' ', '')
    if price_split[1] != '':
        price_with_discount = price_split[0]
        price_without_discount = price_split[1]
    else:
        price_with_discount = price_split[0]
        price_without_discount = price_split[0]
    temp_data = {
        'name': name,
        'link': link,
        'link_image': link_image,
        'price_with_discount': price_with_discount,
        'price_without_discount': price_without_discount,
        'rating': rating,
        'availability': availability,
    }
    json_data[str(j+1)] = temp_data


with open('result.json', 'w', encoding='utf8') as file:
    json.dump(json_data, file, indent=4, ensure_ascii=False)
