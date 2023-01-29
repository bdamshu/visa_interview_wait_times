from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep


city_names = ['Hyderabad', 'New Delhi', 'Chennai', 'Kolkata', 'Mumbai']

driver = webdriver.Firefox()
driver.get('https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/wait-times.html')
dropdown_menu = driver.find_element_by_id('visawaittimeshomepag_visa_embassysearch_VisaWaitTimesHomePage_input')

idx = 0
b1b2_wait_times = {}
while idx < len(city_names):
    city_name = city_names[idx]
    dropdown_menu.send_keys(city_name)
    dropdown_menu.send_keys(Keys.ENTER) # works only when there 1 item in drop-down box
    sleep(2)    # wait for wait-times to populate
    # XML path for B1B2_interview_required wait-time field
    b1b2_wait_times[city_name] = driver.find_element_by_xpath('/html/body/div[3]/div[7]/div[2]/div[1]/div[2]/div[4]/div/div[3]/div[1]/table/tbody/tr[4]/td[2]/span').text
    
    edit_city = driver.find_element_by_class_name('edit_btn')
    edit_city.click()
    idx += 1
driver.close()

for city, wait_times in b1b2_wait_times.items():
    print(f'{city}: {wait_times}')
