import discord
from discord.ext import commands, tasks
import json
from pathlib import Path
from random import randint, choice
import asyncio 
import sys

#Trayendo las carpetas de afuera 
carpeta = Path(Path(__file__).resolve().parent.parent / "Clima" )
sys.path.append(str(carpeta))

import ClimaArg
import LeyendoCSV
import CreandoJson

carpeta = Path(__file__).resolve().parent.parent / "Dolar"
print(carpeta)
sys.path.append(str(carpeta))

import maindolar

print(carpeta)

#Creo la ruta al archivo
config = Path(Path.cwd() / "Bot" /"config.json").read_text()
#Cargo el archivo
config_json = json.loads(config)
print(config_json)


#Dandole permisos
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# 3. Crear el bot
bot = commands.Bot(command_prefix=config_json["PREFIX"], intents=intents)

#Creo un bucle con task que se repite cada 5 segundos y dice manteca
@tasks.loop(seconds=30)
async def manteca():
    #lista con todos los servidores
    for servidor in bot.guilds:
        
        #busco el canal general de este servidor
        canal = discord.utils.get(servidor.text_channels, name = "manteca")
        
        #verifico si existe el canal, y si existe mando el mensaje manteca juju
        if canal is not None:
            
            elegir = randint(0,100)
            if elegir > 90:
                
                await canal.send("Mantecaaaaa, en 30 vuedvo a edcibid manteka jijojeudju")
                print(f"Enviado a {servidor.name}")
            else:
                await canal.send("mmmm manteca mantecosa...")
                await asyncio.sleep(2)
                await canal.send("En 30 vuedvo jujoijkukasdkeio")
        else:
            
            print(f"Ed dervidor {servidor.name} no tiene un canad llamado genedal jujjujiju")

@manteca.before_loop
async def antes_manteca():
    await bot.wait_until_ready()
   
    
# Evento: Cuando el bot se conecta
@bot.event
async def on_ready():
    print(f'✅ ¡Éxito! El bot está conectado como: {bot.user}')
    manteca.start()

# Comando: !hola
@bot.command()
async def holaserver(ctx):
    await ctx.send(f'¡Hola! {ctx.author}, bienvenido a {ctx.guild}.')

#Comando simple que te tira los dados
@bot.command()
async def tirameundado(ctx):
    await ctx.send(f"Pibe, mira, te voy a tirar un dado. abed qe salio. Uh bodudo sasdio un {randint(1,6)}, jeje manteca")

#comando que te dice quienes estan
@bot.command()
#pongo de argumento context para poder usar info el servidor
async def usuarios(ctx):
   # usuarios = [] #lista vacia
    for member in ctx.guild.members:
        #usuarios.append(member.name)
        await ctx.send(member.name)
        
#Creo un comando que hace que Alonso eliga con quien se casa

@bot.command()
#de argumento context para usar la lista de usuarios
async def casamiento(ctx):
    #agarro a todos los usuarios en una lista
    usuarios = []
    for member in ctx.guild.members:
        usuarios.append(member.name)
    await ctx.send(f"Ehh casadme con aldguien???")
    await asyncio.sleep(2)
    await ctx.send(f"Emmm.....")
    await asyncio.sleep(3)
    await ctx.send(f"buedo buedo fue, me caso con {choice(usuarios)}")
        
#Comando que devuelve el clima de capital federal
@bot.command()
async def clima(ctx):
    await ctx.send("Adi te pado el clima de capital fedeheral jejeje mantecubi")
    for lineas in await LeyendoCSV.leyendo():
        await asyncio.sleep(1)
        await ctx.send(f"La zona es {lineas[0]} y la temperatura es {lineas[1]} grados sentigrados jejjdujjujuj manteca")
            
@bot.command()
async def oficial(ctx):
    await ctx.send("Pada bodudo, adi te diho cuanto esta el doddar ofidiald jasjsaas mantecaaaaaa")
    dolar_oficial_contenido = await maindolar.hacer_todo()
    
    await ctx.send(f"Ed dipo te cambio pada ed dodar e {dolar_oficial_contenido[1][1]}y su vadod eh de")
    await asyncio.sleep(1)
    await ctx.send(f"Naaa bodudooo, te pasa mad, e un monton")
    await ctx.send(f"{dolar_oficial_contenido[1][2]}")
    await asyncio.sleep(2)
    await ctx.send(f"aaaa y cadi de me odvida bodulo, esto fue atualizado pod udtima bes {dolar_oficial_contenido[1][3]}")
        


# 4. Encender
bot.run(config_json["TOKEN"])