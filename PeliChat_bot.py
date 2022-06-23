#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import requests
import json

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sheets import gsheet_helper


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Para el uso de la API de YouTube.
DEVELOPER_KEY = 'AIzaSyASOQ_vHoevyZMxyYWrxNkgOFA37WGLlik'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

#Emoji
warning = u'\U000026A0'

gsconn = gsheet_helper()

#Contadores de uso
contUsoAcc = 1
contUsoAve = 1
contUsoAni = 1
contUsoCom = 1
contUsoCri = 1
contUsoDoc = 1
contUsoDra = 1
contUsoFam = 1
contUsoFan = 1
contUsoHis = 1
contUsoHor = 1
contUsoMus = 1
contUsoMys = 1
contUsoRom = 1
contUsoCie = 1
contUsoTvm = 1
contUsoThr = 1
contUsoGue = 1
contUsoWes = 1

#Busqueda en YOUTUBE

def busquedaYT(a,b):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    # Llama al método search.list para recuperar resultados que coincidan con el especificado
    # término de consulta.
    search_response = youtube.search().list(
        q=a,
        part='id,snippet',
        maxResults=b
    ).execute()


    # Retorna el link completo del video encontrado, esperando que sea un video y no otra cosa (Lista de reproducción o Canal).
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            return "https://www.youtube.com/watch?v="+str(search_result['id']['videoId'])
     
#Función para buscar las recomendaciones de peliculas, también es el que muestra da descripción de cada título con sus propiedades.  
def buscar(update,codigoGen, contaP):
    url = "https://api.themoviedb.org/3/discover/movie?api_key=b5568e06436c62049f7b6352d97a593f&language=es&sort_by=popularity.desc&include_adult=false&page="+str(contaP)+"&with_genres="+ str(codigoGen)
    payload = {}
    headers= {}
    
    response = requests.request("GET", url, headers=headers, data = payload)

    if response.status_code == 200:
        response_json = json.loads(response.text)
        #print(response_json['results'][0])
        for cont in range(0, 3):
            #print(response_json['results'][cont]['title'])
            update.message.reply_text("Titulo: " + response_json['results'][cont]['title'] + "\nDescripción: " + response_json['results'][cont]['overview'] + "\nAño de lanzamiento: "+ str(response_json['results'][cont]['release_date']) +"\nPopularidad: " +str(response_json['results'][cont]['popularity']) + "\nPromedio de votos: " + str(response_json['results'][cont]['vote_average']) + "\nPoster: https://image.tmdb.org/t/p/w185_and_h278_bestv2" + response_json['results'][cont]['poster_path'] + "\nTrailer: " + busquedaYT(response_json['results'][cont]['title']+" Trailer",1) )
        
        update.message.reply_text("¿Desea otras recomendaciones? Toque /start para volver a ver la lista de géneros\nO Escriba /buscar seguido del nombre de la película a buscar")
    else:
        update.message.reply_text("No se pudo establecer conexión con el servidor")

def buscarPeli(update,nombrePeli):
    url = "https://api.themoviedb.org/3/search/movie?api_key=b5568e06436c62049f7b6352d97a593f&language=es&page=1&include_adult=false&query="+str(nombrePeli)
    payload = {}
    headers= {}
    
    response = requests.request("GET", url, headers=headers, data = payload)

    if response.status_code == 200:
        response_json = json.loads(response.text)
        for cont in range(0, 5):
            update.message.reply_text("Titulo: " + response_json['results'][cont]['title'] + "\nDescripción: " + response_json['results'][cont]['overview'] + "\nAño de lanzamiento: "+ str(response_json['results'][cont]['release_date']) +"\nPopularidad: " +str(response_json['results'][cont]['popularity']) + "\nPromedio de votos: " + str(response_json['results'][cont]['vote_average']) + "\nPoster: https://image.tmdb.org/t/p/w185_and_h278_bestv2" + response_json['results'][cont]['poster_path'] + "\nTrailer: " + busquedaYT(response_json['results'][cont]['title']+" Trailer",1) )
        
        update.message.reply_text("¿Desea otra búsqueda? Escriba /buscar seguido del nombre de la película a buscar\nO toque /start para ver la lista de géneros :)")
    else:
        update.message.reply_text("No se pudo establecer conexión con el servidor")


# Manejador cuando una persona no escribe un comando
def echo(update, context):
    """Echo the user message."""
    update.message.reply_text("Por favor, seleccione un comando de la lista desplegada por /start o /info "+warning)

# Manejadores de comandos del ChatBot.
def start(update, context):
    users_dic = {
        'id': update.message.from_user.id,
        'primer_nombre': update.message.from_user.first_name,
        'segundo_nombre': update.message.from_user.last_name,
        'username': update.message.from_user.username,
    }
    
    inicio = f"""¡Hola {users_dic["primer_nombre"]} ! Bienvenido a PeliChat, aquí encontrarás recomendaciones de películas de acuerdo al género, además, ¡ahora podrás realizar búsquedas de películas por su nombre!.\nElige entre los siguientes géneros.\n/Accion\n/Aventura\n/Animacion\n/Comedia\n/Crimen\n/Documental\n/Drama\n/Familiar\n/Fantasia\n/Hisrotia\n/Horror\n/Musica\n/Misterio\n/Romance\n/CienciaFiccion\n/TVmovie\n/Thriller\n/Guerra\n/Western\nO puedes escribir /buscar seguido del nombre de la película"""
    update.message.reply_text(inicio)
   
    gsconn.store_user(users_dic)

    

def info(update, context):
    informacion = "Gracias por utilizar este chat.\nLos géneros son los siguientes:\n/Accion\n/Aventura\n/Animacion\n/Comedia\n/Crimen\n/Documental\n/Drama\n/Familiar\n/Fantasia\n/Historia\n/Horror\n/Musica\n/Misterio\n/Romance\n/CienciaFiccion\n/TVmovie\n/Thriller\n/Guerra\n/Western\n\nO puedes escribir /buscar seguido del nombre de la película\nDesarrollado por: Erick Oswaldo Gallegos Pérez\nCorreo: erozgp@gmail.com\nInstagram: @gallegos.lml\nUNISTMO Campus Tehunatepec."
    update.message.reply_text(informacion)

def accion(update, context):
    global contUsoAcc
    update.message.reply_text("Buscando para Acción...")
    buscar(update,28,contUsoAcc)
    contUsoAcc+=1

def aventura(update, context):
    global contUsoAve
    update.message.reply_text("Buscando para Aventura...")
    buscar(update,12,contUsoAve)
    contUsoAve+=1
    
def animacion(update, context):
    global contUsoAni 
    update.message.reply_text("Buscando para Animación...")
    buscar(update,16,contUsoAni)
    contUsoAni+=1

def comedia(update, context):
    global contUsoCom
    update.message.reply_text("Buscando para Comedia...")
    buscar(update,35,contUsoCom)
    contUsoCom+=1

def crimen(update, context):
    global contUsoCri
    update.message.reply_text("Buscando para Crimen...")
    buscar(update,80,contUsoCri)
    contUsoCri+=1

def documental(update, context):
    global contUsoDoc
    update.message.reply_text("Buscando para Documental...")
    buscar(update,99,contUsoDoc)
    contUsoDoc+=1

def drama(update, context):
    global contUsoDra
    update.message.reply_text("Buscando para Drama...")
    buscar(update,18,contUsoDra)
    contUsoDra+=1

def familiar(update, context):
    global contUsoFam
    update.message.reply_text("Buscando para Familiar...")
    buscar(update,10751,contUsoFam)
    contUsoFam+=1

def fantasia(update, context):
    global contUsoFan 
    update.message.reply_text("Buscando para Fantasía...")
    buscar(update,14,contUsoFan)
    contUsoFan+=1

def historia(update, context):
    global contUsoHis
    update.message.reply_text("Buscando para Historia...")
    buscar(update,36,contUsoHis)
    contUsoHis+=1

def horror(update, context):
    global contUsoHor
    update.message.reply_text("Buscando para Horror...")
    buscar(update,27,contUsoHor)
    contUsoHor+=1

def musica(update, context):
    global contUsoMus
    update.message.reply_text("Buscando para Música...")
    buscar(update,10402,contUsoMus)
    contUsoMus+=1

def misterio(update, context):
    global contUsoMys
    update.message.reply_text("Buscando para Misterio...")
    buscar(update,9648,contUsoMys)
    contUsoMys+=1

def romance(update, context):
    global contUsoRom
    update.message.reply_text("Buscando para Romance...")
    buscar(update,10749,contUsoRom)
    contUsoRom+=1

def sifi(update, context):
    global contUsoCie
    update.message.reply_text("Buscando para Ciencia Ficción...")
    buscar(update,878,contUsoCie)
    contUsoCie+=1

def tvmovie(update, context):
    global contUsoTvm
    update.message.reply_text("Buscando para TV Movie...")
    buscar(update,10770,contUsoTvm)
    contUsoTvm+=1

def thr(update, context):
    global contUsoThr
    update.message.reply_text("Buscando para Thriller...")
    buscar(update,53,contUsoThr)
    contUsoThr+=1

def guerra(update, context):
    global contUsoGue
    update.message.reply_text("Buscando para Guerra...")
    buscar(update,10752,contUsoGue)
    contUsoGue+=1

def western(update, context):
    global contUsoWes
    update.message.reply_text("Buscando para Western...")
    buscar(update,37,contUsoWes)
    contUsoWes+=1

def busquedaArgs(update, context):
    args = context.args
    textoB = ""
    if len(args) > 0:
        for conta in range(0,len(args)):
            text1 = str(args[conta]) + " "
            textoB+=text1
        user_search = {
            'id': update.message.from_user.id,
            'primer_nombre': update.message.from_user.first_name,
            'busqueda': textoB,
        }
        buscarPeli(update,textoB)
        gsconn.store_search(user_search)
    else:
        update.message.reply_text("Por favor, escribe algo después de /buscar")
    
    
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1176655079:AAGpIG9kztXyzQtaD3q9-8FXJ445kQx83u4", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("Accion", accion))
    dp.add_handler(CommandHandler("Aventura", aventura))
    dp.add_handler(CommandHandler("Animacion", animacion))
    dp.add_handler(CommandHandler("Comedia", comedia))
    dp.add_handler(CommandHandler("Crimen", crimen))
    dp.add_handler(CommandHandler("Documental", documental))
    dp.add_handler(CommandHandler("Drama", drama))
    dp.add_handler(CommandHandler("Familiar", familiar))
    dp.add_handler(CommandHandler("Fantasia", fantasia))
    dp.add_handler(CommandHandler("Historia", historia))
    dp.add_handler(CommandHandler("Horror", horror))
    dp.add_handler(CommandHandler("Musica", musica))
    dp.add_handler(CommandHandler("Misterio", misterio))
    dp.add_handler(CommandHandler("Romance", romance))
    dp.add_handler(CommandHandler("CienciaFiccion", sifi))
    dp.add_handler(CommandHandler("TVmovie", tvmovie))
    dp.add_handler(CommandHandler("Thriller", thr))
    dp.add_handler(CommandHandler("Guerra", guerra))
    dp.add_handler(CommandHandler("Western", western))
    dp.add_handler(CommandHandler("buscar", busquedaArgs))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()