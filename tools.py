import json



def get_monta(string):
    string = string.replace("\n", " ").lower()
    if "pequena monta" in string:
        return "PEQUENA MONTA"
    elif "media monta" in string:
        return "MÉDIA MONTA"
    elif "média monta" in string:
        return "MÉDIA MONTA"
    elif "grande monta" in string:
        return "GRANDE MONTA"
    elif "sucata" in string:
        return "SUCATA"
    elif "sinistrado" in string:
        return "SINISTRADO"
    elif "sinistro" in string:
        return "SINISTRO"
    elif "seguradora" in string:
        return "SEGURADORA"
    return "NÃO INFORMADO"

def encontrar_marca_carro(string):
    marcas_carros = [
        "Acura", "Alfa Romeo", "Aston Martin", "Audi", "BAIC", "BMW", "Bentley",
        "Brilliance", "Bugatti", "Buick", "BYD", "Cadillac", "Chana", "Changan",
        "Chery", "Chevrolet", "Chrysler", "Citroën", "Datsun", "Dodge", "Dongfeng",
        "FAW", "Ferrari", "Fiat", "Ford", "Foton", "GAC", "GMC", "Geely",
        "Great Wall", "Haima", "Haval", "Hawtai", "Honda", "Hongqi", "Hyundai",
        "Infiniti", "JAC", "JMC", "Jaguar", "Jeep", "Jinbei", "Kia", "Lamborghini",
        "Lancia", "Land Rover", "Lexus", "Lifan", "Lincoln", "Lotus",
        "Maserati", "Mazda", "Mercedes-Benz", "Mini", "Mitsubishi", "Nissan",
        "Peugeot", "Porsche", "RAM", "Renault", "Rolls-Royce", "Roewe", "Land Rover",
        "SsangYong", "Subaru", "Suzuki", "TAC", "Tesla", "Toyota", "Troller",
        "Volkswagen", "Volvo", "Vortex", "Wuling", "Yudo", "Zhidou", "Zotye", "VW", "GM", "MMC",
        "Chev", "LR", "Citroen"]
    
    
    for brand in marcas_carros:
        
        if brand.lower() in string.lower():
            start = string.lower().index(brand.lower())
            model = string[start + len(brand):].strip()
            

            if brand.upper() == "GM":
                brand = "General Motors"
            elif brand.upper() == "VW":
                brand = "VOLKSWAGEN"
            elif brand.upper() == "MMC":
                brand = "MITSUBISHI"
            elif brand.upper() == "LR":
                brand = "LAND ROVER"
            elif brand.upper() == "CITROEN":
                brand = "CITROËN"
            elif brand.upper() == "CHEV":
                brand = "CHEVROLET"
            
            return brand, model

  

                    
        
      
    return "", string



def clear_errors():
 
 errors = {
     "copart": [],
     "daniel_garcia": [],
     "freitas": [],
     "grupo_leilo": [],
     "loop_leiloes": [],
     "superbid": [],
     "vip_leiloes": []
 }
 
 with open("errors.json", "w") as file:
     json.dump(errors, file)

    


def update_errors(key, error):
    with open("errors.json", "r") as file:
        errors = json.load(file)
    
    errors[key].append(error)

    with open("errors.json", "w") as file:
        json.dump(errors, file)

