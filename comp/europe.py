import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def start_driver():
    driver = webdriver.Firefox()
    base_url = "https://www.europcar.com.mx/"

    return driver, base_url

def get_data(driver, base_url):
    driver.get(base_url)

    #start select city
    city = "cancun"
    search_bar = driver.find_element(By.ID, "idcheckoutLocationName")
    search_bar.send_keys(city)
    time.sleep(2)
    result = driver.find_element(By.CLASS_NAME, "custom-menu-search").text
    
    fail_str = "Sin resultados, por favor revisa la ortografía o realiza una nueva búsqueda"
    
    while result == fail_str:
        city = input("cuidad no encontrada, ingresa una ciudad:\n")
        search_bar.clear()
        search_bar.send_keys(city)
        time.sleep(2)
        result = driver.find_element(By.CLASS_NAME, "custom-menu-search").text
    
    city_dropdown = driver.find_element(By.CLASS_NAME, "custom-menu-search")
    cities = city_dropdown.find_elements_by_tag_name("li")
    
    for i, city in enumerate(cities):
        if(city.text.startswith("OFICINAS")):
            del cities[i]

    for i, city in enumerate(cities):
        print("{} - {}".format(i+1, city.text))

    select_city = int(input("Seleciona sucursal para europecar:\n")) - 1

    cities[select_city].click()

    #end select city

    #start select start date

    fi = "2021-06-10"
    smonth = 5
    syear = 2022
    sday = 11
    driver.find_element(By.ID, "idcheckoutDay").click()

    cal1 = driver.find_element(By.ID, "ui-datepicker-div")


    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
            "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    
    while True:
        next_cal = cal1.find_element(By.CLASS_NAME, "ui-datepicker-group-last")
        current_cal = cal1.find_element(By.CLASS_NAME, "ui-datepicker-group-first")
        
        current_month = current_cal.find_element(By.CLASS_NAME, "ui-datepicker-month").text
        current_year = int(current_cal.find_element(By.CLASS_NAME, "ui-datepicker-year").text)

        next_month = next_cal.find_element(By.CLASS_NAME, "ui-datepicker-month").text
        next_year = int(next_cal.find_element(By.CLASS_NAME, "ui-datepicker-year").text)

        try:
            right_arrow = cal1.find_element(By.CLASS_NAME, "ui-datepicker-next")
        except:
            target_month = next_cal.find_element(By.CLASS_NAME, "ui-datepicker-calendar")
            break
        
        current_month_ind = months.index(current_month) + 1
        next_month_ind = months.index(next_month) + 1
        
        print(current_month, current_year, type(current_year), current_month_ind, type(current_month_ind))
        print(next_month, next_year, type(next_year), next_month_ind, type(next_month_ind))

        if(smonth == next_month_ind):
            if(syear > next_year):
                diff = (syear - next_year) * 12
                for i in range(diff):
                    right_arrow = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/a")
                    right_arrow.click()

            next_cal = driver.find_element(By.CLASS_NAME, "ui-datepicker-group-last")        
            target_month = next_cal.find_element(By.CLASS_NAME, "ui-datepicker-calendar")
            break
        elif(smonth == current_month_ind):
            if(syear > current_year):
                diff = (syear - current_year) * 12
                for i in range(diff):
                    right_arrow = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/a")
                    right_arrow.click()
            
            current_cal = driver.find_element(By.CLASS_NAME, "ui-datepicker-group-first")
            target_month = current_cal.find_element(By.CLASS_NAME, "ui-datepicker-calendar")
            break
        else:
            right_arrow.click()
    
    days = target_month.find_elements_by_class_name("ui-state-default")

    for day in days:
        try:
            if(sday == int(day.text)):
                day.click()
        except:
            pass


    #end select start date
    
    #start select start time
    driver.find_element(By.ID, "checkoutHourMinDisplay0").click()
    hi = "10:15"

    time_pattern = re.compile(r"(\d{1,2}):(\d{2})")
    time_match = time_pattern.match(hi)
    hih = int(time_match.group(1))
    him = time_match.group(2)

    if(hih > 12):
        hih -= 12
        temp_time = list()
        if(len(str(hih)) < 2):
            temp_time.append("0")
        temp_time.append(str(hih))
        temp_time.append(":")
        temp_time.append(him)
        temp_time.append(" PM")
        stime = "".join(temp_time)
        times = driver.find_elements_by_class_name("ui-timepicker-pm")
        for t in times:
            if(t.text == stime):
                t.click()
    else:
        hi += " AM"
        if(len(str(hih)) < 2):
            hi = "0" + hi
        times = driver.find_elements_by_class_name("ui-timepicker-am")
        for t in times:
            if(t.text == hi):
                t.click()

        
    #end select start time

    #start select end date

    fe = "2022-06-12"
    fyear, fmonth, fday = date_extract(fe)

    driver.find_element(By.ID, "idcheckinDay").click()

    cal1 = driver.find_element(By.ID, "ui-datepicker-div")


    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
            "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    
    while True:
        next_cal = cal1.find_element(By.CLASS_NAME, "ui-datepicker-group-last")
        current_cal = cal1.find_element(By.CLASS_NAME, "ui-datepicker-group-first")
        
        current_month = current_cal.find_element(By.CLASS_NAME, "ui-datepicker-month").text
        current_year = int(current_cal.find_element(By.CLASS_NAME, "ui-datepicker-year").text)

        next_month = next_cal.find_element(By.CLASS_NAME, "ui-datepicker-month").text
        next_year = int(next_cal.find_element(By.CLASS_NAME, "ui-datepicker-year").text)

        try:
            right_arrow = cal1.find_element(By.CLASS_NAME, "ui-datepicker-next")
        except:
            target_month = next_cal.find_element(By.CLASS_NAME, "ui-datepicker-calendar")
            break
        
        current_month_ind = months.index(current_month) + 1
        next_month_ind = months.index(next_month) + 1
        
        print(current_month, current_year, type(current_year), current_month_ind, type(current_month_ind))
        print(next_month, next_year, type(next_year), next_month_ind, type(next_month_ind))

        if(fmonth == next_month_ind):
            if(fyear > next_year):
                diff = (fyear - next_year) * 12
                for i in range(diff):
                    right_arrow = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/a")
                    right_arrow.click()

            next_cal = driver.find_element(By.CLASS_NAME, "ui-datepicker-group-last")        
            target_month = next_cal.find_element(By.CLASS_NAME, "ui-datepicker-calendar")
            break
        
        elif(fmonth == current_month_ind):
            if(fyear > current_year):
                diff = (fyear - current_year) * 12
                for i in range(diff):
                    right_arrow = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/a")
                    right_arrow.click()
            
            current_cal = driver.find_element(By.CLASS_NAME, "ui-datepicker-group-first")
            target_month = current_cal.find_element(By.CLASS_NAME, "ui-datepicker-calendar")
            break
        else:
            right_arrow.click()
    
    days = target_month.find_elements_by_class_name("ui-state-default")

    for day in days:
        try:
            if(fday == int(day.text)):
                day.click()
        except:
            pass


    #end select end date
    
    #start select end time
    driver.find_element(By.ID, "checkinHourMinDisplay0").click()
    he = "17:45"

    time_match2 = time_pattern.match(he)
    heh = int(time_match2.group(1))
    hem = time_match2.group(2)

    if(heh > 12):
        heh -= 12
        temp_time = list()
        if(len(str(heh)) < 2):
            temp_time.append("0")
        temp_time.append(str(heh))
        temp_time.append(":")
        temp_time.append(hem)
        temp_time.append(" PM")
        ftime = "".join(temp_time)
        times = driver.find_elements_by_class_name("ui-timepicker-pm")
        for t in times:
            if(t.text == ftime):
                t.click()
    else:
        he += " AM"
        if(len(str(heh)) < 2):
            he = "0" + hi
        times = driver.find_elements_by_class_name("ui-timepicker-am")
        for t in times:
            if(t.text == he):
                t.click()

        
    #end select end time
    driver.find_element(By.CLASS_NAME, "bottonYellow").click()


def date_extract(date):
    pattern = re.compile(r"(\d{4})-(\d{1,2})-(\d{1,2})")
    match = pattern.match(date)
    
    year = int(match.group(1))
    month = int(match.group(2))
    day = int(match.group(3))
    
    return year, month, day


def quit_browse(driver):
    driver.quit()



driver, base_url = start_driver()
get_data(driver, base_url)

quit_browse(driver)
