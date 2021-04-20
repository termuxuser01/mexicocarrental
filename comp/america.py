import time
from obj import *
from src.xlsw import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains


def start_driver():
    driver = webdriver.Firefox()
    driver.implicitly_wait(40)

    base_url = "https://americacarrental.com.mx/"

    return driver, base_url

def get_data(driver, base_url, city, fi=None, fe=None, hi=None, he=None):
    
    driver.get(base_url)
    
    #select city
    csearch = driver.find_element_by_id("Pickup")

    csearch.send_keys(city)
    city_dropdown = driver.find_element_by_id("ui-id-1")
    cities = city_dropdown.find_elements_by_class_name("ui-menu-item-wrapper")
 

    while True:
        
        city_dropdown = driver.find_element_by_id("ui-id-1")
        cities = city_dropdown.find_elements_by_class_name("ui-menu-item-wrapper")

        if(cities[0].get_attribute("innerHTML") != "No contamos con autos en esta sucursal"):
            print("I'm going to break")
            break
        else:
            print("cuidad no encontrada")
            city = input("ingresa un nombre de ciudad para buscar:\n")
            csearch.clear()
            csearch.send_keys(city)
            time.sleep(3)
            city_dropdown = driver.find_element_by_id("ui-id-1")
            cities = city_dropdown.find_elements_by_class_name("ui-menu-item-wrapper")
            print("this is me", cities[0].get_attribute("innerHTML"))


    for i, city in enumerate(cities):
        print(i + 1, "-", city.get_attribute("innerHTML"))

    target_city = cities[int(input("Seleciona la sucursal:\n")) - 1]

    time.sleep(5)
    
    action = ActionChains(driver)
    action.double_click(target_city).perform()
    #end select city

    #start select start time
    fi = "2021-6-22"
    syear, smonth, sday = date_extract(fi)
    driver.find_element_by_id("PickUpDate").click()

    cal1 = driver.find_element_by_class_name("calentim-input")
    calendar = cal1.find_element_by_class_name("calentim-calendars")
    current_month = calendar.find_element_by_class_name("calentim-month-switch").text
    current_year = calendar.find_element_by_class_name("calentim-year-switch").text
    print(current_month, current_year)

    if(current_year == syear):
        pass

    #end select start time

def date_extract(date):
    date_pattern = re.compile(r'(\d{4})-(\d{1,2})-(\d{1,2})')
    dates = date_pattern.match(date)
    year = dates.group(1)
    month = dates.group(2)
    day = dates.group(3)

    return year, month, day




driver, base_url = start_driver()
city = "aaaa"
get_data(driver, base_url, city)
