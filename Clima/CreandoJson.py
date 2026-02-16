from pathlib import Path
import json
import asyncio
import aiohttp



#Funcion que realiza la llamada al internet
async def llamada(url = "https://ws.smn.gob.ar/map_items/weather", nombre_json = "json_datos_formatos.json"):
    #Abro una sesión
    async with aiohttp.ClientSession() as sesion:
        #Realizo la llamada (descargo la información en la ram)
        async with sesion.get(url) as respuesta:
            
            #verificando si la llamada se realizo exitosamente
            if respuesta.status == 200:
                print("La llamada se ha realizado exitosamente")
        
            #Abriendo la ruta del nuevo archivo json
            ruta = Path.cwd() / "Clima" / nombre_json
        
            #Vuelvo al json legible con indent = 4
            json_formato = await respuesta.json()
            json_subido =  json.dumps(json_formato, indent = 4)
        
            #Escribo el texto
            ruta.write_text(json_subido)
        

        

    