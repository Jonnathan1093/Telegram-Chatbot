from config import *
import telebot # Para manejar la API de telegram
from telebot.types import ReplyKeyboardMarkup # Para crear botonoes
from telebot.types import ReplyKeyboardRemove # Para eliminar los botones
from random import randint # Para generar numeros enteros aleatoreos

# Instanciamos el bot de telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)
# Variable global en la que guardaremos los datos del usuario
usuarios ={} 

# Responde a los comandos /start, /help, /ayuda
@bot.message_handler(commands=["start", "help", "ayuda"])

def cmd_start(message):
    # Muestra el modo de uso del bot
    botones = ReplyKeyboardRemove() # Para eliminar los posibles botones
    # Muestra los comandos disponibles
    bot.send_message(message.chat.id, "Usa el comando /jugar para empezar", reply_markup = botones)

# Responde al comando /jugar
@bot.message_handler(commands=["jugar"])
def cmd_jugar(message):
    # Inicia el juego
    numero = randint(1, 10)
    cid = message.chat.id
    usuarios[cid] = numero
    botones = ReplyKeyboardMarkup(input_field_placeholder="Pulsa un boton")
    botones.add("1","2","3","4","5","6","7","8","9","10")
    msg = bot.send_message(message.chat.id, "Adivina el numero entre 1 y 10", reply_markup = botones)
    # Registramos la respuesta en la funcion indicada 
    bot.register_next_step_handler(msg, comprobar_numero) # Asignamos la variable y funcion

def comprobar_numero(message):
    # Comprueba si el numero es correcto
    cid = message.chat.id
    if not message.text.isdigit():
        msg = bot.send_message(message.chat.id, "Error: Introduce un numero")
        bot.register_next_step_handler(msg, comprobar_numero)
    else:
        n = int(message.text)
        if n < 1 or n > 10:
            msg = bot.send_message(message.chat.id, "Error: Numero fuera de rango")
            bot.register_next_step_handler(msg, comprobar_numero)
        else:
            if n == usuarios[cid]:
                markup = ReplyKeyboardRemove()
                bot.reply_to(message, "Genial, acertaste el numero")
                return
            elif n > usuarios[cid]:
                msg = bot.reply_to(message, "Pista: Menor")
                bot.register_next_step_handler(msg, comprobar_numero)
            else:
                msg = bot.reply_to(message, "Pista: Mas")
                bot.register_next_step_handler(msg, comprobar_numero)
                
if __name__ == "__main__":
    print("INIICIANDO BOT")
    bot.infinity_polling()
    