from config import *
import os
import sys
import telebot
import time
import requests
from bs4 import BeautifulSoup
from iniciar_Webdriver import iniciar_webdriver
from selenium.webdriver.support.ui import WebDriverWait #Para esperar elementos en selenuim
from selenium.webdriver.common.by import By #Para esperar por tipos de elemento
from selenium.webdriver.support import expected_conditions as ec
import threading # Para poder crear hilos

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=["inicio"]) 
def cmd_start(message):
    bot.send_message(message.chat.id, "Envia un enlace de un producto de amazon o mediamarkt")
    
@bot.message_handler(commands=["captura"]) 
def cmd_captura(message):
    driver.save_screenshot("captura.png")
    bot.send_document(message.chat.id, open("captura.png", "rb"))
    
@bot.message_handler(content_types=["text"]) 
def bot_texto(message):
    # Si el mensaje comienza por http
    if message.text.lower().startswith("http"):
        datos = None
        if "amazon.com" or "amazon.es" in message.text.lower():
            datos = datos_Amazon(message.text)
        elif "mediamarkt.es" in message.text.lower():
            datos = datos_Mediamarkt(message.text)
        else:
            texto = "Error: Enlace no valido"
        if datos:
            texto = datos["nombre"] + "\n"
            texto+= f'Precio: {datos["precio"]}'
    else:
        texto = "Error: Esto no es un enlace"
    print(texto)
    bot.send_message(message.chat.id, texto)
    
def datos_Mediamarkt(url):
    # Devuelve el nombre y precio de un producto de Mediamarkt
    print("Scraping en mediamarkt con selenium")
    # Iniciamos el diccionario de salida
    datos = {}
    # Cargamos la pagina en chrome
    driver.get(url)
    # Nombre del producto
    try:
        datos["nombre"] = driver.find_element(By.TAG_NAME,"h1").text
    except:
        datos["nombre"] = ""
        # Precio actual del producto
    if datos["nombre"]:
        try:
            elemento = wait.until(ec.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class, 'BrandedPrice')]")))
            datos["precio"] = elemento.text.replace("\n", "").replace(".-", "")
        except:
            datos["precio"] = ""
    else:
        datos["precio"] = ""
    return datos
        
def datos_Amazon(url):
    # Deveulve el nombre y precio de un producto de amazon
    print("Scraping den amazon con request y beautiSoup")
    headers = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27",
        "referer": "https://www.google.es", # Para evitar que aparezcan captchas
        }
    # Realizamos la peticion
    req = requests.get(url, headers=headers, timeout=10)
    # Preparamos la sopa
    soup = BeautifulSoup(req.text, "html.parser")
    # Inicializamos el diccionario de salida
    datos = {}
    # Nombre del producto
    try:
        datos["nombre"] = soup.find(id="productTitle").text.strip()
    except:
        datos["nombre"] = ""
        # Precio actual del producto
    try:
        datos["precio"] = soup.find("span", class_="priceToPay").find("span").text
    except:
        try: 
            datos["precio"] = soup.find("span", class_="apexPriceToPay").find("span").text
        except:
            datos["precio"] = ""
    return datos
        
def polling():
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling()
    
# Main
if __name__ == "__main__":
    print("INIICIANDO BOT")        
    driver = iniciar_webdriver()
    wait = WebDriverWait(driver, 20)
    driver.get("https://www.mediamarkt.es/")  
    # Clic en Aceptar todas las cookies
    try:
        elemento = driver.find_element(By.ID, "pwa-consent-layer-accept-all-button")
        elemento.click()
        print("Clic en aceptar cookies")
    except:
        pass
    # Iniciamos la recepcion de mensajes en telegram
    print("Iniciando telebot")
    hilo = threading.Thread(name="hilo_polling", target=polling)
    hilo.start()
    print("Bot Iniciado")
    bot.send_message(MI_CHAT_ID, "Bot iniciado")
    # Mostramos un cronometro del tiempo transcurrido desde el inicio del bot
    mid = bot.send_message(MI_CHAT_ID, "Esperando").message_id
    inicio = time.time() #Timestamp de inicio
    while True:
        time.sleep(1)
        segundos = round(time.time() -inicio)
        minutos = round(segundos // 60)
        segundos = segundos - (minutos * 60)
        reloj = f"{minutos}:{segundos:02d}"
        try:
            bot.edit_message_text(f' ⏰ <code>{reloj}</code>', MI_CHAT_ID, mid, parse_mode='html')
        except:
            pass        
        
        
            
        
        
        