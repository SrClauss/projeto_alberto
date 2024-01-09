from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from tools import get_monta, encontrar_marca_carro, update_errors
import re

all = 1
MAX_TENTATIVAS = 100
tentativas = 1
def set_table_size(driver_pagina):
    
        select = Select(driver_pagina.find_element(By.XPATH, "//select[@name='serverSideDataTable_length']"))
        select.select_by_index(2)
        time.sleep(3)
        global all
        return int(WebDriverWait(driver_pagina, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "paginate_button")))[-3].text)


def clicar_em_personalizar(driver_pagina):
    global tentativas
    try:
        botao_personalizar = WebDriverWait(driver_pagina, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-uname='lotsearchCustomize']"
                                       )))
        botao_personalizar.click()
        
        tentativas = 1
        
    except:
        time.sleep(0.5)
        print("erro ao carregar o botão personalizar, fazendo mais {} tentativas".format(tentativas))
        tentativas += 1
        clicar_em_personalizar(driver_pagina)


def personalizar_pesquisa(driver_pagina):
    global tentativas



    
    options = WebDriverWait(driver_pagina, 10).until(
        EC.presence_of_element_located((By.ID, "multiselect_to"))).find_elements(By.TAG_NAME, "option")
    
    remover = WebDriverWait(driver_pagina, 10).until(
        EC.element_to_be_clickable((By.ID, "multiselect_leftSelected")))
    
    incluir = WebDriverWait(driver_pagina, 10).until(
        EC.element_to_be_clickable((By.ID, "multiselect_rightSelected")))
    
    confirmar = WebDriverWait(driver_pagina, 10).until(
        EC.element_to_be_clickable((By.ID, "custViewCnfBttn")))
    
    time.sleep(1)
    for option in options:
        option.click()
        remover.click()
    ano_fabricacao = WebDriverWait(driver_pagina, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//option[@value='manufacture_year']")))
    ano_fabricacao.click()
    
    incluir.click()
    damage_classification = driver_pagina.find_element(
        By.XPATH, "//option[@value='damage_classification']")
    damage_classification.click()
    incluir.click()
    sale_date_utc = driver_pagina.find_element(
        By.XPATH, "//option[@value='sale_date_utc']")
    sale_date_utc.click()
    incluir.click()
    auction_host_name = driver_pagina.find_element(
        By.XPATH, "//option[@value='auction_host_name']")
    auction_host_name.click()
    incluir.click()
    confirmar.click()

    tentativas = 1


def excluir_vendas_futuras(driver_pagina):
    global tentativas
    try:
        excluir_vendas_futuras = WebDriverWait(driver_pagina, 10).until(
            EC.element_to_be_clickable((By.ID, "upcoming_Lots"
                                        )))

        excluir_vendas_futuras.click()
        tentativas = 1
    except:
        time.sleep(0.5)
        print("erro ao excluir vendas futuras, fazendo mais {} tentativas".format(tentativas))
        tentativas += 1
        excluir_vendas_futuras(driver_pagina)
        

def filtrar_categoria_Automoveis(driver_pagina):
    global tentativas
    try:
        categoriaAutomveis = driver_pagina.find_element(
            By.ID, "categoriaAutomveis")
        categoriaAutomveis.click()
        tentativas = 1
    except:
        time.sleep(0.5)
        print("erro ao filtrar categoria automoveis, fazendo mais {} tentativas".format(tentativas))
        tentativas += 1
        filtrar_categoria_Automoveis(driver_pagina=driver_pagina)

def filtrar_categoria_picapes(driver_pagina):
    global  tentativas
    try:
        categoriaPicapesGrandes = driver_pagina.find_element(
            By.ID, "categoriaPicapesGrandes")
        categoriaPicapesGrandes.click()
        tentativas = 1
    except:
        time.sleep(0.5)
        print("erro ao filtrar categoria picapes, fazendo mais {} tentativas".format(tentativas))
        tentativas += 1
        filtrar_categoria_picapes(driver_pagina=driver_pagina)
       
def filtrar_categoria_SUV_Pequenos(driver_pagina):
    global tentativas
    try:
        categoriaSUVPequenos = driver_pagina.find_element(
            By.ID, "categoriaSUVPequenos")
        categoriaSUVPequenos.click()
        tentativas = 1
    except:
        time.sleep(0.5)
        print("erro ao filtrar categoria SUV pequenos, fazendo mais {} tentativas".format(tentativas))
        tentativas += 1
        filtrar_categoria_SUV_Pequenos(driver_pagina=driver_pagina)

def filtrar_categoria_SUV_Grandes(driver_pagina):
    global tentativas
    try:
        categoriaSUVGrandes = driver_pagina.find_element(
            By.ID, "categoriaSUVGrandes")
        categoriaSUVGrandes.click()
        tentativas = 1
    except:
        time.sleep(0.5)
        print("erro ao filtrar categoria SUV grandes, fazendo mais {} tentativas".format(tentativas))
        tentativas += 1
        filtrar_categoria_SUV_Grandes(driver_pagina=driver_pagina)

def filtrar_categoria_Picapes_Pequenos(driver_pagina):
    global tentativas
    try:
        categoriaPicapesPequenas = driver_pagina.find_element(
            By.ID, "categoriaPicapesPequenas")
        categoriaPicapesPequenas.click()
        tentativas = 1
    except:
        time.sleep(0.5)
        print("erro ao filtrar categoria picapes pequenos, fazendo mais {} tentativas".format(tentativas))
        tentativas += 1
        filtrar_categoria_Picapes_Pequenos(driver_pagina=driver_pagina)

def filtrar_categoria_utilitarios_pequenos(driver_pagina):
    global tentativas
    try:
        categoriaUtilitriosPequenos = driver_pagina.find_element(
            By.ID, "categoriaUtilitriosPequenos")
        categoriaUtilitriosPequenos.click()
        tentativas = 1
    except:
        time.sleep(0.5)
        print("erro ao filtrar categoria utilitarios pequenos, fazendo mais {} tentativas".format(tentativas))
        tentativas += 1
        filtrar_categoria_utilitarios_pequenos(driver_pagina=driver_pagina)
def filtrar_categoria_utilitarios_grandes(driver_pagina):
    global tentativas
    try:
        categoriaUtilitriosGrandes = driver_pagina.find_element(
            By.ID, "categoriaUtilitriosGrandes")
        categoriaUtilitriosGrandes.click()
        tentativas = 1
    except:
        time.sleep(0.5)
        print("erro ao filtrar categoria utilitarios grandes, fazendo mais {} tentativas".format(tentativas))
        tentativas += 1
        filtrar_categoria_utilitarios_grandes(driver_pagina=driver_pagina)
       
def filtrar_tudo(driver_pagina):

    filtrar_categoria_Automoveis(driver_pagina)
    filtrar_categoria_picapes(driver_pagina)
    filtrar_categoria_SUV_Pequenos(driver_pagina)
    filtrar_categoria_SUV_Grandes(driver_pagina)
    filtrar_categoria_Picapes_Pequenos(driver_pagina)
    filtrar_categoria_utilitarios_pequenos(driver_pagina)
    filtrar_categoria_utilitarios_grandes(driver_pagina)

def logar(driver_pagina):
    global tentativas
    try:
        input_email = WebDriverWait(driver_pagina, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/div[3]/div[1]/div/div/div[2]/div/div/form/div/div[1]/div[4]/input"))
        )
        input_email.send_keys("clausembergrodrigues@gmail.com")
        driver_pagina.find_element(By.XPATH,
                                "/html/body/div[3]/div[1]/div/div/div[2]/div/div/form/div/div[3]/div[2]/input").send_keys(
            "AnEfeJ2yFdFfno")
        driver_pagina.find_element(By.XPATH,
                                "/html/body/div[3]/div[1]/div/div/div[2]/div/div/form/div/div[5]/button").click()
        tentativas = 1
    except:
        if tentativas < MAX_TENTATIVAS:
            time.sleep(0.5)
            print("erro ao logar, fazendo mais {} tentativas".format(tentativas))
            tentativas += 1
            logar(driver_pagina)
        else:
            raise Exception("erro ao logar")
        


def get_copart_driver():
    driver_option = webdriver.ChromeOptions()
    driver_option.add_argument("--blink-settings=imagesEnabled=false")

    driver_pagina = webdriver.Chrome(driver_option)
    driver_pagina.get(
        "https://www.copart.com.br/search/autom%C3%B3veis/?displayStr=Autom%C3%B3veis&from=%2FvehicleFinder")
    driver_pagina.maximize_window()

    clicar_em_personalizar(driver_pagina=driver_pagina)
    logar(driver_pagina)
    clicar_em_personalizar(driver_pagina=driver_pagina)
    personalizar_pesquisa(driver_pagina=driver_pagina)
    filtrar_tudo(driver_pagina)
    excluir_vendas_futuras(driver_pagina=driver_pagina)
    global all
    all = set_table_size(driver_pagina=driver_pagina)

    WebDriverWait(driver_pagina, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))

    
    return driver_pagina

def click_next_page(driver_pagina):
    global tentativas
    try:
        next = WebDriverWait(driver_pagina, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Próximo')]")))
        next.click()
        tentativas = 1
    except:
        time.sleep(0.5)
        print("erro ao carregar o botão next, fazendo mais {} tentativas".format(tentativas))
        tentativas += 1
        click_next_page(driver_pagina=driver_pagina)

def get_all_copart_pages(driver_pagina):
   

    

    for i in range(all-1):
        
        for j in get_copart_page(driver_pagina):
            try:
                yield j
            except Exception as e:
                update_errors("copart", str(e))
        click_next_page(driver_pagina=driver_pagina)
    
    driver_pagina.quit()

    
    


def get_copart_page(driver_pagina):
    time.sleep(2)


    trs = WebDriverWait(driver_pagina, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//tbody/tr")))
    copart_erros = 0
    for tr in trs:
        try:
            yield get_copart_row(tr)
        except Exception as e:
            update_errors("copart", str(e))


    


def get_copart_row(tr):

    result = {
        "Data": "",
        "Comitente": "",
        "Marca": "",
        "Modelo": "",
        "Valor": "",
        "Cidade": "",
        "Estado": "",
        "Link": "",
        "Monta": "",
        "Ano": "",
    }
    tds = WebDriverWait(tr, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "td")))
    result["Data"] = tds[9].text.split("\n")[0].replace(".", "/")
    result["Comitente"] = "Copart"
    result["Marca"] = tds[4].text
    result["Modelo"] = tds[5].text
    result["Valor"] = float(re.findall(r"R\$[\s]*\d{1,3}(?:\.\d{3})*(?:,\d{2})", tds[11].text)[0].removeprefix("R$ ").replace(".", "").replace(",", "."))
    result["Cidade"] = tds[10].text.split(" - ")[0]
    result["Estado"] = tds[10].text.split(" - ")[1]
    result["Link"] = tds[1].find_element(
        By.TAG_NAME, "a").get_attribute("href")
    result["Monta"] = get_monta(tds[8].text)
    result["Ano"] = tds[7].text + "/" + tds[3].text
    
    return result

if __name__ == "__main__":
    for i in get_all_copart_pages(get_copart_driver()):
        print(i)