
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

from dataclasses import dataclass
from news import new_crawler_main
uri="https://www.cpbl.com.tw"

@dataclass 
class GameData: 
    date: str 
    score_away: str 
    score_home: str 
    team_away_name: str 
    team_home_name: str
def transform_date(date_str): 
    return date_str.replace('/', '-')

def read_json(file_path = 'data.json'):
  

    # Path to the JSON file
    

    # Read the JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file: 
        data_list = json.load(file) 
# Access the first item in the list 
    # data = data_list[0]
    for data in data_list:
        # Print the data to verify 
        pretty_data = json.dumps(data, indent=4, ensure_ascii=False) 
        # print(pretty_data)
        # Access specific fields
        date = data['date']
        day = data['day']
        score_away = data['score_away']
        score_home = data['score_home']
        team_away_name = data['team_away_name']
        team_home_name = data['team_home_name']
      
        
        # print(f"Day: {day}")
        print(f"Away Team: {team_away_name} - Score: {score_away}")
        print(f"Home Team: {team_home_name} - Score: {score_home}")
        date=transform_date(date)
        print(f"news date {data['news']['date']}")
        
        # Print specific fields
        print(f"Date: {date}")
        game_data = GameData( 
            date=date,
            score_away=data['score_away'],
                score_home=data['score_home'], 
                team_away_name=data['team_away_name'], 
                team_home_name=data['team_home_name'] ) 
        if data['news']['content']:
            generate_score_json(data['news']['content']+data['news']['title'])
        # print(game_data)
        # crawler_main(game_data)
def crawler_main(game_data:GameData):
        # 設定 WebDriver
    driver = webdriver.Firefox()

    driver.get(uri+"/xmdoc")
    # Locate the input field by its ID 
    date_input = driver.find_element(By.NAME, "BeginReleaseDate") 
    # # Input the date 
    date_input.send_keys(game_data.date) # Optionally, simulate pressing Enter if necessary date_input.send_keys(Keys.RETURN) # Close the WebDriver after a short delay import time time.sleep(5) driver.quit()
    date_input = driver.find_element(By.NAME, "EndReleaseDate") 
    # # Input the date 
    date_input.send_keys(game_data.date) # Optionally, simulate pressing Enter if necessary date_input.send_keys(Keys.RETURN) # Close the WebDriver after a short delay import time time.sleep(5) driver.quit()

    # Locate the submit button by its attributes and click it
    submit_button = driver.find_element(By.XPATH, "//input[@value='查詢']")

    submit_button.click()
    
    time.sleep(5) 
    # Get the page source and parse it with BeautifulSoup 
    soup = BeautifulSoup(driver.page_source, 'html.parser') # Find all the div elements with the class 'NewsList' 
    news_list = soup.find_all('div', class_='NewsList') # Extract all href links from the 'a' tags within the 'NewsList'
    hrefs = [] 
    for news in news_list: 
        links = news.find_all('a', href=True) 
        for link in links: hrefs.append(link['href'])
        # Print the href links 
    for href in hrefs:
       news=new_crawler_main(uri+href)
       generate_score_json(news["content"])

       print (news)
    driver.quit()

def write_file(news,file_path = "./news.json"):
    

    # 將資料存成 JSON 格式
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=4)

    print("爬取完成，已儲存至 news.json")    
    

def crawler_page_main(begin_date:str, end_date:str):
        # 設定 WebDriver
    driver = webdriver.Firefox()

    driver.get(uri+"/xmdoc")
    # Locate the input field by its ID 
    date_input = driver.find_element(By.NAME, "BeginReleaseDate") 
    # # Input the date 
    date_input.send_keys(begin_date) # Optionally, simulate pressing Enter if necessary date_input.send_keys(Keys.RETURN) # Close the WebDriver after a short delay import time time.sleep(5) driver.quit()
    date_input = driver.find_element(By.NAME, "EndReleaseDate") 
    # # Input the date 
    date_input.send_keys(end_date) # Optionally, simulate pressing Enter if necessary date_input.send_keys(Keys.RETURN) # Close the WebDriver after a short delay import time time.sleep(5) driver.quit()

    # Locate the submit button by its attributes and click it
    submit_button = driver.find_element(By.XPATH, "//input[@value='查詢']")

    submit_button.click()
    
    time.sleep(0.5) 
    # Get the page source and parse it with BeautifulSoup 
    news_data_list=[]
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser') # Find all the div elements with the class 'NewsList' 
        news_list = soup.find_all('div', class_='NewsList') # Extract all href links from the 'a' tags within the 'NewsList'
        hrefs = [] 
        for div in soup.find_all('div', class_='title'): 
            a_tag = div.find('a') 
            if a_tag and 'href' in a_tag.attrs: 
                hrefs.append(a_tag['href'])  
        # for news in news_list: 
        #     links = news.find_all('a', href=True) 
        #     for link in links: hrefs.append(link['href'])
        #     # Print the href links 
        for href in hrefs:
            news_data=new_crawler_main(uri+href)
            
            news_data_list.append(news_data)
            # generate_score_json(news["content"])

            # print (news)
# Attempt to find the 'next' button and click it 
        try: 
            next_button = driver.find_element(By.CLASS_NAME, 'next') 
            next_button.click() 
            time.sleep(0.5) # Adjust the sleep time as necessary 
        except NoSuchElementException: 
                print("No more 'next' button found.") 
                break
    driver.quit() 
    print("news content",news_data_list)
    write_file(news_data_list)    
               

if __name__ == '__main__':
    #read_json("data.json")
    # game_data = GameData( 
    # date=  "2024-10-06" ,
    # score_away= "5",
    #     score_home="3", 
    #     team_away_name="富邦", 
    #     team_home_name="統一" ) 
    # crawler_main(game_data)
    crawler_page_main("2018-03-24","2018-10-14")#2019/10/05