import datetime
import json
from tkinter import Button, Tk, Checkbutton, filedialog, messagebox
from copart import get_all_copart_pages, get_copart_driver
from daniel_garcia import get_all_daniel_garcia_pages
from freitas import get_all_freitas_cards, get_freitas_driver
from grupo_leilo import get_all_leilo_pages
from loop_leiloes import get_all_loop_leiloes
from superbid import get_all_superbid_pages, get_max_superbid_page
from vip_leiloes import get_all_vipleiloes_pages
from openpyxl import Workbook
import pandas as pd
from tools import clear_errors, save_errors
import threading
from tools import errors, SCRIPT_ID, URL
import requests
def get_leiloes():
   
    

    clear_errors()
    columns=["Data", "Comitente", "Marca", "Modelo", "Valor", "Cidade", "Estado", "Link", "Monta", "Ano"]

    wb = Workbook()
    ws = wb.active
    ws.title = "Leilões"
    ws.append(columns)
    ws.column_dimensions["A"].width = 10
    ws.column_dimensions["B"].width = 10
    ws.column_dimensions["C"].width = 15
    ws.column_dimensions["D"].width = 40
    ws.column_dimensions["E"].width = 20
    ws.column_dimensions["F"].width = 20
    ws.column_dimensions["G"].width = 10
    ws.column_dimensions["H"].width = 60
    ws.column_dimensions["I"].width = 20
    ws.column_dimensions["J"].width = 10
    wb.save("leiloes.xlsx")


    def tab_dict(dict):
        s = ""
        for value in dict.values():
            s+= str(value) + "\t"
        return s + "\n"
    
    
    def append_to_excel(ws, function, file):
        lock = threading.Lock()
        columns = ["Data", "Comitente", "Marca", "Modelo", "Valor", "Cidade", "Estado", "Link", "Monta", "Ano"]
        output = pd.DataFrame(columns=columns)
        i = 0
        for dict in function():
            output.loc[i] = dict
            i+=1
            try:
                print(tab_dict(dict))
            except:
                pass
            
    
        for row in output.itertuples(index=False):
            ws.append([getattr(row, col) for col in columns])
        
        lock.acquire()
        wb.save(file)
        wb.close()
        lock.release()
    

    
    copart_driver = get_copart_driver()
    freitas_driver = get_freitas_driver()
    max_superbid_page = get_max_superbid_page()
    get_all_superbid = lambda : get_all_superbid_pages(max_superbid_page)
    get_all_copart = lambda : get_all_copart_pages(copart_driver)
    get_freitas_cards = lambda : get_all_freitas_cards(freitas_driver)
    


    functions = [
        get_all_copart,
        get_freitas_cards,
        get_all_daniel_garcia_pages,
        get_all_leilo_pages,
        get_all_loop_leiloes,
        get_all_superbid
        get_all_vipleiloes_pages,
        
    ]
    threads = []

    for f in functions:
        thread = threading.Thread(target=append_to_excel, args=(ws, f, "leiloes.xlsx"))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    save_errors()
    print("processo encerrado com os seguintes erros:")
    for key in errors:
        print(key + ": " + str(errors[key]))
    
    wb.save(filedialog.asksaveasfile(mode='w', defaultextension=".xlsx").name)




def button_click(event):
    get_leiloes()


if __name__ == "__main__":
    root = Tk()
    script = json.loads(requests.get(f"{URL}/get_script/" + SCRIPT_ID).text)
    
    if script["activate"]: 
        root.wm_title("Get Leilões - By: Alberto")
        button = Button(root, text="Get Leiloes")
        button.bind("<Button-1>", button_click)
        button.pack(padx=20, pady=20)
        root.geometry("500x100")
        root.mainloop()
    else:
        messagebox.showwarning("Aviso", "Script Desativado, para ativá-lo, entre em contato com o desenvolvedor",)
    