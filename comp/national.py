import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def start_wd():
    driver = webdriver.Firefox()
    baseurl = "https://www.nationalcar.com.mx/"

    return driver, baseurl

def get_data(driver, baseurl):
    driver.get(baseurl)
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/3);")
    
    #start select city
    city = "cancun"
    search_box = driver.find_element(By.ID, "dropDownCiudadPickUp")
    
    
    while True:
        search_box.clear()
        search_box.send_keys(city)
        time.sleep(3)
        try:
            result_lst = driver.find_element(By.CSS_SELECTOR, ".list-group")
            results = result_lst.find_elements(By.TAG_NAME, "li")
            if(len(results) > 0):
                #for i in range(len(results)):
                    #if(i % 2 != 0):
                        #results.pop(i)
                break
        except:
            city = input("Ciudad no encontrada, ingresa ciudad para nationa car:\n")
    
    for i, loc in enumerate(results):
        str1 = repr(loc.text)
        temp = list(str1)
        temp.pop(0)
        city_name = "".join(temp[:temp.index("(")])
        print(i + 1, " - ", city_name)

    city_ind = int(input("Selecciona ubicacion:\n")) - 1
    results[city_ind].click()
    #end select city

    #select start info
    hi = "18:00"
    fi = "2021-7-1"

    hi = time_conv(hi)

    time.sleep(20)

    start_t = driver.find_element(By.ID, "txtFechaIni")

    driver.execute_script("arguments[0].setAttribute('value','{} {}')".format(fi, hi), start_t)
    
    #end select start

    #start select end
    he = "12:30"
    fe = "2021-8-11"

    he = time_conv(he)

    endf = driver.find_element(By.ID, "txtFechaFin")
    driver.execute_script("arguments[0].setAttribute('value','{} {}')".format(fe, he), endf)
    #end select end

    driver.find_element(By.CSS_SELECTOR, "#getQuoteBtn").click()

    time.sleep(2)
    input()

def time_conv(time):
    
    time_pattern = re.compile(r"(\d{1,2}):(\d{2})")
    time_match = time_pattern.match(time)
    timeh = int(time_match.group(1))
    timem = time_match.group(2)

    if(timeh > 12):
        timeh -= 12
        temp_time = list()
        if(len(str(timeh)) < 2):
            temp_time.append("0")
        temp_time.append(str(timeh))
        temp_time.append(":")
        temp_time.append(timem)
        temp_time.append(" PM")
        ntime = "".join(temp_time)
    elif(timeh <= 12):
        time += " AM"
        if(len(str(timeh)) < 2):
            ntime = "0" + time
        else:
            ntime = time
    
    return ntime


def exit_d(driver):
    driver.quit()

driver, baseurl = start_wd()

get_data(driver, baseurl)
exit_d(driver)
