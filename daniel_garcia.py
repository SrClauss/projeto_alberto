from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import requests
from tools import encontrar_marca_carro, get_monta, update_errors
from selenium.webdriver.support import expected_conditions as EC
import re
import time
tentativas = 1

def get_driver_daniel_garcia():
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("--blink-settings=imagesEnabled=false")

    driver = webdriver.Chrome()
    driver.get("https://tudoleilao.com.br/?categoria=1&pag=1&leilao=5")
    driver.maximize_window()
    driver.minimize_window()
    return driver

def get_max_page(driver):
    global tentativas
    try:  
        max_page = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "total-page"))).text.removeprefix("de ")
        while max_page == "":
            time.sleep(10)
            print("Aguardando o elemento total-page aparecer")
            max_page = WebDriverWait(driver=driver, timeout=10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "total-page"))).text.removeprefix("de ")
            driver.refresh()
        max_page = int(max_page)
    
        tentativas = 1
        return max_page
    except:
        time.sleep(20)
        tentativas += 1
        print(f"Erro ao obter o número máximo de páginas, fazendo {tentativas}ª tentativa")
        return get_max_page(driver)

def get_boxes(driver):
   boxes = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "box-leilao")))
   return boxes
   
   
   
def get_all_daniel_garcia_pages():
    driver_principal = get_driver_daniel_garcia()
    max_page = get_max_page(driver_principal)
    for page in range(1, max_page + 1):
        driver_principal.get(f"https://tudoleilao.com.br/?categoria=1&pag={page}&leilao=5")
        boxes = get_boxes(driver_principal)
        for box in boxes:
            try:
                yield get_dict_box(box)
            except Exception as e:
                print(str(e))
                update_errors("daniel_garcia", str(e))
          
                
                
    driver_principal.quit()

    
def get_dict_box(box):
   

    soup = BeautifulSoup(box.get_attribute("innerHTML"), "html.parser")
    data = soup.find("span", class_="date").text
    link_detalhe = WebDriverWait(box, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "a"))).get_attribute("href")
    
    html_detalhe = requests.get(link_detalhe).text
    soup = BeautifulSoup(html_detalhe, "html.parser")
    link_pagina = soup.find("div", class_="bt-participar").find("a").get("href")
    valor = float(soup.find("h3", class_="valor").text.removeprefix("R$").replace(".", "").replace(",", "."))
    
    soup = BeautifulSoup(requests.get(link_pagina).text, "html.parser")
    text = soup.find("b", string="Descrição: ").next_sibling.text
    marca_modelo = encontrar_marca_carro(text)
    marca = marca_modelo[0]
    modelo = marca_modelo[1].split(",")[0].removeprefix("|/").removeprefix("|").removeprefix("/")
    ano = re.findall(r"\d{4}/\d{4}", text)[0]
    comitente = "Daniel Garcia"
    monta = get_monta(text)
    return {
        "Data": data,
        "Comitente": comitente,
        "Marca": marca,
        "Modelo": modelo,
        "Valor": valor,
        "Cidade": "Não Informado",
        "Estado": "Não Informado", 
        "Link": link_pagina,
        "Monta": monta,
        "Ano": ano

    }

if __name__ == "__main__":
    for i in get_all_daniel_garcia_pages():
        print(i)