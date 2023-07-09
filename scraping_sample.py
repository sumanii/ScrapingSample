# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import pandas as pd


def Search2ndBase(outputDir: str, fileFormat: int, view: bool):
    urlBase = "https://www.2ndbase.jp/shopbrand/ct5/"

    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.use_chromium = True

    if view == False:
        options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    pageNum = 1
    focalLength: list[int] = []
    aperture: list[float] = []
    price: list[int] = []
    while 1:
        url = urlBase+"page"+str(pageNum)+"/order/"
        driver.get(url)
        time.sleep(2)

        html = driver.page_source.encode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        categoryList = soup.find("div", attrs={"id": "r_categoryList"})
        categoryListDetails = categoryList.find_all(
            "div", attrs={"class": "detail"})

        if len(categoryListDetails) == 0:
            break

        detail: BeautifulSoup
        for detail in categoryListDetails:
            name = detail.find("p", attrs={"class": "name"}).text
            if "Super" in name:
                if "Takumar" in name:
                    priceStr = detail.find("p", attrs={"class": "price"}).text
                    print(name+" "+priceStr)

                    nameSearch = re.search(r"(\d+)mm F(\d+(?:\.\d+)?)", name)
                    priceVal = re.sub(r"\D", "", priceStr)
                    focalLength.append(int(nameSearch.groups()[0]))
                    aperture.append(float(nameSearch.groups()[1]))
                    price.append(int(priceVal))

        pageNum = pageNum+1

    resultDect = {"焦点距離": focalLength, "f値": aperture, "価格": price}
    result = pd.DataFrame(data=resultDect).sort_values(by=["焦点距離", "f値", "価格"])

    if fileFormat == 0:
        result.to_excel(outputDir+"/2ndBaseData.xlsx",
                        sheet_name="SuperTakumar", index=False)
    elif fileFormat == 1:
        result.to_csv(outputDir+"/2ndBaseData_SuperTakumar.csv",
                      index=False, encoding='utf_8_sig')

    driver.quit()


def main():
    """
    main 関数
    """

    Search2ndBase("output", 0, False)


if __name__ == "__main__":
    main()
