from pathlib import Path
import io
import aiofiles
import csv
from ClimaArg import crear_csv
from CreandoJson import llamada
import asyncio

async def leyendo(archivo = Path("datos_climas.csv")):
    #Funcion que devuelve el clima de Capital Federal
    
    #Llamo a las 2 funciones necesarias
    await llamada()
    await crear_csv()
    
    #Abro el archivo con aiofiles 
    async with aiofiles.open(archivo, mode = "r", encoding = "utf-8") as f:
        #leo el archivo de forma asincronica
        contenido = await f.read()
        
        #abro el contenido con reader que espera un iterable, motivo por el cual uso splitlines()
        archivo_csv = csv.reader(contenido.splitlines())
        #creo una lista vacia en la que se alamacenaran los datos utiles 
        lineas_utiles = []
        #bucle que busca en todas las lineas cuales contienen los datos necesarios
        for linea in archivo_csv:
            if "Capital Federal" in linea[0]: 
                #añade las listas a la lista de datos utiles
                lineas_utiles.append(linea)
    
    #Borro el csv para que no consuma espacio
    archivo_csv = Path.cwd() / "datos_climas.csv"
    archivo_json = Path.cwd()/ "Clima" / "json_datos_formatos.json"
    print(archivo_csv)
    print(archivo_json)
    if archivo_csv.exists():
        #lo borro
        archivo_csv.unlink()
    
    if archivo_json.exists():
        #same thing
        archivo_json.unlink()

    return lineas_utiles  


    


    


