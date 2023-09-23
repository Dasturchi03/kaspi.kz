import asyncio
import json
from pyppeteer import launch
from bs4 import BeautifulSoup


async def main(urls):
    brow = await launch(headless=True)
    page = await brow.newPage()
    cookies = [{'name': 'layout', 'value': 'd', 'domain': 'kaspi.kz', 'path': '/shop', 'expires': 1726644470.633389, 'size': 7, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'k_stat', 'value': '74791a40-1e09-45f8-a9ed-d4ec9e7b7359', 'domain': 'kaspi.kz', 'path': '/', 'expires': 1726644470.844751, 'size': 42, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'ks.tg', 'value': '84', 'domain': 'kaspi.kz', 'path': '/', 'expires': 1726644470.928354, 'size': 7, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'kaspi.storefront.cookie.city', 'value': '632210000', 'domain': 'kaspi.kz', 'path': '/', 'expires': 1726644474, 'size': 37, 'httpOnly': False, 'secure': False, 'session': False}]
    await page.setCookie(*cookies)
    for url in urls:
        # try:
            await page.goto(url)
            await page.waitFor(1000)
            cont = await page.content()
            await get_data(cont, url)
        # except Exception as err:
            # print(err)
    
    await brow.close()


async def get_data(text, url):
    soup = BeautifulSoup(text, 'lxml')
    div = soup.find('div', id='ItemView')
    h1 = soup.find('h1', class_='item__heading')
    name = h1.text.strip()
    d1 = soup.find('div', class_='item__price-once')
    print('d1', d1)
    price = d1.text.strip()
    with open('files/data.json', 'r', encoding='UTF-8') as file:
        dc = json.load(file)
    dc['data'] += {'name': name, 'price': price}
    
    with open('files/data.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(dc, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    URL = 'https://kaspi.kz/shop/p/kolosnik-chugunnyi-zota-000003kl-140x115-mm-104313443/?c=710000000'
    URL = 'https://kaspi.kz/shop/p/vsjo-v-dom-100-sht-101014392/?c=434630100'
    asyncio.get_event_loop().run_until_complete(main([URL]))

