from obj import *
from selenium import webdriver
#possible imports
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def start_driver():
    """Function that starts webdriver and returns it"""
    driver = webdriver.Firefox()
    driver.implicitly_wait(40)

    base_url = "https://hertzmexico.com/"

    return driver, base_url

def get_data(driver, base_url):
    """Function that scrapes data and returns information"""

    driver.get(base_url)
    
    #check to see if continue pop up is on screen
    check_modal(driver)

    #start find city
    intro = driver.find_element_by_id("intro")
    zelect = intro.find_element_by_class_name("zelect")
    zelect.click()
    input("Here I am")    
    cities = zelect.find_element_by_class_name("dropdown").find_elements_by_tag_name("ol")
    input("is the dropdown still there?")
    for city in cities[1:]:
        print(city.text)
    
    input("im about to type")
    test_city = "CANCUN AEROPUERTO"
    #target_city = 
    zearch = zelect.find_element_by_class_name("zearch")
    zearch.send_keys(test_city)
    zelect = driver.find_element_by_class_name("zelect")
    zelect.click()
    zelected = zelect.find_element_by_class_name("zelected")
    zelected.click()
    input("I clicked again")    
    zelect.find_element_by_class_name("current").click()

    input("were the cities done?")

    #end find city

    #find start date
    test_date1 = "20-04-2021".replace("-", "/")
    #target_fi = "DD-MM-YYYY".replace("-", "/")
    driver.find_element_by_id("datepicker").clear()
    driver.find_element_by_id("datepicker").send_keys(test_date1)
    #end start date
    
    #find end date
    test_date2 = "21-04-2021".replace("-", "/")
    driver.find_element_by_id("datepicker2").clear()
    driver.find_element_by_id("datepicker2").send_keys(test_date2)
    #end find end date
    
    #start find start time
    test_time1 = "16:00"
    print(test_time1)
    time_element = driver.find_element_by_id("pickup_time")
    time_obj = Select(time_element)

    time_obj.select_by_value(test_time1)
    #end find start time

    #start find end time
    test_time2 = "08:00"
    time_element = driver.find_element_by_id("return_time")
    time_obj = Select(time_element)
    time_obj.select_by_value(test_time2)
    #end find end time
    input()
    #submit
    #driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/3);")
    #wait = WebDriverWait(driver, 10)
    #download_button = wait.until(EC.visibility_of_element_located((By.ID, "enviaron")))
    #download_button.click()
    input()
    button = driver.find_element_by_id("enviaron").click()
    input()


def check_modal(driver):
    try:
        driver.find_element_by_id("new_reservation_buttton").click()
    except:
        return

def conv_time(time):
    if(int(time[:2]) > 12):
        temp = str(int(time[:2] - 12))
        if(int(temp) < 10):
            temp = "0" + temp
        return temp + time[2:] + " PM"
    else:
        return time + " AM"

def quit_browse(driver):
    driver.quit()

driver, base_url = start_driver()

get_data(driver, base_url)

quit_browse(driver)
