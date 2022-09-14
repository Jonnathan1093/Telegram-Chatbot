from email import message
from config import *
import telebot # Para manejar la API de telegram
from telebot.types import ReplyKeyboardMarkup # Para crear botonoes
from telebot.types import ForceReply # Para citar un mensaje


# Instanciamos el bot de telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)
# Variable global en la que guardaremos los datos del usuario
usuarios ={} 

# Responde a los comandos /start, /help, /ayuda
@bot.message_handler(commands=["start", "help", "ayuda"])

def cmd_start(message):
    # Muestra los comandos disponibles
    bot.send_message(message.chat.id, "Usa el comando /alta para introducir tus datos")

# Responde al comando /alta
@bot.message_handler(commands=["alta"])
def cmd_alta(message):
    markup = ForceReply() #
    # Pregunta el nombre del usuario
    msg = bot.send_message(message.chat.id, "¿Como te llamas?", reply_markup=markup)
    bot.register_next_step_handler(msg,preguntar_edad) # Asignamos la variable y funcion
    
def preguntar_edad(message):
    # Pregunta la edad del usuario
    usuarios[message.chat.id] = {} # De esta manera tendremos un diccionario, dentro de un diccionario pero propio del usuario que usa el comando /alta
    usuarios[message.chat.id]["nombre"] = message.text 
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "¿Cuantos años tienes?", reply_markup = markup)
    bot.register_next_step_handler(msg, preguntar_sexo)
    
def  preguntar_sexo(message):
    # Pregunta el sexo del usuario
    # Si la edad introducida no es un numero 
    if not message.text.isdigit():
        # Informamos del error y volvemos a preguntar
        markup = ForceReply()    
        msg = bot.send_message(message.chat.id, "Error: Debes indicar un numero.\n ¿Cuantos años tienes?", )
        # Volvemos a ejecutar esta funcion
        bot.register_next_step_handler(msg, preguntar_sexo)
    else: # Si se introdujo la edad correctamente
        usuarios[message.chat.id]["edad"] = int(message.text) 
        # Aqui habra 2 botones
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Pulsa un boton",
            resize_keyboard=True
            )
        # Añadimos los  botones
        markup.add("Hombre", "Mujer")
        # Preguntamos por el sexo
        msg = bot.send_message(message.chat.id, "¿Cual es tu sexo?", reply_markup=markup) 
        # Registramos la respuesta en la funcion indicada
        bot.register_next_step_handler(msg, guardar_datos_usuario)
        
def guardar_datos_usuario(message):
    # Guardamos los datos introducidos por el usuario
    # Si el sexo introducido no es valido
    if message.text != "Hombre" and message.text != "Mujer":
        # Informamos del error y volvemos a preguntar
        msg = bot.send_message(message.chat.id, "Error: Sexo no valido\n Pulsa un boton") 
        # Volvemos a ejecutar esta funcion
        bot.register_next_step_handler(msg, guardar_datos_usuario)
    else: # Si el sexo introducido es valido
        usuarios[message.chat.id]["sexo"] = message.text
        texto = "Datos introducidos: \n"
        texto+= f"<code>NOMBRE: </code>{usuarios[message.chat.id]['nombre']}\n"
        texto+= f"<code>EDAD: </code>{usuarios[message.chat.id]['edad']}\n"
        texto+= f"<code>GENERO: </code>{usuarios[message.chat.id]['sexo']}\n"
        bot.send_message(message.chat.id, texto, parse_mode="html")
        print(usuarios)        
        
        
        
# """--- CUERPO DEL BOT ---"""
if __name__ == "__main__":
    print("INIICIANDO BOT")
    bot.infinity_polling()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    