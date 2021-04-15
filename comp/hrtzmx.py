from obj import *
from selenium import webdriver

def start_driver():
    """Function that starts webdriver and returns it"""
    driver = webdriver.Firefox()
    driver.implicitly_wait(40)

    base_url = "https://hertzmexico.com/"

    return driver, base_url

def get_data(driver, base_url):
    """Function that scrapes data and returns information"""

    driver.get(base_url)

    #start find city
    driver.find_element_by_class_name("zelected").click()
    cities = driver.find_element_by_class_name("zelect").find_elements_by_tag_name("ol")

    for city in cities[1:]:
        print(city.text)

    test_city = "CANCUN AEROPUERTO"
    #target_city = 
    zearch = driver.find_element_by_class_name("zearch")
    zearch.send_keys(test_city)

    driver.find_element_by_class_name("current").click()

    #end find city

    #find start date
    test_date1 = "15-04-2021".replace("-", "/")
    #target_fi = "DD-MM-YYYY".replace("-", "/")
    driver.find_element_by_id("datepicker").clear()
    driver.find_element_by_id("datepicker").send_keys(test_date1)
    #end start date
    
    #find end date
    test_date2 = "16-04-2021".replace("-", "/")
    driver.find_element_by_id("datepicker2").clear()
    driver.find_element_by_id("datepicker2").send_keys(test_date2)
    #end find end date
    
    #start find start time
    test_time1 = "16:00"

    time_list = driver.find_element_by_id("pickup_time").find_elements_by_tag_name("option")

    good_times = [time for time in time_list if "disabled" not in time.get_attribute("innerHTML").split()]
    for time in good_times:
        print(time.text)
        if(time.get_attribute("disabled") == ""):
            print("this is a bad time bro")

    good_times[5].get_attribute("disabled")
    print("bad")

    #end find start time


def conv_time(time):
    if(int(time[:2]) > 12):
        temp = str(int(time[:2] - 12))
        return temp + time[2:]
    else:
        return time

def quit_browse(driver):
    driver.quit()

driver, base_url = start_driver()

get_data(driver, base_url)

quit_browse(driver)
