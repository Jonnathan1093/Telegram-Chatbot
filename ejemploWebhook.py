import time
from config import *
import telebot
from flask import Flask, request # Para crear el servidor 
from pyngrok import ngrok, conf # Para creaar un tunel entre nuestro servidor local e internet (url publica)
from waitress import serve # Para ejecutar el servidor en un entorno de produccion

#Instanciamos la API de telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Instanciamos el servidor web de Flask
web_server = Flask(__name__)

# Gestiona las peticiones POSTs enviadas al servidor web
@web_server.route("/", methods=["POST"])
def webhook():
    # Si el POST recibido es un JSON
    if request.headers.get("content-type") == "application/json":# Este request es de la libreria FLASK, no confundir con la libreria request
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "Ok", 200 # Estamos enviando el codigo de respuesta
        
# Responde al comando /start
@bot.message_handler(commands=["start"])
def cmd_start(message):
    # Saluda como buen bot educado XD 
    bot.send_message(message.chat.id, "Hola que hace", parse_mode="html")
    
# Gestiona los mensajes de texto recibidos
@bot.message_handler(content_types=["text"])
def bot_texto(message):
    # Responde con el mismo mensaje recibido
    bot.send_message(message.chat.id, message.text, parse_mode="html")
    
# MAIN
if __name__ == "__main__":
    print("INIICIANDO BOT")
    # bot.infinity_polling() # Lo eliminamos ya que no necesitamos
    conf.get_default().config_path = "./config_ngrok.yml"
    # Configuramos la region del servidor ngrok
    # REGIONES DISPONIBLES
    # Region Code	Location
    # us	United States (Ohio)
    # eu	Europe (Frankfurt)
    # ap	Asia/Pacific (Singapore)
    # au	Australia (Sydney)
    # sa	South America (São Paulo)
    # jp	Japan (Tokyo)
    # in	India (Mumbai)
    conf.get_default().region ="sa"
    # Creamos el archivo de credenciales de la Api de ngrok
    ngrok.set_auth_token(NGROK_TOKEN) # Esto nos descargaras las librerias tanto en linux, windows
    # Creamos un tunel https en el puerto 500 
    ngrok_tunel = ngrok.connect(5000, bind_tls=True) # bind_tls=True indicamos que sea https, si no indico se creara un tunel http   
    # url del tunel https creado
    ngrok_url = ngrok_tunel.public_url
    print("Url Ngrok", ngrok_url)
    # Eliminamos el webhook
    bot.remove_webhook()
    # Pequeña pausa para que se elimine el webhook
    time.sleep(1)
    # Definimos el webhook
    bot.set_webhook(url=ngrok_url)
    # Arrancamos el servidor
    # web_server.run(host="0.0.0.0", port=5000) # Inidcamos esta ip, porque el servidor local estara accesible a todas las ip de nuestra red local
    serve(web_server,host="0.0.0.0", port=5000)
    
    
    
    