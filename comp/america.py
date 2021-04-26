import re
import time
from obj import *
from src.xlsw import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

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

    #start select start date
    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
                "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    fi = "2022-06-02"
    syear, smonth, sday = date_extract(fi)
    driver.find_element_by_id("PickUpDate").click()
    
    cal1 = driver.find_element_by_class_name("calentim-input")
    calendar = cal1.find_element_by_class_name("calentim-calendars")
    current_month = calendar.find_element_by_class_name("calentim-month-switch").text
    current_year = int(calendar.find_element_by_class_name("calentim-year-switch").text)
    print(current_month, current_year)
    
    current_month_ind = months.index(current_month)

    diff = (smonth - 1) - current_month_ind
    right_arrow = cal1.find_element_by_class_name("fa-arrow-right")

    if(current_year == syear):
        pass
    else:
        diff += (syear - current_year) * 12

    if(diff > 0):
        for i in range(diff):
            right_arrow = cal1.find_element_by_class_name("fa-arrow-right")
            right_arrow.click()
    elif(diff == 0):
        pass
    else:
        raise ValueError
    
    cal1 = driver.find_element_by_class_name("calentim-input")

    day_container = cal1.find_element_by_class_name("calentim-days-container")
    days_webelement = day_container.find_elements_by_class_name("calentim-day")

    for i, day in enumerate(days_webelement):
        if("calentim-disabled" in day.get_attribute("class").split()):
            print("removing {}".format(day.text))
            days_webelement.pop(i)
 
    for i, day in enumerate(days_webelement):
        if("calentim-disabled" in day.get_attribute("class").split()):
            print("removing {}".format(day.text))
            days_webelement.pop(i)
    
    for i, day in enumerate(days_webelement):
        if("calentim-disabled" in day.get_attribute("class").split()):
            print("removing {}".format(day.text))
            days_webelement.pop(i)
    
    action = ActionChains(driver)

    for day in days_webelement:
        try:
            if(int(day.text) == sday):
                day.click()
        except:
            pass

    #end select start date

    #start select end date
    fe = "2022-07-02"
    fyear, fmonth, fday = date_extract(fe)
    
    cal2 = driver.find_elements_by_class_name("calentim-input")[1]
    calendar = cal2.find_element_by_class_name("calentim-calendars")
    current_month = calendar.find_element_by_class_name("calentim-month-switch").text
    current_year = int(calendar.find_element_by_class_name("calentim-year-switch").text)
    print(current_month, current_year)

    current_month_ind = months.index(current_month)

    diff = (fmonth - 1) - current_month_ind
    right_arrow = cal2.find_element_by_class_name("fa-arrow-right")

    if(current_year == fyear):
        pass
    else:
        diff += (fyear - current_year) * 12

    if(diff > 0):
        for i in range(diff):
            right_arrow = cal2.find_element_by_class_name("fa-arrow-right")
            right_arrow.click()
    elif(diff == 0):
        pass
    else:
        raise ValueError

    cal2 = driver.find_elements_by_class_name("calentim-input")[1]
    day_container = cal2.find_element_by_class_name("calentim-days-container")
    days_webelement = day_container.find_elements_by_class_name("calentim-day")

    for i, day in enumerate(days_webelement):
        if("calentim-disabled" in day.get_attribute("class").split()):
            print("removing {}".format(day.text))
            days_webelement.pop(i)

    for i, day in enumerate(days_webelement):
        if("calentim-disabled" in day.get_attribute("class").split()):
            print("removing {}".format(day.text))
            days_webelement.pop(i)

    for i, day in enumerate(days_webelement):
        if("calentim-disabled" in day.get_attribute("class").split()):
            print("removing {}".format(day.text))
            days_webelement.pop(i)

    action = ActionChains(driver)

    for day in days_webelement:
        try:
            if(int(day.text) == fday):
                day.click()
        except:
            pass


    #end select end date

    #start select start time
    stime = "8:30"
    driver.find_element_by_id("PickUpHour").click()
    sclock = driver.find_element_by_class_name("calentim-timepicker-start")
    time.sleep(3)
    
    shour, sminutes = time_extract(stime)

    diffh = shour - 11
    
    if(diffh < 0):
        diffh *= -1
        for i in range(diffh):
            up_arrow = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[10]/div[2]/div[3]/div/div[2]/div[1]/i")))
            up_arrow.location_once_scrolled_into_view
            up_arrow.click()
    else:
        for i in range(diffh):
            up_arrow = sclock.find_element_by_class_name("calentim-timepicker-hours-up")
            up_arrow.click()

    #end select end time

def date_extract(date):
    date_pattern = re.compile(r'(\d{4})-(\d{1,2})-(\d{1,2})')
    dates = date_pattern.match(date)
    year = dates.group(1)
    month = dates.group(2)
    day = dates.group(3)

    return int(year), int(month), int(day)

def time_extract(time):
    pattern = re.compile(r"(\d{1,2}):(\d{2})")
    match = pattern.match(time)

    return int(match.group(1)), (match.group(2))


driver, base_url = start_driver()
city = "aaaa"
get_data(driver, base_url, city)
