from lxml import html
import requests

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
url = "https://lenta.ru/"
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

"//div[contains(@class, 'main-page__section')]"
path1 = "//div[contains(@class, 'topnews__column')]/a/@href"
path2 = "//div[contains(@class, 'longgrid-feature-list__box')]/a/@href"
path3 = "//div[contains(@class, 'longgrid-list__box')]/a/@href"

hrefs = dom.xpath(path1) + dom.xpath(path2) + dom.xpath(path3)

import json
with open("step1.json", "w") as f:
    json.dump(hrefs, f)

