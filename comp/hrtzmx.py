import pickle
from comp.obj import *
from comp.src.xlsw import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains


def start_driver():
    """Function that starts webdriver and returns it"""
    driver = webdriver.Firefox()
    driver.implicitly_wait(40)

    base_url = "https://hertzmexico.com/"

    return driver, base_url

def get_data(driver, base_url, fi, fe, hi, he):
    """Function that scrapes data and returns information"""

    driver.get(base_url)
    
    #check to see if continue pop up is on screen
    check_modal(driver)

    #start find city
    intro = driver.find_element_by_id("intro")
    zelect = intro.find_element_by_class_name("zelect")
    zelect.click()
    dropdown = zelect.find_element_by_class_name("dropdown") 
    cities = dropdown.find_elements_by_tag_name("li")
    cities.pop(0)
    for index, city in enumerate(cities):
        print(index + 1, " - ", city.text)
    
    city = cities[int(input("selecciona la ciudad para Hertzmx:\n")) - 1].text
    #target_city = 
    zearch = zelect.find_element_by_class_name("zearch")
    zearch.send_keys(city)
    zelect = driver.find_element_by_class_name("zelect")
    zelect.click()
    zelected = zelect.find_element_by_class_name("zelected")
    zelected.click()
    zelect.find_element_by_class_name("current").click()


    #end find city

    #find start date
    fi = fi.replace("-", "/")
    #target_fi = "DD-MM-YYYY".replace("-", "/")
    driver.find_element_by_id("datepicker").clear()
    driver.find_element_by_id("datepicker").send_keys(fi)
    #end start date
    
    #find end date
    fe = fe.replace("-", "/")
    driver.find_element_by_id("datepicker2").clear()
    driver.find_element_by_id("datepicker2").send_keys(fe)
    #end find end date
    
    #start find start time
    temphi = list(hi)
    if("3" in temphi):
        temphi[3] = "0"

    hi = ""
    hi = hi.join(temphi)
    hi = hi[:2] + ":00"

    time_element = driver.find_element(By.ID, "pickup_time")
    time_obj = Select(time_element)

    time_obj.select_by_value(hi)
    #end find start time

    #start find end time
    temphe = list(he)

    if("3" in temphe):
        temphe[3] = "0"

    he = ""
    he = he.join(temphe)
    time_element = driver.find_element_by_id("return_time")
    time_obj = Select(time_element)
    time_obj.select_by_value(he)
    #end find end time
    #submit
    #driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/3);")
    #wait = WebDriverWait(driver, 10)
    #download_button = wait.until(EC.visibility_of_element_located((By.ID, "enviaron")))
    #download_button.click()
    button = driver.find_element_by_id("enviaron").click()
    
    
    return city, driver

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

def extract_data(driver, v):
    vehicle_list = driver.find_elements_by_class_name("vehicle")
    
    vehicles = list()

    for vehicle in vehicle_list:
        desc = vehicle.find_element_by_class_name("vehicle-header")
        des1 = desc.find_element_by_class_name("vehicle-type").text
        des2 = desc.find_element_by_tag_name("strong").text
        description = str(des1) + " - "  +str(des2)
        price = vehicle.find_element_by_class_name("price").text

        details = vehicle.find_element_by_class_name("details")
        name = details.find_element_by_tag_name("h1").text.replace(" o similar", "")
        
        
        features = list()
        for feature in details.find_elements_by_tag_name("li"):
            features.append(feature.text)
        
        car = compCar(price, name, features, description)
        vehicles.append(car)
        
    if(v):
        for vehicle in vehicles:
            print(vehicle.name, "\n", vehicle.price, "\n", vehicle.description, "\n", vehicle.clave)
            print("#" * 50)
        
    return vehicles

def quit_browse(driver):
    driver.quit()

def load_data():
    return pickle.load(open("./comp/data.p", "rb"))

driver, base_url = start_driver()

data = load_data()

fi = data["fi"]
fe = data["fe"]
hi = data["hi"]
he = data["he"]
v = data["v"]

city, driver = get_data(driver, base_url, fi, fe, hi, he)
vehicles = extract_data(driver, v)

quit_browse(driver)

prices = [vehicle.price for vehicle in vehicles]
names = [vehicle.name for vehicle in vehicles]
descriptions = [vehicle.description for vehicle in vehicles]
claves = [vehicle.clave for vehicle in vehicles]

ws, wb = create_file("hertz", city, fi)
write_to_file(ws, prices, names, descriptions=descriptions, claves=claves)
wb_close(wb)
