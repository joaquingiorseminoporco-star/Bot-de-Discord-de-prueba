#Importo pathlib, csv y json
from pathlib import Path
import csv
import json
import asyncio
import io
import aiofiles



#                                   ------Analizando el json------

async def crear_csv():
    
    ruta_json = Path(Path.cwd()/ "Clima" / "json_datos_formatos.json" )
    
    try:
        async with aiofiles.open(ruta_json, mode = "r", encoding = "utf-8") as file:
            contenido = await file.read()
        
        datos_argentina_json = json.loads(contenido)

        columnas = ["Ubicaciones", "Temperatura en Centigrados"]
        lista_dict_climas = []
        for dict_clima in datos_argentina_json:
    
            provincia =  dict_clima.get("province")
            localidad =  dict_clima.get("name")
            temperatura =  dict_clima.get("weather")
            temperatura = temperatura.get("temp")
            ubicacion = f"{provincia}, {localidad}"

    
            diccionarios_climas = {
                "Ubicaciones" : ubicacion ,
                "Temperatura en Centigrados" : temperatura,

            }
            lista_dict_climas.append(diccionarios_climas)
    
    
        #Escribiendo todo en un csv
        flujo = io.StringIO()
        escribiendo_csv = csv.DictWriter(flujo, fieldnames = columnas)
    
        escribiendo_csv.writeheader()
        escribiendo_csv.writerows(lista_dict_climas)
        contenido_csv = flujo.getvalue()
    
        async with aiofiles.open("datos_climas.csv", mode = "w", encoding = "utf-8", newline = "") as iofile:
            await iofile.write(contenido_csv)
    
        print("archivo io creado exitosamente")

    except FileNotFoundError:
        
        print("El archivo JSON no existe")
        
        
asyncio.run(crear_csv())
    


    
    



