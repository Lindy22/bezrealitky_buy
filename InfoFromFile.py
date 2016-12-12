import csv
import os
import re
from datetime import datetime

locations = ["vinohrady",
             "stare_mesto",
             "nove_mesto",
             "karlin",
             "holesovice",
             "zizkov",
             "vysehrad",
             "vrsovice",
             "dejvice",
             "stresovice"]

text_reg = re.compile('(: .*)+')
#path where all the files with advertisements are
path = "C:\\Users\\Tomas\\Documents\\Python\\bezrealitky_proj\\buy\\"

for quarter in locations:   
    for filename in os.listdir(path+quarter+"\\"):
        print filename
        file_path = path+quarter+"\\"+filename
        with open(file_path, "r") as f:
            content = f.readlines()
            surface_line = [line for line in content if "Velikost: " in line]
            price_line = [line for line in content if "Cena: " in line]
            price_sq_line = [line for line in content if "Cena za metr: " in line]
            web_adress_line = [line for line in content if "Odkaz na web: " in line]
            
            if len(surface_line) > 0:
                surface = text_reg.findall(surface_line[0].strip("\n"))[0].strip(": ")
            else:
                surface = ""

            if len(price_line) > 0:
                price = text_reg.findall(price_line[0].strip("\n"))[0].strip(": ")
            else:
                price = "0"

            if len(price_sq_line) > 0:
                price_per_meter = text_reg.findall(price_sq_line[0].strip("\n"))[0].strip(": ")
            else:
                price_per_meter = "0"

            if len(web_adress_line) > 0:
                web_adress = text_reg.findall(web_adress_line[0])[0].strip(": ")
            else:
                web_adress = ""
            modification_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
            
            if os.path.exists("inzeraty_bezrealitky.csv") == False:
                with open ("inzeraty_bezrealitky.csv","ab") as f:
                    f.write("DateTime;WebAdress;Surface;Price;PricePerMeter;Location\n")
                f.close()
            with open ("inzeraty_bezrealitky.csv","ab") as f:
                f.write(str(modification_time) + ";" + web_adress + ";" + surface + ";" + price + ";" + price_per_meter + ";" + quarter +'\n')
            f.close()
