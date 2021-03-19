from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from pandas import DataFrame
import math
from datetime import date
import time

def get_soup(ticker, attempts=0):
    
    base_url_front = 'http://performance.morningstar.com/funds/etf/total-returns.action?t='
    base_url_back = '&region=usa&culture=en-US&ops=clear'
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver_instance = webdriver.Firefox(options=options) 
    url = base_url_front + ticker + base_url_back

    if attempts == 0:
        driver_instance.get(url)
        time.sleep(1)

    else:
        driver_instance.set_page_load_timeout(10)
        driver_instance.refresh()
        time.sleep(attempts + 1)

    response = BeautifulSoup(driver_instance.page_source.encode("utf-8"), 'html.parser')

    if response.find_all('tbody') == []:
        if attempts == 6:
            print(
                "Maximum retries attempted. Moving on."
            )
            driver_instance.quit()
            return None

        else:
            print(
                "Failure #" + str(attempts + 1) + " for " + ticker + ". Wait " + str(round(math.exp(attempts + 1)/9 + 1,2)) + " seconds. Retrying..."
            )
            driver_instance.quit()
            time.sleep(math.exp(attempts + 1)/9 + 1)
            get_soup(ticker, attempts + 1)       

    driver_instance.quit()
    return response

def extract_data(response):

    current_year = date.today().year
    tables = response.find_all('tbody')[0:2]
    data = {
        'annual': {},
        'trailing': {}
    }
    annual_rows = tables[0].find_all('tr')
    trailing_rows = tables[1].find_all('tr')
    annual_labels = [
        'price_return', 'nav_return', 'benchmark_return', 'category_return', 'expense_ratio', 'turnover_ratio', 'category_rank'
    ]
    trailing_labels = [
        'price_return', 'nav_return', 'benchmark_return', 'category_return', 'category_rank'
    ]
    trailing_row_tags = [
        '1_day', '1_week', '1_month', '3_month', 'ytd', '1_year', '3_year', '5_year', '10_year', '15_year'
    ]

    if len(annual_rows) == 8: # it's a fund, drop the fourth row
        del annual_rows[3]
        del trailing_rows[3]

    for index_r, row in enumerate(annual_rows):
        label = annual_labels[index_r]
        row_dict = dict()
        data_list = []
        for i in row.find_all('td'):
            if len(i) == 0:
                data_list.append('')
            else:
                data_list.append(i.contents[0])
        for index_d, value in enumerate(data_list):
            if (index_d == 10):
                tag = 'ytd'
            else:
                tag = str(current_year - 10 + index_d)
            row_dict[tag] = data_list[index_d]
        data['annual'][label] = row_dict

    for index_r, row in enumerate(trailing_rows):
        label = trailing_labels[index_r]
        row_dict = dict()
        data_list = []
        for i in row.find_all('td'):
            if i.contents[0] == '—':
                data_list.append('')
            else:
                data_list.append(i.contents[0])
        for index_d, value in enumerate(data_list):
            row_dict[trailing_row_tags[index_d]] = data_list[index_d]
        data['trailing'][label] = row_dict
    
    return data


# res = get_data()
# index = [
#     'Price', 'Rank in Cat'
# ]

# columns = [
#     'YTD', '1-Year', '3-Year', '5-Year', '10-Year'
# ]

# data = [
#     [ ],
#     [ ]
# ]

# for i in res[1].find_all("tr")[1]:
#     try:
#         if i.string == '—':
#             data[0].append('-')
#         else:
#             data[0].append(float(i.string))
#     except ValueError as e:
#         pass

# for i in res[1].find_all("tr")[-1]:
#     try:
#         if i.string == '—':
#             data[1].append('-')
#         else:
#             data[1].append(float(i.string))
#     except ValueError as e:
#         pass

# data[0] = data[0][4:8]
# data[1] = data[1][4:8]

# dataframe = DataFrame(
#     index = index, columns = columns, data= data
# )
# print(dataframe)

print(extract_data(get_soup('spy')))

