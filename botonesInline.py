from config import *
import telebot # Para manejar la API de telegram
# Botones Inline
from telebot.types import InlineKeyboardMarkup # Para crear botonoes inline
from telebot.types import InlineKeyboardButton # Para definir los botones inline
import requests
from bs4 import BeautifulSoup
import os
import pickle

N_RES_PAG = 5 # Numero de resultados a mostrar en cada pagina
MAX_ANCHO_ROW = 8 # Maximo de botones por fila(limitacion de telegram)
DIR = {"busquedas": "./busquedas/"} # Donde se guardaran los archivos de las busquedas

for key in DIR: # Creamos los directorios definidos
    try:
        os.mkdir(key)
    except:
        pass

# Instanciamos el bot de telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Responde al comando /botones
@bot.message_handler(commands=["botones"])
def  cmd_botones(message):
    # Muestra un mensaje con botones inlien (a continuacion del mensaje)
    markup = InlineKeyboardMarkup(row_width = 2) # Numero de botones en cada fila | 3 por defecto
    b1 = InlineKeyboardButton("Pagina Oficial", url = "https://retrogeeksla.blogspot.com/")
    b2 = InlineKeyboardButton("Kakushigoto", url = "https://retrogeeksla.blogspot.com/2022/03/kakushigoto_7.html")
    b3 = InlineKeyboardButton("Go-Tōbun no Hanayome S2", url = "https://retrogeeksla.blogspot.com/2021/01/go-toubun-no-hanayome-s2_18.html")
    b4 = InlineKeyboardButton("Re:Zero kara Hajimeru", url = "https://retrogeeksla.blogspot.com/2022/02/rezero-kara-hajimeru-isekai-seikatsu_16.html")
    b5 = InlineKeyboardButton("Yesterday wo Utatte", url = "https://retrogeeksla.blogspot.com/2020/06/yesterday-wo-utatte_10.html")
    b6 = InlineKeyboardButton("Tsugumomo", url = "https://retrogeeksla.blogspot.com/2020/06/tsugumomo_39.html")
    b7 = InlineKeyboardButton("Hunter x Hunter (2011)", url = "https://retrogeeksla.blogspot.com/2020/06/hunter-x-hunter-2011_42.html")
    b8 = InlineKeyboardButton("Gakusen Toshi Asterisk", url = "https://retrogeeksla.blogspot.com/2020/06/gakusen-toshi-asterisk_59.html")
    b9 = InlineKeyboardButton("Tengen Toppa Gurren Lagann", url = "https://retrogeeksla.blogspot.com/2020/07/tengen-toppa-gurren-lagann_50.html")
    b_cerrar = InlineKeyboardButton("Cerrar", callback_data="cerrar")
    markup.add(b1, b2, b3, b4, b5, b6, b7, b8, b9, b_cerrar)
    bot.send_message(message.chat.id, "Mis paginas de anime", reply_markup = markup)

@bot.callback_query_handler(func = lambda x: True) # Hacemos de funciones lambda, son funciones anonimas es decir que no hemos definido previamente
def respuesta_botonesInline(call):
    # Gestiona las acciones de los botones callback_data
    cid = call.from_user.id # cid = chat id
    mid = call.message.id # mid = message id
    if call.data == "cerrar": # Boton cerrar
        bot.delete_message(cid, mid)
        return
    datos = pickle.load(open(f'{DIR["busquedas"]}{cid}_{mid}','rb'))
    if call.data == "anterior": # Boton anterior
    # Si ya estamos en la primera pagina
        if datos["pag"] == 0:
            bot.answer_callback_query(call.id, "Ya estas en la primera pagina")
        else:
            datos["pag"]-= 1 # Retrocedemos una pagina
            pickle.dump(datos, open(f"{DIR['busquedas']}{cid}_{mid}","wb"))
            mostrar_pagina(datos["lista"], cid, datos["pag"], mid)
        return
    elif call.data == "siguiente":
        # Si ya estamos en la ultima pagina
        if datos["pag"] * N_RES_PAG + N_RES_PAG >= len(datos["lista"]):
            bot.answer_callback_query(call.id, "Ya estas en la ultima pagina")
        else:
            datos["pag"]+= 1 # Avanzamos una pagina
            pickle.dump(datos, open(f"{DIR['busquedas']}{cid}_{mid}","wb"))
            mostrar_pagina(datos["lista"], cid, datos["pag"], mid)
        return
            
# Buscador de google en telegram
# Responde al comando /buscar
@bot.message_handler(commands=["buscar"])
def cmd_buscar(message):
    # Realiza una busqueda en google, y devuelve una lista de listas de los resultados
    # con la siguiente estructura [[titulo, url], [titulo, url]...]
    texto_buscar = " ".join(message.text.split()[1:])
    # Controlamos si hay parametros | si no se han pasado parametros
    if not texto_buscar:
        texto = "Debes introducir una busqueda.\n" # Definimos un string
        texto+= "Ejemolo:\n" # Le indicamos ya formateado como deberia ingresar
        texto+= f"<code>{message.text} RetroGeeks</code>"
        bot.send_message(message.chat.id, texto, parse_mode="html") # Enviamos el mensaje
        return 1 # Devolvemos 1 para indicar un error
    #Si se ha indicado un texto de busqueda
    else:
        print(f"Buscando en google:'{texto_buscar}'") 
        url = f'https://www.google.com/search?q={texto_buscar.replace(" ","+")}&num=100' # La url nos devuelve 30 resultados, pero podemos obtener hasta un maximo de 100
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33"
        headers = {"user-agent": user_agent}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code !=200:
            print(f"Error al buscar: {res.status_code} {res.reason}")
            bot.send_message(message.chaat.id, "Se ha producido un error. Intentalo más tarde")
            return 1
        else:
            soup = BeautifulSoup(res.text, "html.parser")
            elementos = soup.find_all("div", class_="g")
            lista = []
            for elemento in elementos:
                try:
                    titulo = elemento.find("h3").text
                    url = elemento.find("a").attrs.get("href")
                    if not url.startswith("http"):
                        url = "https://www.google.com/" + url
                    if [titulo, url] in lista:
                        continue
                    lista.append([titulo, url])
                except:
                    continue
        # print(lista) # Para comprobar el ingreso de datos
        mostrar_pagina(lista, message.chat.id)
        
# Crea o edita un mensaje de la pagina   
def mostrar_pagina(lista, cid, pag = 0, mid=None):
# Creamos la botonera
    markup = InlineKeyboardMarkup()
    b_anterior = InlineKeyboardButton("←", callback_data="anterior") # Boton de pagina anterior
    b_cerrar = InlineKeyboardButton("X", callback_data="cerrar") # Boton de cerrar
    b_siguiente = InlineKeyboardButton("→", callback_data="siguiente") # Boton de pagina siguiente
    inicio = pag*N_RES_PAG # Nro resultado inicio de pagina en curso
    fin =  inicio + N_RES_PAG # Nro resultado fin de pagina en curso | fin = pag * N_RES_PAG + N_RES_PAG
    markup.row(b_anterior, b_cerrar, b_siguiente) # Ponemos lo botones
    mensaje = f'<i>Resultados {inicio+1}-{fin} de {len(lista)}</i>\n\n' # Este seria el encabezado del mensaje
    # Montamos el listado de los resultados
    n = 1
    for item in lista[inicio:fin]:
        mensaje+= f'[<b>{n}</b>] <a href="{item[1]}"> {item[0]}</a>\n' # Añadimos texto 
        n+= 1
    if mid:
        bot.edit_message_text(mensaje, cid, mid, reply_markup=markup, parse_mode="html", disable_web_page_preview=True)
    else:
        res = bot.send_message(cid, mensaje, reply_markup=markup, parse_mode="html", disable_web_page_preview=True)
        mid = res.message_id
        datos = {"pag":0, "lista": lista}
        pickle.dump(datos, open(f"{DIR['busquedas']}{cid}_{mid}","wb"))
        
# Programa principal
if __name__ == "__main__":
    print("INIICIANDO BOT")
    bot.infinity_polling()
    

    
    
    
    