import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia
import pyaudio

#opciones de voz / icioma
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

'''#Saber que voces tiene tu sistema operativo
engine = pyttsx3.init()
for voz in engine.getProperty('voices'):
    print(voz)'''

# escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_en_texto():

    #Almacenar el recognizer en variable
    r = sr.Recognizer()

    #Configurar el microfono
    with sr.Microphone() as origen:

        #tiempo de espera
        r.pause_threshold = 0.5

        # informar que comenzo la grabación
        print("Ya puedes hablar")

        #Guardar lo que escucho como audio en una variable
        audio = r.listen(origen)

        try:
            #buscar en google
            pedido = r.recognize_google(audio, language="es")

            #prueba de que pudo ingresar
            print("Dijiste: "+ pedido)

            #devolver pedido
            return pedido

        # En caso de que no comprenda el audio
        except sr.UnknownValueError:

            #Prueba de que no comprendio el audio
            print("Ups, no entendí")

            # Devolver error
            return "Sigo esperando"

        #En caso de no resolver el pedido
        except sr.RequestError:

            # Prueba de que no comprendio el audio
            print("Ups, no hay servicio")

            # Devolver error
            return "Sigo esperando"

        #error inesperado
        except:

            # Prueba de que no comprendio el audio
            print("Ups, algo ha salido mal")

            # Devolver error
            return "Sigo esperando"

#Funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    #encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

#informar el día de la semana
def pedir_dia():

    #crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    #crear variable para el día de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    #diccionario con nombres de días
    calendario = {0:'Lunes',
                  1:'Martes',
                  2:'Miércoles',
                  3:'Jueves',
                  4:'Viernes',
                  5:'Sábado',
                  6:'Domingo'}

    #decir el día de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')

#informar que hora es
def pedir_hora():

    #crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)

    #decir la hora
    hablar(hora)

#Funcion saludo inicial
def saludo_inicial():

    #crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'

    #decir el saludo
    hablar(f'{momento}, soy Helena, tú asistente personal virtual. ¿En que te puedo ayudar?')

#Funcion central del asistente

def pedir_cosas():

    #activar el saludo inicial
    saludo_inicial()

    #variable de corte
    comenzar = True

    #loop central
    while comenzar:

        #activar el micro y guardar el pedido en el string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo YouTube')
            webbrowser.open('https://www.youtube.com/')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro, estoy en ello')
            webbrowser.open('https://www.google.com/')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando eso en Wikipedia')
            pedido = pedido.replace('wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente: ')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Ya estoy en ello')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Buena indea, ya comienzo a reproducirlo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                       'amazon':'AMZN',
                       'google':'GOOGL'}
            try:
                accion_buscar = cartera[accion]
                accion_buscar = yf.Ticker(accion_buscar)
                precio_actual = accion_buscar.info['regularMarketPrice']
                hablar(f'La encontre, el precio de {accion} es: {precio_actual}')
                continue
            except:
                hablar("Perdón, pero no la he encontrado")
                continue
        elif 'adiós' in pedido:
            hablar("Me voy a descansar, cualquier cosa me avisas.")
            break

pedir_cosas()




