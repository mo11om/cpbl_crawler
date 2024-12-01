import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 設定 WebDriver

def crawler_news_with_driver(driver):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "date"))
        )

        # time.sleep(2)
        # 在新頁面進行一些操作
        # 定位包含標題的元素
        title_element = driver.find_element(By.CSS_SELECTOR, ".articleTitle span")

        # 擷取文字內容
        title_text = title_element.text
        print(title_text) 
        # Find the specific element using Selenium
        post_info_element = driver.find_element(By.CSS_SELECTOR, ".post_info")

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(post_info_element.get_attribute('innerHTML'), 'html.parser')

        # Extract the date text
        date_text = soup.find('span', {'class': 'date'}).text

        print(date_text)  # Output: 2024/10/07

        # 定位包含文字的 div 元素
        content_div = driver.find_element(By.CSS_SELECTOR, "div.content.dev-xew-block")

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(content_div.get_attribute('innerHTML'), 'html.parser')

        # 找到所有 p 標籤
        paragraphs = soup.find_all('p')

        # 提取並合併所有 p 標籤的文字
        all_text = ""
        for paragraph in paragraphs:
            all_text += paragraph.text

        print(all_text)
        data_dict = {
            "date": date_text,
            "title": title_text,
            "content": all_text
        }
        return data_dict




def new_crawler_main(news_uri="https://www.cpbl.com.tw/box/news?year=2024&kindCode=A&gameSno=266"):
    
    driver = webdriver.Firefox()
    driver.get(news_uri)
    news_data=crawler_news_with_driver(driver)
    #print(news_data)
    driver.quit()
    return news_data

if __name__ == '__main__':
    uri="https://www.cpbl.com.tw"+ "/xmdoc/cont?bdate=2019-03-23&edate=2019-10-05&sid=0L132506962281105048"
    new_crawler_main(uri)
