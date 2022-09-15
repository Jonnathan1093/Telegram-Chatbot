from config import *
import telebot # Para manejar la API de telegram
# Botones Inline
from telebot.types import InlineKeyboardMarkup # Para crear botonoes inline
from telebot.types import InlineKeyboardButton # Para definir los botones inline

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
    b_cerrar = InlineKeyboardButton("Cerrar", callback_data="Cerrar")
    markup.add(b1, b2, b3, b4, b5, b6, b7, b8, b9, b_cerrar)
    bot.send_message(message.chat.id, "Mis paginas de anime", reply_markup = markup)

@bot.callback_query_handler(func = lambda x: True) # Hacemos de funciones lambda, son funciones anonimas es decir que no hemos definido previamente
def respuesta_botonesInline(call):
    # Gestiona las acciones de los botones callback_data
    cid = call.from_user.id
    mid = call.message.id
    if call.data == "cerrar":
        bot.delete_message(cid, mid)
        
    
    
# Programa principal
if __name__ == "__main__":
    print("INIICIANDO BOT")
    bot.infinity_polling()
    