import telebot
import time
import pyowm
import random
import tg_analytic


owm = pyowm.OWM('dbeee7264d80b183568973e21e1633fd', language = "ru")


#telegram bot
#bot = telebot.TeleBot("915096497:AAFvPSbMpvjdtNSucGNwSy6afA8UURu89nI")

#testbot

from telebot import apihelper
apihelper.proxy = {'https':'http://80.187.140.26:8080'}
bot = telebot.TeleBot("1225831912:AAG60sUGFoeRVePSufgLFM0Xaat176T2t1o")


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
 tg_analytic.statistics(message.chat.id, message.text)
 r = random.randint(0,2)
 if r == 0:
     bot.send_message(message.chat.id, 'Привет, просто напиши мне место, а я пришлю тебе погоду в нём 🤔')
 elif r == 1:
     bot.send_message(message.chat.id, 'Всё просто, с тебя город с меня погода, ничего больше...')
 elif r == 2:
     bot.send_message(message.chat.id, 'ку, пиши город, я напишу сколько там градусов, какая влажность и т.д.')

@bot.message_handler(content_types=['document', 'audio', 'sticker', 'photo']) 
def handle_docs_audio(message):
 tg_analytic.statistics(message.chat.id, message.text)
 r = random.randint(0,2)
 if r == 0:
     bot.send_message(message.chat.id, 'Я ждал название города, но это тоже интересно')
 elif r == 1:
     bot.send_message(message.chat.id, 'Ого, файлик, прикольно')
 elif r == 2:
     bot.send_message(message.chat.id, 'я конечно посмотрю это на досуге, но это не то чем я обычно занимаюсь 🤖')


@bot.message_handler(func=lambda message: True, content_types=['location'])
def echo_msg(message):
 f = open('location.txt', 'a')
 tg_analytic.statistics(message.chat.id, 'location')
 f.write(str(message.chat.id) + '  ' + str(message.location.latitude) + '  ' + str(message.location.longitude) + '\n')
 f.close()
 try:
   bot.send_message(message.chat.id, 'показана погода возле ближайшей метеостанции')
   observation = owm.weather_at_coords(int(message.location.latitude), int(message.location.longitude))
   w = observation.get_weather()
   l = observation.get_location()
   if w.get_detailed_status() == "ясно":
     answer = ("В городе "+ l.get_name() + " сейчас Ясно ☀️ \n")

   elif w.get_detailed_status() == "дождь":
     answer = ("В городе "+ l.get_name() + " сейчас дождь ⛈ \n")

   elif w.get_detailed_status() == "легкий дождь": 
     answer = ("В городе "+ l.get_name() + " сейчас лёгкий дождь 💦 \n")

   elif w.get_detailed_status() == "облачно с прояснениями": 
     answer = ("В городе "+ l.get_name() + " сейчас облачно с прояснениями 🌥️ \n")

   elif w.get_detailed_status() == "переменная облачность": 
     answer = ("В городе "+ l.get_name() + " сейчас переменная облачность 🌤️ \n")

   else: 
     answer = ("В городе "+ l.get_name() + " сейчас " + w.get_detailed_status() + "\n")

   answer += ("Температура: " + str(w.get_temperature('celsius')["temp"]) + "ºC \n")
   answer += ("Скорость ветра: " + str(w.get_wind()["speed"]))
   if int(str(w.get_wind()["speed"])[-1]) == 1:
    answer += (" метр в секунду \n")
   elif int(str(w.get_wind()["speed"])[-1]) == 2 or int(str(w.get_wind()["speed"])[-1]) == 3 or int(str(w.get_wind()["speed"])[-1]) == 4:
    answer += (" метра в секунду \n")
   else: 
    answer += (" метров в секунду \n")
   answer += ("Влажность: " + str(w.get_humidity()) + "% \n\n")
   bot.send_message(message.chat.id, answer)
 except:
 	echo_msg(message)
 	"""
     r = random.randint(0,2)
     if owm.is_API_online():
     	if r == 0:
      	 bot.send_message(message.chat.id, 'От тебя требовалось написать город \n ты даже тут не справился...')
     	elif r == 1:
      	 bot.send_message(message.chat.id, 'я с тобой тут шутки шучу что-ли? \n ПРОСТО   НАПИШИ   ГОРОД')
     	elif r == 2:
      	 bot.send_message(message.chat.id, 'Введен неправильный город, попытайся еще раз...')
     else: 
     	bot.send_message(message.chat.id, 'похоже сервера метеослужбы не отвечают \n попробуй позже')
    """


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
 tg_analytic.statistics(message.chat.id, message.text)
 if message.text[:11] == '8916sheshov':
        st = message.text.split(' ')
        if 'txt' in st or 'тхт' in st:
            tg_analytic.analysis(st,message.chat.id)
            with open('%s.txt' %message.chat.id ,'r',encoding='UTF-8') as file:
                bot.send_document(message.chat.id,file)
                tg_analytic.remove(message.chat.id)
        else:
         messages = tg_analytic.analysis(st,message.chat.id)
         bot.send_message(message.chat.id, messages)
 else:
  try:
   observation = owm.weather_at_place(message.text)
   w = observation.get_weather()
   if w.get_detailed_status() == "ясно":
	   answer = ("В городе "+ message.text + " сейчас Ясно ☀️ \n")

   elif w.get_detailed_status() == "дождь":
	   answer = ("В городе "+ message.text + " сейчас дождь ⛈ \n")

   elif w.get_detailed_status() == "легкий дождь": 
	   answer = ("В городе "+ message.text + " сейчас лёгкий дождь 💦 \n")

   elif w.get_detailed_status() == "облачно с прояснениями": 
	   answer = ("В городе "+ message.text + " сейчас облачно с прояснениями 🌥️ \n")

   elif w.get_detailed_status() == "переменная облачность": 
	   answer = ("В городе "+ message.text + " сейчас переменная облачность 🌤️ \n")

   else: 
 	   answer = ("В городе "+ message.text + " сейчас " + w.get_detailed_status() + "\n")

   answer += ("Температура: " + str(w.get_temperature('celsius')["temp"]) + "ºC \n")
   answer += ("Скорость ветра: " + str(w.get_wind()["speed"]))
   if int(str(w.get_wind()["speed"])[-1]) == 1:
    answer += (" метр в секунду \n")
   elif int(str(w.get_wind()["speed"])[-1]) == 2 or int(str(w.get_wind()["speed"])[-1]) == 3 or int(str(w.get_wind()["speed"])[-1]) == 4:
    answer += (" метра в секунду \n")
   else: 
    answer += (" метров в секунду \n")
   answer += ("Влажность: " + str(w.get_humidity()) + "% \n\n")
   bot.send_message(message.chat.id, answer)
  except:
  	echo_msg(message)
  	"""
     r = random.randint(0,2)
     if owm.is_API_online():
     	if r == 0:
      	 bot.send_message(message.chat.id, 'От тебя требовалось написать город \n ты даже тут не справился...')
     	elif r == 1:
      	 bot.send_message(message.chat.id, 'я с тобой тут шутки шучу что-ли? \n ПРОСТО   НАПИШИ   ГОРОД')
     	elif r == 2:
      	 bot.send_message(message.chat.id, 'Введен неправильный город, попытайся еще раз...')
     else: 
     	bot.send_message(message.chat.id, 'похоже сервера метеослужбы не отвечают \n попробуй позже')
    """
 


bot.polling(none_stop=True)