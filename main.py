from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from pandas import DataFrame
import math
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

    tables = response.find_all('tbody')[0:2]
    return tables

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

print(extract_data(get_soup('SPY')))

