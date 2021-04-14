import re
import time
import argparse
from selenium import webdriver


class Car():

    def __init__(self, city, syear, smonth, sday, fyear, fmonth, fday, shour, fhour, v):
        self.city = city
        self.syear = int(syear)
        self.smonth = int(smonth)
        self.sday = sday
        self.fyear = int(fyear)
        self.fmonth = int(fmonth)
        self.fday = fday
        self.shour = shour
        self.fhour = fhour
        self.v = v

        #handle webdriver
        self.driver = webdriver.Firefox()

        self.driver.implicitly_wait(40)
        self.base_url = "https://mexicocarrental.com.mx/#/searchcars"
        #end webdriver


    def click_scroll(self):
        driver = self.driver

        driver.get(self.base_url)
        
        #find city
        IATA_chosen = driver.find_element_by_id("IATA_chosen")
        target = IATA_chosen.find_element_by_tag_name("a")
        

        target.click()

        search_drop = IATA_chosen.find_element_by_class_name("chosen-drop")
        search_div = search_drop.find_element_by_class_name("chosen-search")
        search = search_div.find_element_by_tag_name("input")
        
        #debug
        #search.send_keys("guadalajara")

        search.send_keys(self.city)

        result_ul = search_drop.find_element_by_tag_name("ul")
        result = result_ul.find_element_by_tag_name("li")

        result.click()
        #end find city
        
        #select start date
        months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
                "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        start_dt = driver.find_element_by_id("fhInicio")
        start_dt.click()

        current_month_div = driver.find_element_by_class_name("datepicker-switch")
        
        month_pattern = re.compile(r"(\w+)\s(\d+)")
        current_month_name = month_pattern.match(current_month_div.text).groups()[0]
        current_year = int(month_pattern.match(current_month_div.text).groups()[1])

        current_month_ind = months.index(current_month_name)
        
        ##debug
        #smonth_name = "Junio"
        #sday = str(30)
        #syear = 2022

        #fmonth_name = "Julio"
        #fday = str(5)
        #fyear = 2022

        #smonth_ind = months.index(smonth_name)

        diff = (self.smonth - 1) - current_month_ind
        
        right_arrow = driver.find_element_by_class_name("newArrowRight")

        if(current_year == self.syear):
            pass
        else:
            diff += (self.syear - current_year) * 12

        if(diff > 0):
            for i in range(diff):
                right_arrow.click()
        elif(diff == 0):
            pass
        else:
            raise ValueError
        
        cal1 = driver.find_element_by_class_name("table-condensed")

        days_tag = cal1.find_element_by_tag_name("tbody")
        days = days_tag.find_elements_by_class_name("day")
        old_days = days_tag.find_elements_by_class_name("old")
        
        try:
            disabled_days = days.find_element_by_class_name("disabled")

            bad_days_elements = old_days + disabled_days
        except:
            bad_days_elements = old_days
        
        bad_days = list()

        for day in bad_days_elements:
            bad_days.append(day.text)

        if(self.sday in bad_days):
            bad_day = True
        else:
            bad_day = False
 
        try:
            for day in days:
                if(day.text == self.sday):
                    if(bad_day):
                        bad_day = False
                        continue
                    else:
                        day.click()
        except:
            cal2 = driver.find_element_by_class_name("table-condensed")
        #end select start date
        
        #select finish date
        current_month_div = driver.find_element_by_class_name("datepicker-switch")
        current_month_name = month_pattern.match(current_month_div.text).groups()[0]
        current_month_ind = months.index(current_month_name)
        
        current_year = int(month_pattern.match(current_month_div.text).groups()[1])

        
        diff = (self.fmonth - 1) - current_month_ind
        
        right_arrow = driver.find_element_by_class_name("newArrowRight")

        if(current_year == self.fyear):
            pass
        else:
            diff += (self.fyear - current_year) * 12

        if(diff > 0):
            for i in range(diff):
                right_arrow.click()
        elif(diff == 0):
            pass
        else:
            raise ValueError


        days_tag = cal2.find_element_by_tag_name("tbody")
        days = days_tag.find_elements_by_class_name("day")
        
        try:
            for day in days:
                if(day.text == self.fday):
                    if(bad_day):
                        bad_day = False
                        continue
                    else:
                        day.click()
        except:
            pass
        
        #end select finish date

        #select location
        location_menu = driver.find_element_by_id("ubicacion")
        location_menu.click()

        location_options = location_menu.find_elements_by_tag_name("option")

        for i, option in enumerate(location_options):
            print(i + 1, "-", option.text)

        location_choice = int(input("selecciona ubicacion:\n"))

        location_options[location_choice - 1].click()
        #end select location

        #select start time
        
        #debug
        #shour = "16:30"

        hora_inicio = driver.find_element_by_id("hora_pu")

        times = hora_inicio.find_elements_by_tag_name("option")

        for rtime in times:
            if(self.shour == rtime.get_attribute("value")):
                rtime.click()
        #end select start time

        #select finish time
        #debug
        #fhour = "18:00"

        hora_final = driver.find_element_by_id("hora_do")

        times = hora_final.find_elements_by_tag_name("option")

        for rtime in times:
            if(self.fhour == rtime.get_attribute("value")):
                rtime.click()
        #end select finish time
       
        #submit form

        
        subm = driver.find_element_by_name("tipo_cobro")

        subm.click()

        time.sleep(10)
        
        #end submit form

        ################################DEBUG###########################################
        #driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/3);")  #
        #time.sleep(2)                                                                 #
        #driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)*2/3);")#
        #time.sleep(2)                                                                 #
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")      #  
        ################################################################################

        #extract prices
        prices = self.find_price(driver)
        #extract names
        car_names = self.find_car_names(driver)
        #extract hours
        hours = self.find_hours(driver)
        #extract insurance
        insurances = self.find_insurance(driver)
        #extract description
        descriptions = self.find_description(driver)
        #extract clave
        claves = self.find_clave(driver)
        #extract group
        groups = self.find_group(driver)

        if(self.v):
            for price, name, hour, insurance, description, clave, group in zip(prices, car_names, hours, insurances, descriptions, claves, groups):
                print("#"*50)
                print("price:{}\nname:{}\nhour:{}\ninsurance:{}\ndescription:{}\nclave:{}\ngroup:{}".format(price, name, hour, insurance, description, clave, group))
        
        return prices, car_names, hours, insurances, descriptions, claves, groups
        
    def find_price(self, driver):
        prices = list()
        

        for price in driver.find_elements_by_class_name("precioDes"):
            si = price.text.index("$")
            fi = price.text.index('.') + 3
            prices.append(price.text[si:fi])

        return prices

    def find_car_names(self, driver):
        names = list()

        for name in driver.find_elements_by_class_name("tituloAutolista"):
            names.append(name.text)

        return names

    def find_hours(self, driver):
        hours = list()

        go = False
        
        for hour in driver.find_elements_by_class_name("datosOperadorDiv"):
            if(go):
                hours.append(hour.text)
                go = False
            else:
                go = True

        return hours

    def find_insurance(self, driver):
        insurances  = driver.find_elements_by_class_name("listatarifa")
        
        all_insurances = list()

        for insurance in insurances:
            all_insurances.append(self.cleanhtml(insurance.get_attribute("innerHTML")))

        return all_insurances

    def find_description(self, driver):
        descriptions = driver.find_elements_by_class_name("listCarFlota")

        all_descriptions = list()

        for description in descriptions:
            all_descriptions.append(description.text)

        return all_descriptions

    def find_clave(self, driver):
        claves = driver.find_elements_by_class_name("flotaTipo")

        all_claves = list()

        for clave in claves:
            all_claves.append(clave.text)

        return all_claves
        
    def find_group(self, driver):
        groups = driver.find_elements_by_class_name("tipoFlotaChar")

        all_groups = list()

        for group in groups:
            all_groups.append(group.text)

        return all_groups

    def cleanhtml(self, raw_html):
        cleaner = re.compile('<.*?>')
        cleantext = re.sub(cleaner, '', raw_html)
        semi = cleantext.split("\n")
        
        insurance = list()
        no = "Incluimos todos los seguros!"
        nl = True
        for word in semi:
            if(word == ''):
                continue
            elif(word == no):
                continue
            elif(nl):
                nl = False
                continue
            insurance.append(word.replace("\t", ""))

        insurance.pop(0)

        return [x[1:] for x in insurance if x != '']

    def done(self):
        self.driver.quit()

def date_extract(date):
    date_pattern = re.compile(r'(\d{4})-(\d{1,2})-(\d{1,2})')
    dates = date_pattern.match(date)
    year = dates.group(1)
    month = dates.group(2)
    day = dates.group(3)
    
    return year, month, day


if __name__ == "__main__":
    #handle arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--ciudad", help="Nombre de la ciudad")
    parser.add_argument("--fi", help="Fecha de inicio (YYYY-MM-DD) sin 0 a la izquirda")
    parser.add_argument("--fe", help="Fecha de entrega")
    parser.add_argument("--hi", help="Hora de inicio (formato militar)")
    parser.add_argument("--he", help="Hora de entrega (formato militar)")
    parser.add_argument("-v", "--verbose", help="Mostrar datos en consola",
                                action="store_true")

    args = parser.parse_args()
    #end handle arguments

    #handle dates
    syear, smonth, sday = date_extract(args.fi)
    fyear, fmonth, fday = date_extract(args.fe)
    #end handle dates
    car = Car(args.ciudad, syear, smonth, sday, fyear, fmonth, fday, args.hi, args.he, args.verbose)

    prices, names, hours, insurances, descriptions, claves, groups = car.click_scroll()

    car.done()
    
    from xlsw import *

    workbook = create_workbook(args.ciudad, args.fi)
    worksheet = create_worksheet(workbook)

    write_to_file(worksheet, prices, names, hours, insurances, descriptions, claves, groups)
    
    workbook.close()
