from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from tools import update_errors
import math
import re
from bs4 import BeautifulSoup


tentativas = 1

def get_vip_driver():
    driver_option = webdriver.ChromeOptions()

    driver_option.add_argument("--blink-settings=imagesEnabled=false")

    driver_principal = webdriver.Chrome(driver_option)
    driver_principal.get("https://www.vipleiloes.com.br/Veiculos/ListarVeiculos?TipoVeiculos=1")
    driver_principal.maximize_window()
    driver_principal.minimize_window()
    return driver_principal

def get_number_pages(driver_principal):
    number_elements = int(WebDriverWait(driver_principal, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "slv-restit"))).text.split(" ")[0])
    return math.ceil(number_elements/12)
def get_page_cards(driver_principal):
    cards = WebDriverWait(driver_principal, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "itm-card")))

    for card in cards:
        if card.text !="":
            try:
                yield get_dict_card(card)
            except:
                vip_leilao_errors += 1

                


def get_dict_card(card):
    html = card.find_element(By.CLASS_NAME, "itm-action").find_element(By.TAG_NAME, "a").get_attribute("data-bs-content")
    
    soup = BeautifulSoup(html, "html.parser")
    local = soup.find("p", class_="itm-tagloc").text
    cidade = local.split(" - ")[0]
    estado = local.split(" - ")[1]
    ano = soup.find("p", class_="itm-tagyar").text.removeprefix("Ano: ")
    monta = soup.find("p", class_="itm-tagrec").text
    descricao = card.find_element(By.CLASS_NAME, "itm-name").text.split("\n")
    try :
        marca = descricao[0]
        modelo = re.sub(r"\d{4}/\d{4}", "", descricao[1]).strip()
    except:
        marca = ""
        modelo = ""

    valor = float(card.find_element(By.CLASS_NAME, "itm-value").text.removeprefix("R$ ").replace(".", "").replace(",", "."))
    link = card.find_element(By.CLASS_NAME, "itm-cdlink").get_attribute("href")
    data = card.find_elements(By.CLASS_NAME, "itm-start")[1].text
    data = re.findall(r'\d{2}/\d{2}/\d{4}', data)[0]
    return {
        "Data": data,
        "Comitente": "VIP LEILÕES",
        "Marca": marca.upper(),
        "Modelo": modelo.upper(),
        "Valor": valor,
        "Cidade": cidade.upper(),
        "Estado": estado.upper(),
        "Monta": monta.upper(),
        "Link": link,
        "Ano": ano,
        
    }
def try_next_page(driver_principal, next):
    driver_principal.get(f'https://www.vipleiloes.com.br/Veiculos/ListarVeiculos?TipoVeiculos=1&Pagina={next}')
    try:
        
        driver_principal.implicitly_wait(2)
    except:
        raise Exception("Não foi possível acessar a página")

def process_page(driver_princial, i):
    
    driver_princial.get(f"https://www.vipleiloes.com.br/Veiculos/ListarVeiculos?TipoVeiculos=1&Pagina={i}")
    try:
        WebDriverWait(driver_princial, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "itm-card")))
    except Exception as e:
        update_errors("vip_leiloes", str(e))
        process_page
    

                        
def get_all_vipleiloes_pages():
    driver_principal = get_vip_driver()
    max_pages = get_number_pages(driver_principal)
    for i in range(1, max_pages + 1):
        if i == 1:
            pass
        else:
            process_page(driver_principal, i)   
        for card in get_page_cards(driver_principal):
            try:
                yield card
            except Exception as e:
                update_errors("vip_leiloes", str(e))
    driver_principal.quit()
    
