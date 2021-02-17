"""Парсим СПБбиржу."""


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
# import json
# import os

# Путь для сохранения
# os.chdir(r'C:\Users')

headers = {"accept": "*/*",
           "user-agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:84.0) Gecko/20100101 Firefox/84.0"
           }
url = 'https://spbexchange.ru/ru/stocks/inostrannye/Instruments.aspx'
req = requests.get (url, headers = headers, stream = True)
rows = req.text
soup_header = BeautifulSoup(rows, 'lxml')

# заголовки с головной таблицы
t_header = soup_header.find('div', id="ctl00_BXContent_iii_up").find('table', class_ ='izmen_info').find('tr').find_all('th')
table_header = []
for item_head in t_header:
    table_header.append(item_head.text)
table_header.insert(3, 'Ссылка')
table_header.extend(['эмитент', 'описание', 'сектор', 'индустрия'])
print(table_header)

driver = webdriver.Chrome ("C:\\Users\\dkd_a\\Downloads\\chromedriver_win32\\chromedriver.exe")
driver.get('https://spbexchange.ru/ru/stocks/inostrannye/Instruments.aspx')
time.sleep(3)

xpath = '/html/body/form/div[3]/div[2]/div[2]/div[3]/span/a[{}]'

table_links_one_page = []
table_body_one_page = []
table_all_one_page = []
table_links_pages = []
table_all_pages = []
df_links_pages = pd.DataFrame()

df_all_pages = pd.DataFrame()
for number_page in range(1, 7):
    print(number_page)
    if number_page == 1:
        first = 22
        last = 24

    elif number_page == 6:
        first = 5
        last = 8

    else:
        # break
        first = 23
        last = 25

    table_links_one_list = []
    table_body_one_list = []
    table_cabinets_one_list = []
    table_all_one_list = []
    df_all_one_page = pd.DataFrame()
    df_links_one_page = pd.DataFrame()
    df_body_one_page = pd.DataFrame()
    try:
        for item_list in range(first, last): #(4, 24) next(, 25)
            time.sleep(1)
            print(item_list)
            if number_page == 7:
                xpath = '/html/body/form/div[3]/div[2]/div[2]/div[3]/span/a[8]'
                driver.find_element_by_xpath(xpath).click()
            else:
                driver.find_element_by_xpath(xpath.format(item_list)).click()
            html_page = driver.page_source
            soup = BeautifulSoup(html_page, 'lxml')

            # links
            trs = soup.find('div', id='ctl00_BXContent_iii_up').find('table', class_="izmen_info").find_all('a')
            t_links = []
            for i, link_elem in enumerate(trs):
                path = 'https://spbexchange.ru'
                t_links.append(link_elem.get('href'))
                if 'listing' in t_links[i]:
                    t_links[i] = path + t_links[i]
                else:
                    continue
            table_links_one_list = t_links
            print(table_links_one_list)
            print('g')

            t_body = soup.find('div', id="ctl00_BXContent_iii_up").find('table', class_='izmen_info').find_all('tr')[1:]
            t_one_body = []
            for body_elem in t_body:
                t_one_body.append(body_elem.text.strip().split('\n'))
            table_body_one_list = t_one_body

            table_links_one_page.extend(table_links_one_list)
            df_links_one_page = pd.DataFrame(table_links_one_page)
            print(df_links_one_page)
            df_links_one_page.to_csv('link.csv')
            print('l')

            table_body_one_page.extend(table_body_one_list)
            df_body_one_page = pd.DataFrame(table_body_one_page)
            df_body_one_page.to_csv('body.csv')

        time.sleep(3)
    except Exception as ex:
        print(ex)

table_links_pages.extend(table_links_one_page)
df_links_pages = pd.DataFrame(table_links_pages)
df_links_pages.to_csv('Links.csv')

df_1 = pd.read_csv('link.csv')['0']
df_2 = pd.read_csv('link_2.csv')['0']
print(df_1)
df_3 = list(['https://investcab.ru/ru/inmarket/torg_instruments/card.aspx?issue=7403', 'https://investcab.ru/ru/inmarket/torg_instruments/card.aspx?issue=7510', 'https://investcab.ru/ru/inmarket/torg_instruments/card.aspx?issue=7516'])
df_3 = pd.DataFrame(df_3)
df = pd.concat([df_1, df_2, df_3])
df.to_csv('all_links.csv')

table_all = []
df_cabinet = pd.DataFrame()
for index, data_elem in enumerate(df_3):

    # # Сохраняем код страницы в файл
    # headers = {"accept": "*/*",
    # "user-agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:84.0) Gecko/20100101 Firefox/84.0"
    # }
    # req = requests.get (url, headers = headers, stream = True)
    # rows = req.text
    # print(rows)
    #
    # with open("index1.html", "w", encoding='utf-8') as file:
    #     file.write(rows)

    headers = {"accept": "*/*",
               "user-agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:84.0) Gecko/20100101 Firefox/84.0"
               }
    req_html = requests.get(data_elem, headers=headers, stream=True)
    data_html = req_html.text

    with open("index1.html", "w", encoding='utf-8') as file:
        file.write(data_html)

    with open("index1.html", encoding='utf-8') as file:
        data_html = file.read()

    soup_html = BeautifulSoup(data_html, 'lxml')
    # print(soup_html)
    table_cabinets_one_list = []
    try:
        name_cabinet = soup_html.find('div', class_='row').find('h1').text.strip()
        name_cabinet = ('name' + '\n' + name_cabinet).split('\n')
    except Exception:
        name_cabinet = ['name', 'no_name']
    try:
        table_one_sector = soup_html.find('div', class_='row').find('table').find_all('td')[0:2]
        table_sector_cabinet = []
        for item in table_one_sector:
            table_sector_cabinet.append(item.text)
    except Exception:
        table_sector_cabinet = ['Сектор', 'no_sector']
    try:
        table_industry = soup_html.find('div', class_='row').find('table').find_all('tr')[5].text
        table_industry_cabinet = table_industry.strip().split('\n')
    except Exception:
        table_industry_cabinet = ['Отрасль', 'no_industry']
    try:
        description_cabinet = soup_html.find('div', id='ftcontainer').find('div').text
        description_cabinet = ('description' + '\n' + description_cabinet).strip().split('\n')
    except Exception:
        description_cabinet = ['description', 'no discription']

    table_body_cabinet = []
    try:
        table_body_cabinet.append(name_cabinet[1])
    except:
        name_cabinet = ['name', 'no_name']
    try:
        table_body_cabinet.append(table_sector_cabinet[1])
    except:
        table_sector_cabinet.append(item.text)
    try:
        table_body_cabinet.append(table_industry_cabinet[1])
    except:
        table_industry_cabinet = ['Отрасль', 'no_industry']
    try:
        table_body_cabinet.append(description_cabinet[1])
    except:
        description_cabinet = ['description', 'no discription']

    table_body_cabinet = [table_body_cabinet]
    table_cabinets_one_list.extend(table_body_cabinet)
    # print(table_cabinets_one_list)

    time.sleep(3)
    table_all.extend(table_cabinets_one_list)
    df_cabinet = pd.DataFrame(table_all)
    df_cabinet.to_csv('_All_Cabinet.csv')    
       
