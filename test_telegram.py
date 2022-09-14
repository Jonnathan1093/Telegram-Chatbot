from config import * #Importamos el token
import telebot #para manejar la API de telegram
import time
import threading
# Instanciamos el bot de Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Para controlar que va hacer el bot, esta responde al comando /start

# Los decoradores inician con @ son funciones que reciben 
# como parámetros de entrada una función y devuelven otra función
@bot.message_handler(commands=["start", "ayuda", "help"])

# Acontinuacion debemos definir una funcion
def cmd_start(message):
    # Da la bienvenida al usuario del bot
    bot.reply_to(message, "Hola, aqui encontraras todo lo que te gusta")
    print(message.chat.id)

@bot.message_handler(content_types=["text"])
# @bot.message_handler(content_types=["text", "photo"]) # Se ejecutata si recibe texto o imagem
# Responde a los mensajes de texto que no son comandos o se puede usar los de abajo dependiendo
# text, audio, document, photo, sticker, video, video_note, 
# voice, location, contact, new_chat_members, left_chat_member, 
# new_chat_title, new_chat_photo, delete_chat_photo, group_chat_created, 
# supergroup_chat_created, channel_chat_created, migrate_to_chat_id, 
# migrate_from_chat_id, pinned_message

def bot_mensajes_texto(message):
    # Gestiona los mensajes de texto recibidos
# # FORMATOS HTML 
#     texto_html = '<b><u>Formatos Html</u>:</b>' + '\n' # Manera de anidar etiquetas
#     texto_html+= '<b>NEGRITA</b>' + '\n' # Negrita en html
#     texto_html+= '<i>CURSIVA</i>' + '\n' # Cursiva en html
#     texto_html+= '<u>SUBRAYADO</u>'+ '\n' # Subrayado en html
#     texto_html+= '<s>TACHADO</s>' + '\n' # Tachado en html
#     texto_html+= '<code>MONOESPACIADO</code>' + '\n' # Monoespaciado en html
#     texto_html+= '<span class="tg-spoiler">SPOILER</span>' + '\n' #S poiler en html 
#     texto_html+= '<a href="https://retrogeeksla.blogspot.com/">ENLACE</a>' + "\n" # Enlace en html
# #FORMATOS MARKDOWNV2 
#     texto_markdown ='*__Formatos Markdown__:*' + '\n' # Manera de anidar etiquetas
#     texto_markdown+= '*NEGRITA*' + '\n' # Negrita 
#     texto_markdown+= '_CURSIVA_' + '\n' # Cursiva 
#     texto_markdown+= '__SUBRAYADO__'+ '\n' # Subrayado 
#     texto_markdown+= '~TACHADO~' + '\n' #T achado 
#     texto_markdown+= '```MONOESPACIADO```' + '\n' # Monoespaciado 
#     texto_markdown+= '||SPOILER||' + '\n' # Spoiler 
#     texto_markdown+= '[ENLACE](https://retrogeeksla.blogspot.com/)' + '\n' # Enlace

# Gestionar los mensajes de texto recibidos    
    if message.text and message.text.startswith("/"): #Controlo el texto para que no inicien con barra
        bot.send_message(message.chat.id, "Comando no disponible") #Controla el texto si por ejemplo ponen: /hola 
    else:
        # x = bot.send_message(message.chat.id, "<b>Hola</b>", parse_mode="html", disable_web_page_preview=True)
        # time.sleep(3) # Pausa
        # bot.edit_message_text("<u>Adios</u>", message.chat.id, x.message_id, parse_mode="html") # Para editar el mensaje, como primer argumento recibe el mensaje, y segundo el identificador
        # bot.delete_message(message.chat.id, x.message_id) # Eliminar mensaje bot
        # bot.delete_message(message.chat.id, message.message_id)
        # bot.send_message(message.chat.id, texto_html, parse_mode="html", disable_web_page_preview=True) 
        # bot.send_message(message.chat.id, texto_markdown, parse_mode="MarkdownV2", disable_web_page_preview=True)  # Podemos ver en formato Markdown    
        # De esta manera obtenemos el chat id del usuario que nos envio el mensaje parse_mode me permite enviar en formato html
        # Para controlar la previsualizacion de nuestro enlace usamos disable_web_page_preview, el valor sera true, porque por defecto es false
        
        # # Primer argumento chat id, segundo el objeto que contiene la foto, el tercero es opcional, es un "Caption" puede ir un mensaje
        # foto = open("./Imagenes/Marca de Maldicion.jpg", "rb")
        # bot.send_photo(message.chat.id, foto, "Marca") 
        
        # # Para enviar un archivo
        # archivo = open("./Docs/Problemas de geometria analitica plana.pdf", "rb")
        # bot.send_document(message.chat.id, archivo, caption="Libro Geometria")
        
        # Para mostrar en la barra superior escribiendo
        bot.send_chat_action(message.chat.id, "upload_video")
        # action_string can be one of the following strings: 'typing', 'upload_photo', 'record_video', 'upload_video',
        # 'record_audio', 'upload_audio', 'upload_document' or 'find_location'
        
        # Para enviar un video
        video = open("./Video/Otoko Intro.mp4", "rb")
        bot.send_video(message.chat.id, video, caption="Mira mi intro")
      
def recibir_mensajes():
    bot.infinity_polling()
    
# Comenzamos a escribir nuestro programa principal
if __name__== '__main__': # Para indicar que se inicia el bot
    # Este recibira los argumentos, el primero sera el comando, y el segundo la descripcion del mmismo
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Inicia el bot"), 
        telebot.types.BotCommand("/boom", "Explota el mundo")
        ])
    print('Iniciando el bot') 
    hilo_bot = threading.Thread(name="hilo_bot", target=recibir_mensajes)
    hilo_bot.start() # Con esto iniciamos
    # bot.infinity_polling() # Este metodo se trata de un bucle infinito, comprueba constantemente si se reciben mensajes nuevos
    print('Bot iniciado')
    # bot.send_message(MI_CHAT_ID, "Python mola mucho") # Mandamos al mismo bot
    bot.send_message(CANAL_ID, "Python mola mucho") # Mandamos al canal
    









