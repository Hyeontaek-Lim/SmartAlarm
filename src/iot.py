import requests 
import re 
import time 
import csv 
import json
from bs4 import BeautifulSoup 
  

global headers 
global f 
global wr 
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'} 
  
URL = 'https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80'
key = 'qgFypBjNB4z0DucEHHFWxDooQzXBW6gDcEt1YBRwM%2FCRThAA5XB0xCn73sX9E15pc8p4rs1Q9IjEDMb9QbHLPA%3D%3D'

def get_time(BUSSTOP_ID, bus_name):
    url = 'http://api.gwangju.go.kr/json/arriveInfo?serviceKey='+key+'&BUSSTOP_ID='+BUSSTOP_ID
    data = requests.get(url).text
    parsed_data = json.loads(data)
    
    bus_list = parsed_data['BUSSTOP_LIST']
    st =""

    # print(parsed_data)
    for bus in bus_list:
        if bus['LINE_NAME'] == bus_name:
            st=""
            if bus['ARRIVE_FLAG'] =='1' or bus['ARRIVE_FLAG'] ==1:
                st = str(bus['LINE_NAME'])[2:]+'bus' + " soon"
                print(bus['LINE_NAME'] ,'곧 도착합니다.')
            else:
                st = str(bus['LINE_NAME'])[2:] +'bus '+str(bus['REMAIN_MIN'])+'minute'
                print(bus['LINE_NAME'] ,bus['REMAIN_MIN'],'분 남았습니다')
            return st
        
    return "no bus data"

def bus_data_code(bus_stop):
    url = 'http://api.gwangju.go.kr/json/stationInfo?serviceKey='+key
    data = requests.get(url).text
    parsed_data = json.loads(data)
    res = []
    print(bus_stop," 정류장 정보")
    for i in parsed_data['STATION_LIST']:
        if(i['BUSSTOP_NAME'] == bus_stop):
            temp = "다음 정류소 : ",i['NEXT_BUSSTOP'],i['BUSSTOP_ID']
            res.append(temp)
    return res

def page_url_parse(city):
    req = requests.get(URL, headers = headers)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    arr = []
    
    data = soup.find('th',text=city).parent
    for i in data.find_all('td'):
        arr.append(i.span.text)

    var = int(arr[0])
    state = ""
    if var <=30:
        state = "good"
    elif var <= 80:
        state = "normal"
    elif var<= 150:
        state = "bad"
    else:
        state = "Very Bad"

    return 'dust:'+ str(arr[0]) +' '+state



                           # print()
    # for data in body:
    #     # if data.findchildren("th") != null:
    #     for tr in data:
    #         i = 0 
    #         for test in tr:
    #             if i==0:
    #                 print("지역은", test)

    #             print(test)


    
        # print('\n')
    # body.replace("<", "")
    
    # datas = body.children()
    # children = li.findChildren("a" , recursive=False)

    # print(body)
    # for i in body.find_all('tr'):
    #     print('*')
  

    #for item in soup.find_all('#main_pack > div.content_search.section._atmospheric_environment > div > div.contents03_sub > div  > div:nth-of-type(3) > div.main_box > div.detail_box > div.tb_scroll > table > tbody'):
        

 
def main(): 
    print()
    # bus_data_code('신창중')
    # get_time("896")
    # page_url_parse() 

 
if __name__ == "__main__": 
    main() 