# -*- coding: utf-8 -*-
import string
import json
test_json={"content": "味全龍和富邦悍將在新莊棒球場進行補賽，本場賽事是一場保留補賽，味全概由鋼龍接替投球，富邦悍將則由陳仕朋續投，兩隊投手表現優異形成精彩的投手戰，富邦靠著池恩齊的關鍵超前安打，終場以3:1拿下比賽勝利，池恩齊也獲得生涯首座單場MVP。前五局兩隊皆無攻下分數，6局下，富邦發動攻勢，劉俊豪保送上壘，接著靠著暴投攻佔二壘，王正棠右邊方向安打送回隊友，幫助富邦率先破蛋。陳仕朋此戰接續先發任務，總計6.2局沒有失掉分數，吳世豪接替投球，劉基鴻擊出左外野方向陽春砲，為球隊追平比數。不過富邦在7局下立刻反擊，申皓瑋先擊出安打，周佳樂短打推進至二壘，池恩齊敲出關鍵安打，將領先要回，比數形成2:1。8局下再度進攻，兩出局後陳真保送上壘，戴培峰、申皓瑋串聯安打，富邦再添保險分，終場富邦就以3:1力退味全，收下比賽勝利。"}
def filter_sentences(sentences, keywords):
    """
    過濾掉包含指定關鍵字的句子

    Args:
        sentences: 一個包含句子的列表
        keywords: 要過濾的關鍵字列表

    Returns:
        一個新的列表，包含不含指定關鍵字的句子
    """

    filtered_sentences = []
    for sentence in sentences:
        if not any(keyword in sentence for keyword in keywords):
            filtered_sentences.append(sentence)
    return filtered_sentences




def tokenize(text):
  """Tokenizes a given text into words, using '，' as the primary delimiter and '。' as a secondary delimiter.

  Args:
    text: The text to tokenize.

  Returns:
    A list of tokens (words).
  """

  # Split the text based on primary delimiter '，'
  tokens = text.split("，")

  # Further split tokens based on secondary delimiter '。'
  tokens = [token.split("。") for token in tokens]

  # Flatten the list of lists into a single list of tokens
  tokens = [token for sublist in tokens for token in sublist]

  # Remove punctuation from tokens
  tokens = [token.strip(string.punctuation) for token in tokens]

  # Remove empty tokens
  tokens = [token for token in tokens if token]

  return tokens


def main(file_path = 'data.json'):
  

    # Path to the JSON file
    

    # Read the JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file: 
        data_list = json.load(file) 
# Access the first item in the list 
    for data in data_list:
        news=data['news']
        if news['content'] != None:
            processed_result=preprocess_hit(news=news)
            news['processed_result'] = processed_result
    with open("new"+file_path, 'w', encoding='utf-8') as file:
      json.dump(data_list, file, indent=4, ensure_ascii=False)

    
def preprocess_hit(news=test_json):
    content =news["content"]
    sentences=tokenize(content)

    # 過濾句子
    keywords = ["壓制","守護神","拆彈","救援","中繼","關門","投", "失", "先發", "後援","補賽"]
    result = filter_sentences(sentences, keywords)
    # # 印出結果
    # for sentence in result:
    #     print(sentence)
    print(result)
    return result
    



if __name__ == '__main__':
    main("2324例行賽資料.json")