from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
from pathlib import Path
import pandas as pd


city_names = ['Hyderabad', 'New Delhi', 'Chennai', 'Kolkata', 'Mumbai']

driver = webdriver.Firefox()
driver.get('https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/wait-times.html')
dropdown_menu = driver.find_element_by_id('visawaittimeshomepag_visa_embassysearch_VisaWaitTimesHomePage_input')

idx = 0
b1b2_wait_times = {'Time': datetime.now()}
while idx < len(city_names):
    city = city_names[idx]
    dropdown_menu.send_keys(city)
    dropdown_menu.send_keys(Keys.ENTER) # works only when there 1 item in drop-down box
    sleep(2)    # wait for wait-times to populate
    # XML path for B1B2_interview_required wait-time field
    wait_time = driver.find_element_by_xpath('/html/body/div[3]/div[7]/div[2]/div[1]/div[2]/div[4]/div/div[3]/div[1]/table/tbody/tr[4]/td[2]/span').text
    b1b2_wait_times[city] = int(wait_time.split(' ')[0])

    edit_city = driver.find_element_by_class_name('edit_btn')
    edit_city.click()
    idx += 1
driver.close()

for city, wait_time in b1b2_wait_times.items():
    print(f'{city}: {wait_time} days')

b1b2_wait_times_df = pd.DataFrame(b1b2_wait_times, index=[0])
filename = Path('b1b2_interview_required_wait_times.csv')
if filename.is_file():
    data = pd.read_csv(filename)
    data = pd.concat([data, b1b2_wait_times_df], ignore_index=True)
    data.to_csv(filename, index=False)

    for city in city_names:
        if data.iloc[-1][city] < data.iloc[-2][city]:
            print(f'Wait time decreased at {city}. <<<<<<<<<<<<<<')
        elif data.iloc[-1][city] >= data.iloc[-2][city]:
            print(f'Wait time same or increased at {city}.')
else:
    b1b2_wait_times_df.to_csv(filename, index=False)