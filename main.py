from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter
import logging, asyncio, time, pyowm, random, aiohttp, schedule
import emoji

logging.basicConfig(level=logging.INFO)
owm = pyowm.OWM('dbeee7264d80b183568973e21e1633fd', language = "ru")


#telegram bot

token='915096497:AAFvPSbMpvjdtNSucGNwSy6afA8UURu89nI'




#testbot

#token = '1225831912:AAG60sUGFoeRVePSufgLFM0Xaat176T2t1o'



bot = Bot(token)

dp = Dispatcher(bot)
db = SQLighter('db.db')


@dp.message_handler(commands=['start', 'help'])
async def handle_start_help(message: types.Message):
	r = random.randint(0,2)
	if r == 0:
		await message.answer('Привет, просто напиши мне место, а я пришлю тебе погоду в нём 🤔')
	elif r == 1:
		await message.answer('Всё просто, с тебя город с меня погода, ничего больше...')
	elif r == 2:
		await message.answer('Ку, пиши город, я напишу сколько там градусов, какая влажность и т.д.')
	await message.answer('Также можно подписаться на ежедневный прогноз погоды в городе:\n/subscribe "город"')
	await message.answer('А ещё можно узнать прогноз командой /forecast "город"')
	if db.subscriber_exists(message.from_user.id) == 'da':
		pass
	else:
		# если юзера нет в базе, добавляем его
		db.add_subscriber(message.from_user.id)
		await bot.send_message(214196761, '{0} added'.format(message.from_user.id))



@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
	city = message.text[11:]
	if db.subscriber_exists(message.from_user.id) == 'da':
		if db.subscription_status(message.from_user.id):
			city = str(db.subscription_city(message.from_user.id))
			city = city[3:-4]
			await message.answer("Вы уже подписаны на город: {0}!\nуведомления приходят в 10 утра(МСК)\nпозже будет доступен выбор времени\nдля отписки напиши /unsubscribe".format(city))
		else:
			if city == "":
				city = 'москва'
				db.update_subscription(message.from_user.id, True, city)
				await message.answer('Вы подписались на обновления, но не написали город\nпо умолчанию выставлена москва\nдля выбора другого города -\n1. /unsubscribe\n2. /subscribe "город"')
			else:
				db.update_subscription(message.from_user.id, True, city)
				await message.answer("Вы успешно подписались на обновления погоды в городе: {0}\nпогода приходит в 10 утра(МСК)\nпозже будет доступен выбор времени\nдля отписки напиши /unsubscribe".format(city))
	else:
		if city == "":
			city = 'москва'
			db.add_subscriber(message.from_user.id, True)
			db.update_subscription(message.from_user.id, True, city)
			await bot.send_message(214196761, '{0} added'.format(message.from_user.id))
			await message.answer('Вы подписались на обновления, но не написали город\nпо умолчанию выставлена москва\nдля выбора другого города -\n1. /unsubscribe\n2. /subscribe "город"')
		else:
			# если юзера нет в базе, добавляем его
			db.add_subscriber(message.from_user.id, True)
			db.update_subscription(message.from_user.id, True, city)
			await bot.send_message(214196761, '{0} added'.format(message.from_user.id))
			await message.answer("Вы успешно подписались на обновления погоды в городе: {0}\nпогода приходит в 10 утра(МСК)\nпозже будет доступен выбор времени\nдля отписки напиши /unsubscribe".format(city))


			

@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
	if db.subscriber_exists(message.from_user.id) == 'da':
		if (db.subscription_status(message.from_user.id)):
			db.update_subscription(message.from_user.id, False)
			await message.answer('Вы успешно отписались от рассылки.\nдля подписки - /subscribe "город"')
		else:
			await message.answer('Вы и так ни на что не подписаны\nдля подписки - /subscribe "город"')
	else:
		# если юзера нет в базе, добавляем его с неактивной подпиской
		db.add_subscriber(message.from_user.id, False)
		await bot.send_message(214196761, '{0} added'.format(message.from_user.id))
		await message.answer('Вы и так ни на что не подписаны\nдля подписки - /subscribe "город"')



@dp.message_handler(commands=['forecast'])
async def unsubscribe(message: types.Message):
	city = str(message.text[10:])
	if city == '':
		await message.answer('Используйте: /forecast "город"')
		if db.subscriber_exists(message.from_user.id) == 'da':
			pass
		else:
			db.add_subscriber(message.from_user.id, False)
			await bot.send_message(214196761, '{0} added'.format(message.from_user.id))
	else:
		observation = owm.weather_at_place(city)
		w = observation.get_weather()
		fc1 = owm.three_hours_forecast(city)
		f = fc1.get_forecast()
		reception_date = str(f)
		reception_date = reception_date[55:65]
		answer = ""
		for w in f:
			time = str(w.get_reference_time('iso'))
			date = time[:10] 
			if date == reception_date:
				time = str(time[11:16])
				temp = str(w.get_temperature('celsius')["temp"])
				detailed_status = w.get_detailed_status()
				not_detailed = w.get_status()
				answer1 = "{0}:\n{1}{3} {2}ºC\n\n".format(time,detailed_status,temp,emoji.get_emoji(not_detailed))
				answer = answer + answer1
		await message.answer('прогноз для города: ' +city + '\n\n' + answer)
		if db.subscriber_exists(message.from_user.id) == 'da':
			pass
		else:
			# если юзера нет в базе, добавляем его с неактивной подпиской
			db.add_subscriber(message.from_user.id, False)
			await bot.send_message(214196761, '{0} added'.format(message.from_user.id))
			



@dp.message_handler(content_types=['document', 'audio', 'sticker', 'photo', 'entities', 'animation', 'video', 'video_note', 'voice', 'contact', 'game', 'poll']) 
async def handle_docs_audio(message: types.Message):
	r = random.randint(0,2)
	if r == 0:
	    await message.answer('Я ждал название города, но это тоже интересно')
	elif r == 1:
	    await message.answer('Ого, файлик, прикольно')
	elif r == 2:
	    await message.answer('я конечно посмотрю это на досуге, но это не то чем я обычно занимаюсь 🤖')
	if db.subscriber_exists(message.from_user.id) == 'da':
		pass
	else:
		# если юзера нет в базе, добавляем его
		db.add_subscriber(message.from_user.id)
		await bot.send_message(214196761, '{0} added'.format(message.from_user.id))
		
 


@dp.message_handler(content_types=['location'])
async def by_location(message: types.Message):
	f = open('location.txt', 'a')
	f.write(str(message.from_user.id) + '  ' + str(message.location.latitude) + '  ' + str(message.location.longitude) + '\n')
	f.close()
	try:
		await message.answer('показана погода возле ближайшей метеостанции')
		observation = owm.weather_at_coords(int(message.location.latitude), int(message.location.longitude))
		w = observation.get_weather()
		l = observation.get_location()
		detailed_status = w.get_detailed_status()
		not_detailed = w.get_status()
		answer = ("В городе "+ l.get_name() + " сейчас Ясно"+  str(emoji.get_emoji(not_detailed)) +"\n")
		answer += ("Температура: " + str(w.get_temperature('celsius')["temp"]) + "ºC \n")
		answer += ("Скорость ветра: " + str(w.get_wind()["speed"]) + "м/с\n")
		answer += ("Влажность: " + str(w.get_humidity()) + "% \n\n")
		await message.answer(answer)
	except:
		await message.answer('похоже произошла внутренняя ошибка \n попробуй ещё раз')
	if db.subscriber_exists(message.from_user.id) == 'da':
		pass
	else:
		# если юзера нет в базе, добавляем его
		db.add_subscriber(message.from_user.id)
		await bot.send_message(214196761, '{0} added'.format(message.from_user.id))
		



@dp.message_handler( content_types=['text'])
async def by_massage(message: types.Message):
	if ((message.text[0:4].capitalize() == 'Push') and (message.from_user.id == 214196761)):
		push_text = str(message.text[5:])
		await message.answer('Рассылка активирована')
		name = 0
		try:
			while name < (db.all_users()[-1][0]-4):
				await bot.send_message(db.all_users()[name][1], push_text)
				name +=1
		except:
			await bot.send_message(214196761, "ошибка рассылки для " + str(db.all_users()[name][1]))
	else:
		try:
			observation = owm.weather_at_place(message.text)
			w = observation.get_weather()
			detailed_status = w.get_detailed_status()
			not_detailed = w.get_status()
			answer = ("В городе "+ message.text + " сейчас Ясно"+  str(emoji.get_emoji(not_detailed)) +"\n")
			answer += ("Температура: " + str(w.get_temperature('celsius')["temp"]) + "ºC \n")
			answer += ("Скорость ветра: " + str(w.get_wind()["speed"]) + "м/с\n")
			answer += ("Влажность: " + str(w.get_humidity()) + "% \n\n")
			await message.answer(answer)
		except:
			await bot.send_message(message.chat.id, 'похоже произошла внутренняя ошибка \nпопробуй ещё раз')
		if db.subscriber_exists(message.from_user.id) == 'da':
			pass
		else:
			# если юзера нет в базе, добавляем его
			db.add_subscriber(message.from_user.id)
			await bot.send_message(214196761, '{0} added'.format(message.from_user.id))
			

	


async def time_check():
	while True:
		schedule.run_pending()
		await asyncio.sleep(1)


async def mailing():
	loop  =  asyncio.get_event_loop()
	subscriptions = db.get_subscriptions()
	for s in subscriptions:
		city = str(db.subscription_city(s[1])[0])
		city = city[2:-3]
		observation = owm.weather_at_place(city)
		w = observation.get_weather()
		fc1 = owm.three_hours_forecast(city)
		f = fc1.get_forecast()
		reception_date = str(f)
		reception_date = reception_date[55:65]
		answer = ""
		for w in f:
			time = str(w.get_reference_time('iso'))
			date = time[:10] 
			if date == reception_date:
				time = str(time[11:16])
				temp = str(w.get_temperature('celsius')["temp"])
				detailed_status = w.get_detailed_status()
				not_detailed = w.get_status()
				answer1 = "{0}:\n{1}{3} {2}ºC\n\n".format(time,detailed_status,temp,emoji.get_emoji(not_detailed))
				answer = answer + answer1
		await bot.send_message(s[1],"⏰Время погоды🔔:")
		await bot.send_message(s[1],"Прогноз города {0}:\n{1}".format(city,answer))
		
		

def mailing123():
	asyncio.run_coroutine_threadsafe(mailing(), bot.loop)



schedule.every().day.at("07:00").do(mailing123) #время по гринвичу

#mailing123()






if __name__ == '__main__':
	dp.loop.create_task(time_check())
	executor.start_polling(dp, skip_updates=True)
