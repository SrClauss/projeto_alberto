from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import requests as rq
from bs4 import BeautifulSoup
from tools import get_monta, encontrar_marca_carro, update_errors
from tools import get_monta
from datetime import datetime, timedelta



def get_max_superbid_page():


    driver_pagina = webdriver.Chrome()
    driver_pagina.get("https://www.superbid.net/categorias/carros-motos/carros?searchType=opened&filter=auction.modalityDesc:leilao&pageNumber=1&pageSize=60&orderBy=price:desc")
    driver_pagina.maximize_window()
    gcap = WebDriverWait(driver_pagina, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "gcap-close")))
    gcap.click()
    accept_cookie_button = WebDriverWait(driver_pagina, 10).until(
    EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    accept_cookie_button.click()
    last = WebDriverWait(driver_pagina, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@data-testid='SkipNextIcon']")))
    last.click()
    all = int(driver_pagina.current_url.split("pageNumber=")[1].split("&")[0])
    driver_pagina.quit()
    return all
   
def get_valids_soups(driver_pagina):
    boxes = WebDriverWait(driver_pagina, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[starts-with(@id, 'offer-')]")))


    soups = [BeautifulSoup(box.get_attribute("innerHTML"), "html.parser") for box in boxes]
    soups = [soup for soup in soups if soup.find("img", {"src": "./images/logo_location.svg"}) is not None]
    return soups
def get_date(soup):
    current_date = datetime.now()

    encerramento = soup.find_all("span", class_="MuiChip-labelMedium")[0]
    string_date = re.findall(r"\d{2}/\d{2}", str(encerramento))[0] if re.findall(r"\d{2}/\d{2}", str(encerramento)) else None
    if string_date:
        date = datetime.strptime(string_date + "/" + str(current_date.year), "%d/%m/%Y")
        if date < current_date:
            date = date.replace(year=current_date.year + 1)
    
        return date.strftime("%d/%m/%Y")
    if encerramento.text[-1] == 'h':
        horas = int(re.findall(r"\d+", str(encerramento))[0])
        return (current_date + timedelta(hours=horas)).strftime("%d/%m/%Y")
    if str(encerramento.text).__contains__("dias"):
        dias = int(re.findall(r"\d+", str(encerramento))[0])
        return (current_date + timedelta(days=dias)).strftime("%d/%m/%Y")
    
    return "Não Informado"
       

def get_local(soup):
    cidade_estado = soup.find_all("p", class_="MuiTypography-body1")[1].text.split(" • ")[0]
    return cidade_estado.split(" - ")[0], cidade_estado.split(" - ")[1] if cidade_estado.__len__() > 0 else "Não Informado"

def get_valor(soup):
    valor = soup.find_all('p', class_='MuiTypography-body1')[4].text
    return float(valor.replace('R$', '').replace('.', '').replace(',', '.')) if valor.__len__() > 0 else "Não Informado"

def get_text(soup):
    return soup.find('p', class_='MuiTypography-body1').text


def get_dict_card(soup):

    text = get_text(soup)
    monta = get_monta(text)
    marca, modelo = encontrar_marca_carro(text)
    modelo = modelo.split(",")[0] if "," in modelo else modelo
    ano = re.findall(r"\d{4}/\d{4}", text)[0] if re.findall(r"\d{4}/\d{4}", text) else None
    valor = get_valor(soup)
    date = get_date(soup)
    cidade, estado = get_local(soup)
    comitente = "SuperBID"

    return {
        "Data": date,
        "Comitente": comitente.upper(),
        "Marca": marca.upper(),
        "Modelo": modelo.removeprefix("/").removeprefix(" /").strip().upper(),
        "Valor": valor,
        "Cidade": cidade.upper(),
        "Estado": estado.upper(),
        "Link": "https://www.superbid.net" + soup.find('a').get('href'),
        "Monta": monta.upper(),
        "Ano": ano,     
    }
def get_all_superbid_pages(all):
        drivers = []
        driver_option = webdriver.ChromeOptions()
        #driver_option.add_argument("--headless")
        driver_option.add_argument("--no-sandbox")
        driver_option.add_argument("--disable-dev-shm-usage")
        driver_option.add_argument("--disable-gpu")
        driver_option.add_argument("--blink-settings=imagesEnabled=false")
        for i in range(1, all+1):
            driver = webdriver.Chrome(driver_option)
            driver.get(f"https://www.superbid.net/categorias/carros-motos/carros?searchType=opened&filter=auction.modalityDesc:leilao&pageNumber={1}&pageSize=60&orderBy=price:desc")
            drivers.append(driver)
        
        for driver in drivers:           
            soups = get_valids_soups(driver)
            for soup in soups:
                try:
                    yield get_dict_card(soup)
                except Exception as e:
                    update_errors("superbid", str(e))
            driver.quit()
        
if __name__ == "__main__":
    for i in get_all_superbid_pages():
        print(i)


