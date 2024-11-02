from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
#import crawler news func
from news import new_crawler_main

# 設定 WebDriver
driver = webdriver.Chrome()  
driver.get("https://www.cpbl.com.tw/box/live?gameSno=214&year=2024&kindCode=A")  # 初始頁面網址

# 用於儲存所有比賽的資料
data = []
total_num_games = 498
now_num_games = 1

# 等待頁面載入並抓取各標示的內容
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "date"))
)

while now_num_games < total_num_games + 1: 
    # 抓取所有比賽的 li 元素，因為同一天可能有超過一場的比賽
    li_elements = driver.find_elements(By.CSS_SELECTOR, "div.game_list ul li a")
    num_games = len(li_elements)

    # 抓取所有比賽的狀態
    game_status = driver.find_elements(By.CSS_SELECTOR, "div.game_list .Tags span")

    # 反向遍歷每場比賽
    for game_index in range(num_games - 1, -1, -1):
        print("now_num_games", now_num_games)
        try: 
            game_tags = driver.find_elements(By.CSS_SELECTOR, ".Tags .tag.game_status span, .Tags .tag.game_note span")
            current_status = game_tags[game_index].text.strip() 

            if "延賽" in current_status: 
                continue

            li_elements = driver.find_elements(By.CSS_SELECTOR, "div.game_list ul li a")
            game_element = li_elements[game_index]
            # 點選對應的比賽
            game_element.click()  
            time.sleep(2)  # 等待頁面加載
            
            # 重新獲取需要的元素
            date = driver.find_element(By.CLASS_NAME, "date").text.strip() 
            day = driver.find_element(By.CSS_SELECTOR, ".date_selected .day").text.strip()  

             # 抓new
            news_data = {
                    "date": None,
                    "title": None,
                    "content": None
                }
           
            
            # 主客隊最終比分
            score_away = driver.find_element(By.CSS_SELECTOR, ".item.ScoreBoard .team.away .score").text.strip() 
            score_home = driver.find_element(By.CSS_SELECTOR, ".item.ScoreBoard .team.home .score").text.strip()
            # 主客隊名稱
            team_element = driver.find_element(By.CSS_SELECTOR, ".team.away a")  
            team_away_name = team_element.get_attribute("title").strip()  
            team_element = driver.find_element(By.CSS_SELECTOR, ".team.home a")  
            team_home_name = team_element.get_attribute("title").strip() 

            # 主客隊目前勝敗場
            team_away_wl = driver.find_element(By.CSS_SELECTOR, ".team.away .w-l-t").text.strip() 
            team_home_wl = driver.find_element(By.CSS_SELECTOR, ".team.home .w-l-t").text.strip()

            # MVP
            mvp_name = driver.find_element(By.CSS_SELECTOR, ".item.MVP .name a").text.strip()
            li_elements = driver.find_elements(By.CSS_SELECTOR, "ul.record li")
            span_elements = driver.find_elements(By.CSS_SELECTOR, "ul.record .count")
            # 獲取第二個 li 的文本
            second_li_text = li_elements[1].text.strip()  
            # 使用第二個 li 的文本判斷是否為投手
            if "投球" in second_li_text: 
                is_pitcher = True
                annual_selection_count = span_elements[0].text.strip() # MVP次數
                innings_pitched = span_elements[1].text.strip()  # 投球局數
                strikeouts = span_elements[2].text.strip()  # 奪三振數
                earned_runs = span_elements[3].text.strip()  # 失分數
                # 設定打擊統計為 None
                at_bats = runs_batted_in = runs_scored = hits = home_runs = None
            else:
                is_pitcher = False
                annual_selection_count = span_elements[0].text.strip() # MVP次數
                at_bats = span_elements[1].text.strip()  # 打數
                runs_batted_in = span_elements[2].text.strip()  # 打點
                runs_scored = span_elements[3].text.strip()  # 得分
                hits = span_elements[4].text.strip()  # 安打
                home_runs = span_elements[5].text.strip()  # 全壘打
                # 設定投球統計為 None
                innings_pitched = strikeouts = earned_runs = None

            # 獲取局數
            inning_group = driver.find_element(By.CSS_SELECTOR, "div.InningPlaysGroup")
            li_elements = inning_group.find_elements(By.TAG_NAME, "li")
            # 根據 li 的數量來確定局數
            num_innings = len(li_elements)

            # 初始化局資料
            all_plays = []

            for inning in range(1, num_innings + 1):
                # 上半局
                inning_header = driver.find_element(By.CSS_SELECTOR, ".InningPlaysGroup .top .title").text.strip()

                top_half = {
                    "offense_team": team_away_name,
                    "inning": f"{inning}上",
                    "records": []
                }

                # 該半局每個棒次的打擊資訊
                plays = driver.find_elements(By.CSS_SELECTOR, ".InningPlaysGroup .top .item.play")
        
                for play in plays:
                    player = play.find_element(By.CSS_SELECTOR, 'div.player span').text.strip()
                    desc = play.find_element(By.CSS_SELECTOR, 'div.desc').text.strip()
                    away_score = play.find_element(By.CSS_SELECTOR, 'div.num.away').text.strip()
                    home_score = play.find_element(By.CSS_SELECTOR, 'div.num.home').text.strip()
                    
                    record = {
                        "player": player,
                        "desc": desc,
                        "away_score": away_score,
                        "home_score": home_score
                    }
                    top_half["records"].append(record)
                all_plays.append(top_half)

                # 下半局
                try:
                    inning_header = driver.find_element(By.CSS_SELECTOR, ".InningPlaysGroup .bot .title").text.strip()
                
                    bot_half = {
                        "offense_team": team_home_name,
                        "inning": f"{inning}下",
                        "records": []
                    }
                    
                    plays = driver.find_elements(By.CSS_SELECTOR, ".InningPlaysGroup .bot .item.play")
                    
                    for play in plays:
                        player = play.find_element(By.CSS_SELECTOR, 'div.player span').text.strip()
                        desc = play.find_element(By.CSS_SELECTOR, 'div.desc').text.strip()
                        away_score = play.find_element(By.CSS_SELECTOR, 'div.num.away').text.strip()
                        home_score = play.find_element(By.CSS_SELECTOR, 'div.num.home').text.strip()
                        
                        record = {
                            "player": player,
                            "desc": desc,
                            "away_score": away_score,
                            "home_score": home_score
                        }
                        bot_half["records"].append(record)

                    all_plays.append(bot_half)

                    # 獲取所有的 li 元素（局數）
                    li_elements = driver.find_elements(By.CSS_SELECTOR, ".tab_cont.all_plays.active .tabs li")
                    # 如果當前的局數小於總局數則點選下一局
                    if inning < len(li_elements):  
                        next_button = driver.find_elements(By.CSS_SELECTOR, ".tab_cont.all_plays.active .tabs li a")[inning]
                        # driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                        driver.execute_script("arguments[0].click();", next_button)

                except Exception as e:
                    print(f"沒有下半局")
                    break

            try :
                # 點擊連結，進入新頁面
                link_element = driver.find_element(By.LINK_TEXT, "賽事新聞")
                link_uri = link_element.get_attribute("href")
                print("news_link",link_element)
                news_data=new_crawler_main(link_uri)
                
            except :
                print("Link '賽事新聞' not found.")
               
                print("news not exist")
        
            # 儲存本場比賽資料
            game_data = {
                "date": date,
                "day": day, 
                "score_away": score_away,
                "score_home": score_home,
                "team_away_name": team_away_name,
                "team_home_name": team_home_name,
                "team_away_wl": team_away_wl,
                "team_home_wl": team_home_wl,
                "mvp": {
                    "球員姓名": mvp_name,
                    "當年度獲選次數": annual_selection_count,
                    "投球統計" if is_pitcher else "打擊統計": {
                    "投球局數": innings_pitched,
                    "奪三振數": strikeouts,
                    "失分數": earned_runs,
                    "打數": at_bats,
                    "打點": runs_batted_in,
                    "得分": runs_scored,
                    "安打": hits,
                    "全壘打": home_runs,
                    }
                },
                "all_plays": all_plays,
               "news":news_data
            }
            data.append(game_data)
            print(f"已擷取比賽資料: {game_data}")
            now_num_games += 1

        except Exception as e:
            print(f"錯誤: {e}")
    try:
        # 找到並點擊「上一場」按鈕，因為是倒著抓
        last_game_button = driver.find_element(By.CLASS_NAME, "prev")
        driver.execute_script("arguments[0].click();", last_game_button)
        time.sleep(2)
    except Exception as e:
        print(f"錯誤: {e}")
        print("無法找到上一場按鈕，或已達最後一場比賽，停止爬取。")
        break


# 關閉瀏覽器
driver.quit()

# 指定文件路徑
file_path = "./data.json"

# 將資料存成 JSON 格式
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("爬取完成，已儲存至 data.json")
