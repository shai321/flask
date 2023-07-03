import json
import re
import time
from urllib.parse import urljoin
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from gtts import gTTS

def india_mart_scraper():
    driver = webdriver.Firefox()
    driver.get("https://www.indiamart.com/")

    time.sleep(2)
    try:
        checkbox = driver.find_element(
            By.XPATH, "div[@class='recaptcha-checkbox-spinner']"
        )
        checkbox.click()
    except:
        pass
    search_product_name = []
    for search_product in driver.find_elements(
        By.XPATH, "//div[@class='product-meta']//h3"
    ):
        search_product_name.append(search_product.text)
    try:
        for search in search_product_name:
            time.sleep(2)
            driver.get("https://www.indiamart.com/")
            time.sleep(2)
            driver.refresh()
            time.sleep(5)
            search_box = driver.find_element(By.ID, 'search-input')
            search_box.send_keys(search)
            time.sleep(5)
            search_button=driver.find_element(By.ID, 'searchBtn')
            search_button.click()

            time.sleep(4)
            product_link_list = []
            product_link = driver.find_elements(
                By.XPATH,
                "//div[@class='prd-list-name pn-trgt flx100']//span[@class='elps elps2 p10b0 fs14 tac mListNme']//a[@href]",
            )
            time.sleep(3)
            for i in product_link:
                product_link_list.append(i.get_attribute("href"))
            
            product_data = []
            try:
                for url in product_link_list:
                    time.sleep(3)
                    driver.get(url)
                    pro_name = {}
                    try:
                        product_name = driver.find_element(
                            By.XPATH, "//h1[@class='bo center-heading']"
                        ).text
                        pro_name["product_name"] = product_name
                    except:
                        if checkbox:
                            checkbox.click()
                        else:
                            pass
                    time.sleep(2)
                    try:
                        seller_name = driver.find_element(
                            By.XPATH, "//div[@class='pt8 color1']//div[@id='supp_nm']"
                        ).text
                        pro_name["seller_name"] = seller_name
                    except:
                        if checkbox:
                            checkbox.click()
                        else:
                            pass
                    time.sleep(2)
                    try:
                        seller_address = driver.find_element(
                            By.XPATH, "//span[@class='color1 dcell verT fs13']"
                        ).text
                        pro_name["seller_address"] = seller_address
                    except:
                        if checkbox:
                            checkbox.click()
                        else:
                            pass

                    try:
                        company_website_link = driver.find_element(
                            By.XPATH, "//div[@class='mt5']//div//a[@href]"
                        ).text
                        pro_name["company_website_link"] = company_website_link
                    except:
                        if checkbox:
                            checkbox.click()
                        else:
                            pass

                    try:
                        product_description = driver.find_element(
                            By.XPATH, "//div[@class='fs16 lh28 pdpCtsr']"
                        ).text
                        pro_name["product_description"] = product_description
                    except:
                        if checkbox:
                            checkbox.click()
                        else:
                            pass
                    print(pro_name)
                    try:
                        company = []

                        for company_details in driver.find_elements(
                            By.XPATH,
                            "//div[@class='f16 color6']//div[@class='lh21 pdinb wid3 mb20 verT']//span[@class='on color7']",
                        ):
                            company_details_name = company_details.text

                            company_details_value = company_details.find_element(
                                By.XPATH,
                                "./following-sibling::span"   # Use relative XPath expression

                            ).text
                            company.append(
                                {company_details_name: company_details_value}
                            )
                    except:
                        if checkbox:
                            checkbox.click()
                        else:
                            pass

                    try:
                        product = []
                        for product_details in driver.find_elements(
                            By.XPATH,
                            "//div[@class='dtlsec1']//table//tr//td[@class='tdwdt']",
                        ):
                            product_details_name = product_details.text

                            product_details_value = product_details.find_element(
                                By.XPATH,
                                "//td[@class='tdwdt1 color6']"
                                # "./following-sibling::td"   # Use relative XPath expression

                            ).text
                            product.append(
                                {product_details_name: product_details_value}
                            )
                    except:
                        if checkbox:
                            checkbox.click()
                        else:
                            pass

                    try:
                        product_video_url = []
                        video_url = driver.find_elements(
                            By.XPATH,
                            "//div[@class='pdVdmn']//div//div[@class='bxs videoWrapper']//iframe",
                        )
                        for product_video in video_url:
                            video = product_video.get_attribute("src")
                            product_video_url.append(video)
                    except:
                        if checkbox:
                            checkbox.click()
                        else:
                            pass

                    try:
                        product_img_url = []
                        image_elements = driver.find_elements(
                            By.XPATH,
                            "//div[@class='color dtbl pr wful bxs pdtsp pwdf']//div[@class='wid1 dcell verT pr bxs']//div[@class='bdr1 pdppro-img']//img",
                        )
                        for image_element in image_elements:
                            image = image_element.get_attribute("data-gzoom")
                            if image.startswith("https:"):
                                product_img_url.append(image)
                            else:
                                product_img_url.append("https:" + image)

                    except:
                        if checkbox:
                            checkbox.click()
                        else:
                            pass

                    breakpoint()
                    product_data.append(
                        {
                            "product_name": product_name,
                            "seller_name": seller_name,
                            "seller_address": seller_address,
                            "company_website_link": company_website_link,
                            "product_description": product_description,
                            "company_details": json.dumps({
                                k: v for d in company for k, v in d.items()
                            }),
                            "product_details": json.dumps({
                                k: v for d in product for k, v in d.items()
                            }),
                            "product_img_url": product_img_url,
                            "product_video_url": product_video_url,
                        }
                    )
            except:
                pass

                df = pd.DataFrame(product_data)
                df.to_csv("product_data_details_3.csv", mode="a", index=False)

    except:
        pass


india_mart_scraper()

# key = [
#     "product_name",
#     "seller_name",
#     "seller_address",
#     "company_website_link",
#     "product_description",
#     "product_img_url",
#     "product_video_url",
#     "Year of Establishment",
#     "Legal Status of Firm",
#     "Nature of Business",
#     "Number of Employees",
#     "Annual Turnover",
#     "IndiaMART Member Since",
#     "GST",
#     "Import Export Code (IEC)",
#     "Exports to",
#     "Brand",
#     "Type",
#     "Grade",
#     "Material",
#     "Usage/Application",
#     "Carbon Equivalent",
#     "Minimum Order Quantity",
#     "Fabric Type",
#     "Width",
#     "Pattern",
#     "GSM",
#     "Color",
# ]

 # speech = gTTS(text="extracted_message")
    # speech.save('static/speech.wav')

    # #//input[@id='audio-response']

    # driver.find_element(By.XPATH, "//div[@class='button-holder audio-button-holder']//button[@id='recaptcha-audio-button']").click()
    # audio = driver.find_element(By.XPATH, "//audio[@id='audio-source'][@src]")
    # audio_url = audio.get_attribute("src")
    # print(audio_url)