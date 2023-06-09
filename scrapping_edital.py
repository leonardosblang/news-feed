import asyncio
from pyppeteer import launch
from typing import List, Dict


# Helper function to extract content based on type
async def get_content_for_type(element, page, selector: str, type_: str) -> str:
    val = ""
    text_ob = element
    try:
        text_ob = await element.querySelector(selector)
    except Exception as e:
        print("INFO: selector not valid - probably the parent object is the object")

    try:
        if type_ == 'TEXT':
            val = (await page.evaluate('(el) => el.textContent', text_ob)).strip()
        elif type_ == 'IMAGE':
            # Probably not complete - could also be in srcset or so....
            val = await page.evaluate('(el) => el.src', text_ob)
        elif type_ == 'LINK':
            # Probably not complete
            val = await page.evaluate('(el) => el.href', text_ob)

        return val
    except Exception as e:
        print("INFO: object not found", e)


# Function to generate a common selector
def generate_common_selector(selectors):
    arr = [s.replace(' > ', '> ').split(' ') for s in selectors]
    arr.sort()
    a1 = arr[0]
    a2 = arr[len(arr) - 1]
    L = len(a1)
    i = 0
    while i < L and a1[i] == a2[i]:
        i += 1
    return ' '.join([s.replace('>', ' >') for s in a1[:i]])


# Function to scrape data from the website
async def scrape_data(page, selectors: List[Dict]) -> List[Dict]:
    elements = await page.querySelectorAll(".tileItem")

    scraped_data = []
    for element in elements:
        data = {}
        for selector in selectors:
            data_point = await get_content_for_type(element, page, selector["selector"], selector["type"])
            if data_point:
                data[selector["name"]] = data_point
        scraped_data.append(data)

    return scraped_data

SELECTORS = [
    {"name": "title", "description": "title", "selector": ".tileHeadline a", "type": "TEXT"},
    {"name": "date", "description": "date", "selector": ".tileInfo ul > li:nth-child(3)", "type": "TEXT"},
    {"name": "time", "description": "time", "selector": ".tileInfo ul > li:nth-child(4)", "type": "TEXT"},
    {"name": "link", "description": "link", "selector": ".tileHeadline a", "type": "LINK"}
]


LINK = "https://portal.cdm.ifsuldeminas.edu.br/editais/editais-do-campus"


async def main():
    browser = await launch(
        headless=True,
        timeout=100000,
        ignoreDefaultArgs=["--enable-automation"],
        args=[],
        defaultViewport=None
    )
    page = await browser.newPage()
    await page.goto(LINK, waitUntil=["networkidle2"], timeout=15000)
    scraped_data = await scrape_data(page, SELECTORS)
    await browser.close()

    return scraped_data





