#Importando las bibliotecas necesarias

import aiohttp
import io
import aiofiles
import asyncio
from pathlib import Path
import json
import re
import datetime
import csv


#Haciendo la llamada a la api
async def llamada_dolar(url = "https://dolarapi.com/v1/dolares/oficial"):
    
    #Abriendo la sesion
    async with aiohttp.ClientSession() as sesion:
        #Haciendo la llamada
        async with sesion.get(url) as respuesta:
            
            #verificamos el estatus de la llamda
            if respuesta.status == 200:
                print("la llamada con la API dolar oficial se ha realizado exitosamente")
    
            #Veemos que datos nos trae
            contenido = await respuesta.json()
            contenido_json = json.dumps(contenido, indent = 4)
            
            ruta_dolar = Path(Path(__file__).parent / "dolar_oficial.json")
            ruta_dolar.write_text(contenido_json)
                    






#Funcion que crea un csv con los datos anteriormente obtenidos

async def csv_dolar():
    
    #Asigno la ruta
    ruta_dolar = Path(__file__).parent / "dolar_oficial.json"
    
    #Bucle while que verifica con un try/except que el archivo se encuentre, de no encontrarse, llama a la función
    #que lo crea
    while True:
        
        try:
            #Creo el with open pero con programación asincronica
            async with aiofiles.open(ruta_dolar, mode = "r") as archivo_dolar:
        
                #leo el archivo 
                contenido = await archivo_dolar.read()
        
            contenido_csv = json.loads(contenido)
        
            #creo un bucle que sacara todos los datos neesarios
    
            columnas = ["Moneda", "Tipo de cambio", "Valor", "Actualizado"]
    
            #Re llamo a contenido_csv como dict para que sea más entendible
            dict = contenido_csv
        
            #Sacando los valores para cada variable, posteriormente iran en un diccionario
            moneda = dict.get("moneda")
            tipo_cambio = dict.get("casa")
             
            compra = dict.get("compra")
            venta = dict.get("venta")
    
    
            #Uso expresiones regulares para: practicar y para separar fecha y hora
            fecha_hora = dict.get("fechaActualizacion")
            fecha_match = re.search(r"\d{4}-\d{2}-\d{2}", fecha_hora)
    
    
            if fecha_match:
                fecha = fecha_match.group()
            else:
                fecha = "S/D"
        
            hora_match = re.search(r"\d{2}:\d{2}:\d{2}", fecha_hora)  
    
            if hora_match:
                hora = hora_match.group()
            else:
                hora = "S/D"
        
            diccionario_de_valores = {
        
                "Moneda" : moneda,
                "Tipo de cambio" : tipo_cambio,
                "Valor" : f"Ed vador de venta es: {venta} y el valor de compra es: {compra}",
                "Actualizado" : f"Actualizado el {fecha}, a las {hora}"
        
                }
             
            #Escribiendo el csv
            flujo = io.StringIO()
            escritor = csv.DictWriter(flujo ,fieldnames = columnas)
            escritor.writeheader()
            escritor.writerow(diccionario_de_valores)
            contenido_csv = flujo.getvalue()
    
            async with aiofiles.open(Path(__file__).parent / "dolar_oficial.csv", mode = "w", encoding = "utf-8", newline = "") as csv_file:    
                await csv_file.write(contenido_csv)
    
            flujo.close()
            break
        
        except FileNotFoundError:
            print("No se encontro ningun archivo JSON, llamando a la función para que lo escriba")
            await llamada_dolar()
            continue
        



#Funcion que lee lo anotado en el csv y tras eso borra tanto la llamada como el csv

async def valor_dolar():
    
    ruta_csv = Path(__file__).parent / "dolar_oficial.csv"
    
    #Abro el archivo y extraigo su contenido
    async with aiofiles.open(ruta_csv, mode = "r", encoding = "utf-8") as datos_csv:
        
        contenido = await datos_csv.read()
    
    #Leo con csv reader
    
    contenido_csv = list(csv.reader(contenido.splitlines()))
    
    #Eliminando los archivos que ya no utilizaremos (json y csv)
    
    ruta_json = Path(__file__).parent / "dolar_oficial.json"
    
    if ruta_json.exists():
        ruta_json.unlink()
    
    if ruta_csv.exists():
        ruta_csv.unlink()
    
    return contenido_csv



async def hacer_todo():
    
    await llamada_dolar()
    await csv_dolar()
    
    return await valor_dolar()
