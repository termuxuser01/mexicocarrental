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
    cities = city_dropdown.find_elements(By.TAG_NAME, "li")
    
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
    
    days = target_month.find_elements(By.CLASS_NAME, "ui-state-default")

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
        times = driver.find_elements(By.CLASS_NAME, "ui-timepicker-pm")
        for t in times:
            if(t.text == stime):
                t.click()
    else:
        hi += " AM"
        if(len(str(hih)) < 2):
            hi = "0" + hi
        times = driver.find_elements(By.CLASS_NAME, "ui-timepicker-am")
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
    
    days = target_month.find_elements(By.CLASS_NAME, "ui-state-default")

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
        times = driver.find_elements(By.CLASS_NAME, "ui-timepicker-pm")
        for t in times:
            if(t.text == ftime):
                t.click()
    else:
        he += " AM"
        if(len(str(heh)) < 2):
            he = "0" + hi
        times = driver.find_elements(By.CLASS_NAME, "ui-timepicker-am")
        for t in times:
            if(t.text == he):
                t.click()

        
    #end select end time
    driver.find_element(By.CLASS_NAME, "bottonYellow").click()

    time.sleep(1)

    
    return driver, city

def data_extract(driver):
    vehicles = driver.find_elements(By.CLASS_NAME, "autoLista")
    
    ids = list()
    selectors = list()
    
    for vehicle in vehicles:
        divid = vehicle.get_attribute("id")
        pattern_no = re.compile(r"DivCarList_(\d+)")
        divno = pattern_no.match(divid).group(1)
        sel_tit = "#FrmCarList_{}".format(divno)
        css_selector = "{}"
        selectors.append(sel_tit)
        ids.append(divid)

    for sel_tit, idno in  zip(selectors, ids):
        vehicle = driver.find_element(By.ID, idno)

        name = vehicle.find_element(By.CLASS_NAME, "h2").text

        lists = vehicle.find_elements(By.TAG_NAME, "ul")

        descriptions = list()
        insurances = list()

        desc_i = lists[0].find_elements(By.TAG_NAME, "li")

        kilo_selector = "{} > div:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > li:nth-child(1) > span:nth-child(1) > span:nth-child(1)".format(sel_tit)
        kilo = driver.find_element(By.CSS_SELECTOR, kilo_selector).text
        descriptions.append("Kilometraje: " + kilo)

        descs = [desc.text for desc in desc_i]


        descriptions.append("Passajeros: " + descs[2])
        descriptions.append(descs[3])
        descriptions.append("Equipaje: " + descs[4])
        descriptions.append("Puertas: " + descs[6])
        descriptions.append(descs[7])

        for i in range(6):
            sel = "{} > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > ul:nth-child(1) > li:nth-child({})".format(sel_tit, i + 1)
            txt = driver.find_element(By.CSS_SELECTOR, sel).text
            insurances.append(txt)

        
        price_selector = "{} > div:nth-child(2) > div:nth-child(2) > a:nth-child(1) > div:nth-child(1) > p:nth-child(1)".format(sel_tit)
        price_box = driver.find_element(By.CSS_SELECTOR, price_selector)
        price_text = cleanhtml(price_box.get_attribute("innerHTML"))
        if(price_text != "No disponible"):
            vehicle.find_element(By.CLASS_NAME, "bottonVerde").click()
            time.sleep(1)
            price = extract_price(driver)
            driver.back()
            clear_page(driver)
        else:
            price = price_text

        print(name)
        print(price)
        print(descriptions)
        print(insurances)
        print("#" * 50)

        time.sleep(1)

def extract_price(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, "#waiverSinglePaquete_2 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1)").click()
    except:
        pass
    try:
        driver.find_element(By.CSS_SELECTOR, "a.paquete_2:nth-child(5)").click()
    except:
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "a.paquete_2:nth-child(5)").click()

    time.sleep(1)
    price = driver.find_element(By.ID, "extrasPrecio")

    return price.text

def clear_page(driver):
    #clean screen
    try:
        driver.find_element(By.CLASS_NAME, "btn-close-premium").click()
    except:
        pass
    try:
        driver.find_element(By.CSS_SELECTOR, ".modal-dialogFix > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)").click()
    except:
        pass

    time.sleep(1)
    elements = driver.find_elements(By.CLASS_NAME, "modal-backdrop")

    for element in elements:
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)
    
    try:
        driver.find_elements(By.ID, "closeprivilege")[1].click()
    except:
        pass

    try:
        driver.find_element(By.CSS_SELECTOR, ".modal-dialogFix > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)").click()
    except:
        pass
    
    return driver
    #end clean screen



def cleanhtml(html):
  clean_pattern = re.compile('<.*?>')
  cleantext = re.sub(clean_pattern, '', html)
  return cleantext

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
driver, city = get_data(driver, base_url)
driver = clear_page(driver)
data_extract(driver)
quit_browse(driver)
