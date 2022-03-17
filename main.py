from importlib.resources import path
from posixpath import split
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pathlib import Path
from PIL import Image
import os


def url(): # Open Browser at his url
    return "https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces"

def exe_chrome_driver(): # Chrome driver location
    return Path("Selenium\chromedriver.exe")

def search_bar_location():
    return "vistaConsultaEstadoRUT:formConsultaEstadoRUT:numNit"

def error_button_location(): 
    return "//img[@src='imagenes/es/botones/botcerrarrerror.gif']"

def key_response(): # HTML object that tells if CNPJ status
    return "vistaConsultaEstadoRUT:formConsultaEstadoRUT:estado"

def lista_cnpj_txt(): # txt name with CNPJ list
    return "lista_cnpj.txt"

def read_file(): # Read txt
    read_file = open(lista_cnpj_txt(), "r")
    read_file = read_file.read().split()
    return read_file

def lista_cnpj(): # Convert txt containing CNPJ list in python list
    read_file_var = read_file()
    
    key_list = []

    for line in read_file_var:
        key_list.append(line)

    return key_list

def open_browser():
    s = Service(exe_chrome_driver())
    driver = webdriver.Chrome(service = s)
    driver.get(url())
    return driver

def create_txt(): # Creates txt file with CNPJ and it's status
    txt = open("ResultadoConsulta.txt", "a")
    return txt 

def main():
    key_list = lista_cnpj()

    driver = open_browser()

    txt = create_txt()

    index = 0
    for cnpj in key_list: # Loop to search status for each CNPJ in txt file
        try:
            driver.find_element(By.ID, search_bar_location()).send_keys(cnpj + Keys.ENTER) # Input CNPJ into web search bar
        
            response = driver.find_element(By.ID, key_response()).text # Get CNPJ status
            
            txt.write(f"{cnpj}: {response}\n") # Write CNPJ status into ResultadoConsulta.txt file

            if response == "REGISTRO ACTIVO":
                driver.save_screenshot(f'{cnpj}.png')
                image_1 = Image.open(f'{cnpj}.png')
                im_1 = image_1.convert('RGB')
                im_1.save(f'Screenshots\{cnpj}.pdf')
                os.remove(f'{cnpj}.png')
            else:
                continue

            driver.find_element(By.ID, search_bar_location()).clear() # Clear web search bar

            index += 1
        except:
            driver.find_element(By.XPATH, error_button_location()).click()

            txt.write(f"{cnpj}: ERROR --> check CNPJ format\n")

            driver.find_element(By.ID, search_bar_location()).clear()

            index += 1

if __name__ == "__main__":
    main()
    

