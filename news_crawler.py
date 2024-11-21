from news import new_crawler_main
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

from dataclasses import dataclass
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

def read_json():
  

    # Path to the JSON file
    file_path = 'data.json'

    # Read the JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file: 
        data_list = json.load(file) 
# Access the first item in the list 
    data = data_list[0]
    # Print the data to verify 
    pretty_data = json.dumps(data, indent=4, ensure_ascii=False) 
    print(pretty_data)
    # Access specific fields
    date = data['date']
    day = data['day']
    score_away = data['score_away']
    score_home = data['score_home']
    team_away_name = data['team_away_name']
    team_home_name = data['team_home_name']
    
    date=transform_date(date)
    # Print specific fields
    print(f"Date: {date}")
    print(f"Day: {day}")
    print(f"Away Team: {team_away_name} - Score: {score_away}")
    print(f"Home Team: {team_home_name} - Score: {score_home}")
    game_data = GameData( 
        date=date,
          score_away=data['score_away'],
            score_home=data['score_home'], 
            team_away_name=data['team_away_name'], 
            team_home_name=data['team_home_name'] ) 
    print(game_data)
    # crawler_main(game_data)
def crawler_main(game_data:GameData):
        # 設定 WebDriver
    driver = webdriver.Chrome()

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
       print (news)
    driver.quit()
if __name__ == '__main__':
    read_json()