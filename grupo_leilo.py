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

import concurrent.futures
tentativas = 1
max_page = 0

def get_leilo_drivers():
    global tentativas
    global max_page
    driver = webdriver.Chrome()
    driver.get("https://leilo.com.br/leilao/carros?ordenacao=dataFim%7Casc")
    x = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "text-white.cursor-pointer.q-icon.notranslate.material-icons-round")))
    x.click()
    soap = BeautifulSoup(driver.page_source, 'html.parser'                    )
   
    max_page = int(soap.find("i", string="keyboard_double_arrow_right").parent.parent.parent["aria-label"])
    driver.quit

    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("--blink-settings=imagesEnabled=false")
    driver_principal = webdriver.Chrome(driver_options)
    driver_principal.get("https://leilo.com.br/leilao/carros?ordenacao=dataFim%7Casc")
    driver_principal.maximize_window()
    return driver_principal

   
def recuse_cookies(driver):
    global tentativas
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cc-nb-reject"))).click()
        tentativas = 1
    except:
        tentativas+= 1
        driver.refresh()
        print("erro ao recusar cookies, fazendo uma {}ª tentativa".format(tentativas))
        time.sleep(0.5)
        recuse_cookies()
        

    
def get_dict_card(card):
    soap = BeautifulSoup(card.get_attribute("outerHTML"), "html.parser")
    data = re.findall(r"\d{2}/\d{2}/\d{4}", soap.find("span", string="Leilão:").next_sibling.text)[0]
    comitente = "Grupo Leilo"
    marca_modelo = encontrar_marca_carro(soap.select_one(".q-ma-none.text-weight-600.text-secondary").text)
    marca = marca_modelo[0]
    modelo = marca_modelo[1].removeprefix("I/ ").removeprefix("/").split(",")[0].upper()
    ano = soap.find("p", class_="text-ano").text

    valor = float(re.sub(r'[\n\xa0R$]+','', 
            soap.find("li", attrs={"class": "valor-atual"}).text)
            .strip().replace(".", "").replace(",", "."))

    link = "https://leilo.com.br" + soap.find("a").get("href")
    result = rq.get(link).text


        
    soap = BeautifulSoup(result, "html.parser")
    monta = get_monta(soap.find("div", attrs={"id": "gtm-detalhe-descricao"}).text)
    cidade =  soap.find("span", string="Cidade ").next_sibling.next_sibling.split(" - ")[0]
    estado =  soap.find("span", string="Cidade ").next_sibling.next_sibling.text.split(" - ")[1]


    
    return {
        "Data": data,
        "Comitente": comitente,
        "Marca": marca,
        "Modelo": modelo,
        "Valor": valor,
        "Cidade":cidade,
        "Estado":estado,
        "Link": link,
        "Monta": monta,
        "Ano": ano,
        
    }



def process_card(card):
    #return get_dict_card(card)
    
    try:
        return get_dict_card(card)
    except Exception as e:
        update_errors("grupo_leilo", str(e))
    

def get_all_cards_page(driver_principal):
    try:
        cards = WebDriverWait(driver_principal, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-leilao-vertical")))
    except:
        driver_principal.refresh()
        return get_all_cards_page(driver_principal)
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_results = [executor.submit(process_card, card) for card in cards]

        for future in concurrent.futures.as_completed(future_results):
            #result = future.result()
            #results.append(result)
            #yield result
    
            try:
                result = future.result()
                results.append(result)
                yield result
            except Exception as e:
                update_errors("grupo_leilo", str(e))
                print(f"Error processing card: {str(e)}")
    
    return results
   
def get_all_leilo_pages():
    global max_page
    driver_principal = get_leilo_drivers()
    recuse_cookies(driver_principal)    
    for i in range(1, max_page+1):
        WebDriverWait(driver_principal, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-leilao-vertical")))
        driver_principal.get(f"https://www.grupoleilo.com.br/leilao/carros?pagina={i}&ordenacao=dataFim%7Casc")
        for card in get_all_cards_page(driver_principal):
           yield card

    driver_principal.quit()

    



if __name__ == "__main__":
    for i in get_all_leilo_pages():
        print(i)