from bs4 import BeautifulSoup as bs
import lxml
import requests
import pymongo
import re

# расшифровка cruwl запроса при заходе на сайт и копирование всех значений https://curlconverter.com/python/
# леруа блочит парсер после каждых примерно 5 запросов, в таком случаи cookies и headers нужно обновлять
cookies = {
    'uid_experiment': 'cd407272-8c4c-441e-b104-08368ba9d02e',
    'dummy_aa_test': 'A',
    'disp_react_aa': '1',
    'ggr-widget-test': '0',
    '_ym_uid': '1677679770580494843',
    '_ym_d': '1677679770',
    'st_uid': '2cb8b9441060870a2c2eddbe6551f198',
    'cookie_accepted': 'true',
    'iap.uid': '7474f437082c4c028fe812d52fec15de',
    'tmr_lvid': '71b89d3ec5c933ac89541577e5f72e85',
    'tmr_lvidTS': '1677679770524',
    'aplaut_distinct_id': 'Ce6l16HgTaTj',
    '___dmpkit___': '58a4ea12-c393-4933-95b3-50f4f37c1ea4',
    'uxs_uid': 'af4aeb10-b83a-11ed-ade9-4b86d9598df0',
    'adrcid': 'AASsHI82ZEx-nx6fbRhWTEQ',
    '_gid': 'GA1.2.1288056980.1677679771',
    '_showSberPay': 'true',
    '_pickupMapSearch': 'true',
    'sawOPH': 'true',
    'GACookieStorage': 'GA1.2.776087419.1677679771',
    '_ym_isad': '2',
    'qrator_jsid': '1677829343.996.WVcecAL0POtzy1Hr-v83dvve1jrcmr5lks0amukl2cqtjo69e',
    'X-API-Experiments-sub': 'B',
    '_regionID': '34',
    '_ga': 'GA1.2.776087419.1677679771',
    'tmr_detect': '0%7C1677831592065',
    '_ga_Z72HLV7H6T': 'GS1.1.1677824458.3.1.1677831658.0.0.0',
}

headers = {
    'authority': 'leroymerlin.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ru,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'uid_experiment=cd407272-8c4c-441e-b104-08368ba9d02e; dummy_aa_test=A; disp_react_aa=1; ggr-widget-test=0; _ym_uid=1677679770580494843; _ym_d=1677679770; st_uid=2cb8b9441060870a2c2eddbe6551f198; cookie_accepted=true; iap.uid=7474f437082c4c028fe812d52fec15de; tmr_lvid=71b89d3ec5c933ac89541577e5f72e85; tmr_lvidTS=1677679770524; aplaut_distinct_id=Ce6l16HgTaTj; ___dmpkit___=58a4ea12-c393-4933-95b3-50f4f37c1ea4; uxs_uid=af4aeb10-b83a-11ed-ade9-4b86d9598df0; adrcid=AASsHI82ZEx-nx6fbRhWTEQ; _gid=GA1.2.1288056980.1677679771; _showSberPay=true; _pickupMapSearch=true; sawOPH=true; GACookieStorage=GA1.2.776087419.1677679771; _ym_isad=2; qrator_jsid=1677829343.996.WVcecAL0POtzy1Hr-v83dvve1jrcmr5lks0amukl2cqtjo69e; X-API-Experiments-sub=B; _regionID=34; _ga=GA1.2.776087419.1677679771; tmr_detect=0%7C1677831592065; _ga_Z72HLV7H6T=GS1.1.1677824458.3.1.1677831658.0.0.0',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.3.949 Yowser/2.5 Safari/537.36',
}

# сдесь будут лежать блоки товара //div[contains(@class, "phytpj4_plp largeCard")]
block_of_product = []

# монго клиент куда будут дампиться данные
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['leroymerlin'].stolyarnye_izdeliya

# парс блоков
for number in range(1, 5):
    params = {'page': f'{number}', }
    response = requests.get('https://leroymerlin.ru/catalogue/stolyarnye-izdeliya/', params=params, cookies=cookies, headers=headers)
    dom = bs(response.text, 'lxml')
    print(f"Cтраница {number} получена")
    block = dom.find_all('div', {'class': "phytpj4_plp largeCard"})
    block_of_product += block
    print(block)
    print(f"Блоки со страницы {number} получены")

# разбор каждого блока
for block in block_of_product:
    # цена формата 1, за штуку.
    if block.find('div', {'class': "n1s0vz55_plp"}):
        price = block.find('span', {'class': "_3rC-Ot1yr4_plp _1pNwL6sJc8_plp nfh3x0v_plp"}).text
        desc_of_price = block.find('span', {'class': "_3rC-Ot1yr4_plp _2HXHNcAG4G_plp n5lsd7o_plp _1w5oEIwicR_plp"}).text
    else:
        price = block.find('p', {'class': "t3y6ha_plp xc1n09g_plp p1q9hgmc_plp"}).text
        desc_of_price = block.find('p', {'class': "t3y6ha_plp x9a98_plp pb3lgg7_plp"}).text
    price = re.sub(r',', '.', price)
    price = re.sub(r'\xa0', '', price)

    # цена формата 2, за покрываюмую поверхность.
    price_for_square_list = block.find_all('p', {'class': "t3y6ha_plp s1dis8vt_plp"})
    if price_for_square_list:
        desc_of_price_price_for_square = price_for_square_list[1].text
        price_for_square = price_for_square_list[0].text
        price_for_square = re.sub(r',', '.', price_for_square)
        price_for_square = re.sub(r'\xa0', '', price_for_square)
    else:
        desc_of_price_price_for_square = "NULL"
        price_for_square = 0

    # описание товара, сылка, сылка на пикчу товара
    description = block.find('span', {'class': "t9jup0e_plp p1h8lbu4_plp"}).text
    href = block.find('a', {'class': "bex6mjh_plp b1f5t594_plp p5y548z_plp pblwt5z_plp nf842wf_plp"}).get('href')
    img = block.find('img', {'class': "p1g8n69v_plp"}).get('src')

    #дамп в базу
    db.insert_one({"name": description, "img_link": img, "price": float(price), "grade": desc_of_price, "price_2": (float(price_for_square), desc_of_price_price_for_square)})