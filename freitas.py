from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from tools import get_monta, update_errors
from selenium.webdriver.support.ui import WebDriverWait


def get_freitas_driver():
    driver_options = webdriver.ChromeOptions()
    driver_principal = "--blink-settings=imagesEnabled=false"
    driver_principal = webdriver.Chrome(driver_options)

    
    driver_principal.get("https://www.freitasleiloeiro.com.br/")
    driver_principal.maximize_window()
    botao = WebDriverWait(driver_principal, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-lg.btn-success"))
    )
    href = botao.get_attribute("href")
    driver_principal.get(href)
    while driver_principal.find_elements(By.CLASS_NAME, "small.text-center.text-secondary") == []:
        ActionChains(driver_principal).send_keys(Keys.PAGE_DOWN).perform()
    driver_principal.minimize_window()
    return driver_principal

from superbid import encontrar_marca_carro
def get_dict_card(card):
    dict_card = {
        "Data": "",
        "Comitente": "Freitas Leiloeiro",
        "Marca": "",
        "Modelo": "",
        "Valor": 0.0,
        "Cidade": "SANTO ANDRÉ",
        "Estado": "SP",
        "Monta": "", 
        "Link ": "",
        "Ano": ""
    }
    dict_card["Link"] = card.find_element(By.TAG_NAME, "a").get_attribute("href")
    dict_card["Data"] = card.find_element(
        By.CLASS_NAME, "cardLote-data").find_elements(
            By.TAG_NAME, "span")[0].text
    
    text_card = card.find_element(By.CLASS_NAME, "cardLote-descVeic").text
    marca_modelo = encontrar_marca_carro(text_card)
    try:
        dict_card["Modelo"] = marca_modelo[1].removeprefix("I/").removeprefix("/").split(",")[0].upper()
        dict_card["Marca"] = marca_modelo[0].upper()
    except:
        dict_card["Modelo"] = text_card
        dict_card["Marca"] = "Não Processado"
    dict_card["Ano"] = "20" + re.findall(r"\d{2}/\d{2}", text_card)[0].replace("/", "/20")
    dict_card["Monta"] = get_monta(card.find_element(By.CLASS_NAME, "cardLote-details").text)
    dict_card["Valor"] = float(card.find_element(By.CLASS_NAME, "cardLote-vlr").text.replace("R$ ", "").replace(".", "").replace(",", "."))



    return dict_card
def get_all_freitas_cards(driver_principal):

    cards = driver_principal.find_elements(By.CLASS_NAME, "cardlote")

    freitas_erros = 0
    for card in cards:
        try:
            yield get_dict_card(card)
        except Exception as e:
            update_errors("freitas", str(e))

    driver_principal.quit()



if __name__ == "__main__":
    driver_principal = get_freitas_driver()
    for card in get_all_freitas_cards(driver_principal):
        print(card)