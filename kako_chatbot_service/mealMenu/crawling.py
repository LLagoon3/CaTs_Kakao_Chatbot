import requests
from bs4 import BeautifulSoup as bs
import re
from datetime import datetime
from config.settings import CBNU_COOP_URL

class Crawling():
    def __init__(self) -> None:
        self.url = CBNU_COOP_URL
        self.headers = {"User-Agent": 
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}
    
    def requestGET(self):
        response = requests.get(CBNU_COOP_URL, headers=self.headers)
        html = bs(response.text, 'html.parser')
        return html
    
    def parsingMenu(self):
        r_index = ['한빛식당', '별빛식당', '은하수식당']
        html = self.requestGET()
        date, pattern = list(), r"(\d{1,2})\.(\d{1,2})\((\w+)\)"
        for d in html.find_all(attrs = {'class': 'weekday-title'}):
            g = re.match(pattern, d.text).groups() 
            month, day = map(int, g[:2])
            date.append([month, day, g[2]])
        
        tab_list = html.find_all(attrs = {'class': 'tab-pane in active'}) 
        for tmp in html.find_all(attrs = {'class': 'tab-pane in'}):
            tab_list.append(tmp)
        
        pattern = r'\d+(?:-\d+)*-\d+'
        menu_list = [[], [], []]
        for i, tab in enumerate(tab_list):
            tr = tab.find_all('tr')
            for j in range(2, len(tr), 2):
                label = tr[j].find(attrs = {'class': 'row-label'}).text[-4:-2]
                tmp_list = list() 
                for tmp in tr[j].find_all('td'):
                    id = re.search(pattern, str(tmp)).group() 
                    menu = html.find(attrs = {'data-table': id}) 
                    main_menu = menu.find(attrs={'class': 'card-header'})
                    side_menu = [i.text for i in menu.find_all(attrs={'class': 'side'})]
                    tmp_list.append({'label': label, 'main': main_menu.text, 'side': side_menu})
                menu_list[i].append(tmp_list)

        res = list()
        for date_count in range(0, len(date) // 3):
            dateT = str(datetime.now().year) + '-' + str(date[date_count][0]) + '-' + str(date[date_count][1])
            dateT = datetime.strptime(dateT,'%Y-%m-%d')
            for i, r in enumerate(r_index):
                for m in menu_list[i]:
                    tmpDict = dict()
                    tmpDict['date'] = dateT
                    tmpDict['time'] = m[date_count]['label']
                    tmpDict['restaurant'] = r 
                    tmpDict['menu'] = m[date_count]['main'] + ',' + ','.join(m[date_count]['side'])
                    res.append(tmpDict)
                
        # res = dict() 
        # for date_count in range(0, len(date) // 3):
        #     dateT = str(datetime.now().year) + '-' + str(date[date_count][0]) + '-' + str(date[date_count][1])
        #     # dateT = datetime.strptime(dateT,'%Y-%m-%d')
        #     tmpR = {r_index[0]: [], r_index[1]: [], r_index[2]: []}
        #     for i, r in enumerate(r_index):
        #         tmpMenu = {'아침': [], '점심': [], '저녁': []}
        #         for j, m in enumerate(menu_list[i]):
        #             tmpMenu[m[date_count]['label']] = [{'main': m[date_count]['main'], 'side': m[date_count]['side']}]
        #         tmpR[r].append(tmpMenu)
        #     res[dateT] = [tmpR]
        return res
    

'''
#### RESULT JSON ####
{'2023.12.29':[{'한빛식당':[{'아침':'휴무',
                           '점심':'휴무',
                           '저녁':'휴무'}]},
               {'별빛식당':[]}]}
'''

# c = Crawling().parsingMenu()
            
