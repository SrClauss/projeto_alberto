import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from tools import encontrar_marca_carro, update_errors
from bs4 import BeautifulSoup
import requests as rq
import concurrent.futures
tentativas = 1

def get_max_box(driver):
    global tentativas
    try:
        max_box = int(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jss129"))).find_element(By.TAG_NAME, "div").text.split(" ")[0])
        tentativas = 1
        return max_box
    
    except:
        tentativas += 1
        print(f"Erro ao obter o número máximo de box, fazendo {tentativas}ª tentativa")
        return get_max_box(driver)

def get_loop_driver():

    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("--blink-settings=imagesEnabled=false")
    driver_options.add_argument("--disable-gpu")
    driver_options.add_argument("--no-sandbox")
    driver_options.add_argument("--disable-dev-shm-usage")

    driver_principal_options = webdriver.ChromeOptions()
    driver_principal_options.add_argument("--blink-settings=imagesEnabled=false")
    driver_principal = webdriver.Chrome()
    driver_principal.get(
        "https://loopleiloes.com.br/estoque?tipo=Leve&evento_data=2077-01-01&")
    driver_principal.maximize_window()
    max_box = get_max_box(driver_principal)
    WebDriverWait(driver_principal, 10).until(
        EC.presence_of_element_located((By.ID, "hs-eu-decline-button"))
    ).click()

    driver_principal.get(f"https://loopleiloes.com.br/estoque?tipo=Leve&evento_data=2077-01-01&numero_veiculos={max_box}")
    box = get_all_boxes(driver_principal)[0]
    click_box_button(box)
    click_close(driver_principal)
    driver_principal.back()
    driver_principal.minimize_window()
    

    
    return driver_principal



def get_all_boxes(driver_principal):
    boxes = WebDriverWait(driver_principal, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "undefined"))
    )
    return boxes

def click_box_button(box):
    
    try:
        button = WebDriverWait(box, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "MuiButtonBase-root"))
        )
    
        button.click()
    except:
        click_box_button(box)
       
def click_close(driver_principal):
    button_close = WebDriverWait(driver_principal, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@data-testid='close-button']"))

    )
    button_close.click()


def get_dict_box(box):
    result = {
        "Data": "",
        "Comitente": "",
        "Marca": "",
        "Modelo": "",
        "Valor": 0,
        "Cidade":"",
        "Estado":"",
        "Link": "",
        "Monta": "",
        "Ano": "",     
    }
    valor = box.find_elements(By.CLASS_NAME, "MuiGrid-root.MuiGrid-container.MuiGrid-justify-content-xs-space-between")[1].text.split("\n")[1]
    valor = float(valor.replace(".", "").replace(",", ".").removeprefix("R$ "))
    link = box.find_element(By.TAG_NAME, "a").get_attribute("href")
    soap = BeautifulSoup(rq.get(link).text, "html.parser")
    h1 = soap.find_all("h1")
    text_descricao = h1[0].text
    marca_modelo = encontrar_marca_carro(text_descricao)
    padrao = r"\d{4}/\d{4}"
    try: 
        marca = marca_modelo[0]
        modelo = re.sub(padrao, "", marca_modelo[1])
    except:
        marca = ""
        modelo = text_descricao
    try:
        ano = re.findall(padrao, marca_modelo[1])[0]
    except:
        ano = ""
    score = soap.find("div", attrs={"role": "tooltip"}).get_attribute_list("data-score")[0] + "/" +"500"
    data = soap.find_all("div", string="Data do evento")[0].next_sibling.text
    data = re.findall(r"\d{2}/\d{2}/\d{4}", data)[0]
    local = soap.find_all("div", string="Local do evento")[0].next_sibling.text
    cidade = local.split(" - ")[0]
    estado = local.split(" - ")[1]
    
 
    result["Ano"] = ano
    result["Data"] = data
    result["Comitente"] = "Loop Leilões"
    result["Marca"] = marca
    result["Modelo"] = modelo
    result["Valor"] = valor
    result["Cidade"] = cidade
    result["Estado"] = estado
    result["Link"] = link
    result["Monta"] = score
    return result



def process_box(box):
    try:
        return get_dict_box(box)
    except Exception as e:
        print(f"Error processing card: {str(e)}")
        update_errors("loop_leiloes", str(e))


def get_all_loop_leiloes():
    print("Loop Leilões")
    driver_principal= get_loop_driver()
    boxes = get_all_boxes(driver_principal)
    threads = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_results = [executor.submit(process_box, box) for box in boxes]

        for future in concurrent.futures.as_completed(future_results):
            try:
                result = future.result()
                yield result
            except Exception as e:
                update_errors("loop_leiloes", str(e))
                print(f"Error processing card: {str(e)}")
    driver_principal.quit()

    print("Encerrando crawling de loop leilões")


if __name__ == "__main__":
    for i in get_all_loop_leiloes():
        print(i)