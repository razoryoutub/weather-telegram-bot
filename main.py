from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter
import logging, asyncio, time, pyowm, random, aiohttp, schedule
import emoji
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons.enums import SubscriptionTypeEnum

config_dict = get_default_config()
config_dict['language'] = 'ru'  # your language here


logging.basicConfig(level=logging.INFO)
owm = pyowm.OWM('dbeee7264d80b183568973e21e1633fd', config_dict)
mgr = owm.weather_manager()


#telegram bot

#token='915096497:AAFvPSbMpvjdtNSucGNwSy6afA8UURu89nI'




#testbot

token = '1225831912:AAG60sUGFoeRVePSufgLFM0Xaat176T2t1o'



bot = Bot(token)

dp = Dispatcher(bot)
db = SQLighter('db.db')

inline_btn_1 = InlineKeyboardButton('4🕓', callback_data='time4')
inline_btn_2 = InlineKeyboardButton('5🕔', callback_data='time5')
inline_btn_3 = InlineKeyboardButton('6🕕', callback_data='time6')
inline_btn_4 = InlineKeyboardButton('7🕖', callback_data='time7')
inline_btn_5 = InlineKeyboardButton('8🕗', callback_data='time8')
inline_btn_6 = InlineKeyboardButton('9🕘', callback_data='time9')
inline_btn_7 = InlineKeyboardButton('10🕙', callback_data='time10')
inline_btn_8 = InlineKeyboardButton('11🕚', callback_data='time11')
inline_btn_9 = InlineKeyboardButton('12🕛', callback_data='time12')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5, inline_btn_6, inline_btn_7, inline_btn_8, inline_btn_9)






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
		db.add_subscriber(message)
		await bot.send_message(214196761, '{0} added\n{1} {2} \n{3}'.format(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username))



@dp.callback_query_handler()
async def process_callback_button1(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	if callback_query.data=='time4':
		await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="время установлено на 4:00")
		db.add_time(callback_query.message.chat.id, "00")
	elif callback_query.data=='time5':
		await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="время установлено на 5:00")
		db.add_time(callback_query.message.chat.id, "01")
	elif callback_query.data=='time6':
		await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="время установлено на 6:00")
		db.add_time(callback_query.message.chat.id, "02")
	elif callback_query.data=='time7':
		await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="время установлено на 7:00")
		db.add_time(callback_query.message.chat.id, "03")
	elif callback_query.data=='time8':
		await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="время установлено на 8:00")
		db.add_time(callback_query.message.chat.id, "04")
	elif callback_query.data=='time9':
		await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="время установлено на 9:00")
		db.add_time(callback_query.message.chat.id, "05")
	elif callback_query.data=='time10':
		await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="время установлено на 10:00")
		db.add_time(callback_query.message.chat.id, "06")
	elif callback_query.data=='time11':
		await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="время установлено на 11:00")
		db.add_time(callback_query.message.chat.id, "07")
	elif callback_query.data=='time12':
		await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="время установлено на 12:00")
		db.add_time(callback_query.message.chat.id, "08")


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
	city = message.text[11:]
	if db.subscriber_exists(message.from_user.id) == 'da':
		if db.subscription_status(message.from_user.id):
			city = str(db.subscription_city(message.from_user.id))
			city = city[3:-4]
			time = str(db.get_time(message.from_user.id)[0][0] + 4) + ":00"
			await message.answer("Вы уже подписаны на город: {0}!\nуведомления приходят в {1} (МСК)\nдля отписки напиши /unsubscribe".format(city,time))
		else:
			if city == "":
				await message.answer('Используйте /subscribe "город"')
			else:
				await message.answer("выбери время: ", reply_markup=inline_kb1)
				db.update_subscription(message, True, city)		
	else:
		if city == "":
			db.add_subscriber(message)
			await bot.send_message(214196761, '{0} added\n{1} {2} \n{3}'.format(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username))
			await message.answer('Используйте /subscribe "город"')
		else:
			# если юзера нет в базе, добавляем его
			db.add_subscriber(message, True)
			db.update_subscription(message, True, city)
			await bot.send_message(214196761, '{0} added\n{1} {2} \n{3}'.format(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username))
			await message.answer("выбери время: ", reply_markup=inline_kb1)


			

@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
	if db.subscriber_exists(message.from_user.id) == 'da':
		if (db.subscription_status(message.from_user.id)):
			db.update_subscription(message, False)
			await message.answer('Вы успешно отписались от рассылки.\nдля подписки - /subscribe "город"')
		else:
			await message.answer('Вы и так ни на что не подписаны\nдля подписки - /subscribe "город"')
	else:
		# если юзера нет в базе, добавляем его с неактивной подпиской
		db.add_subscriber(message, False)
		await bot.send_message(214196761, '{0} added\n{1} {2} \n{3}'.format(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username))
		await message.answer('Вы и так ни на что не подписаны\nдля подписки - /subscribe "город"')



@dp.message_handler(commands=['forecast'])
async def unsubscribe(message: types.Message):
	city = str(message.text[10:])
	if city == '':
		await message.answer('Используйте: /forecast "город"')
		if db.subscriber_exists(message.from_user.id) == 'da':
			pass
		else:
			db.add_subscriber(message, False)
			await bot.send_message(214196761, '{0} added\n{1} {2} \n{3}'.format(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username))
	else:
		observation = mgr.weather_at_place(city)
		w = observation.weather
		fc1 = mgr.forecast_at_place(city,'3h')
		f = fc1.forecast
		reception_date = str(f)
		reception_date = reception_date[55:65]
		answer = ""
		for w in f:
			time = str(w.reference_time('iso'))
			date = time[:10] 
			if date == reception_date:
				time = str(time[11:16])
				temp = str(w.temperature('celsius')["temp"])
				detailed_status = w.detailed_status
				not_detailed = w.status
				answer1 = "{0}:\n{1}{3} {2}ºC\n\n".format(time,detailed_status,temp,emoji.get_emoji(not_detailed))
				answer = answer + answer1
		await message.answer('прогноз для города: ' +city + '\n\n' + answer)
		if db.subscriber_exists(message.from_user.id) == 'da':
			pass
		else:
			# если юзера нет в базе, добавляем его с неактивной подпиской
			db.add_subscriber(message, False)
			await bot.send_message(214196761, '{0} added\n{1} {2}\n{3}'.format(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username))
			



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
		db.add_subscriber(message)
		await bot.send_message(214196761, '{0} added\n{1} {2} \n{3}'.format(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username))
		
 


@dp.message_handler(content_types=['location'])
async def by_location(message: types.Message):
	f = open('location.txt', 'a')
	f.write(str(message.from_user.id) + '  ' + str(message.location.latitude) + '  ' + str(message.location.longitude) + '\n')
	f.close()
	
	await message.answer('показана погода возле ближайшей метеостанции')
	observation = mgr.weather_at_coords(int(message.location.latitude), int(message.location.longitude))
	w = observation.weather
	l = observation.location
	detailed_status = w.detailed_status
	not_detailed = w.status
	answer = ("В городе "+ l.name + " сейчас Ясно"+  str(emoji.get_emoji(not_detailed)) +"\n")
	answer += ("Температура: " + str(w.temperature('celsius')["temp"]) + "ºC \n")
	answer += ("Скорость ветра: " + str(w.wind()["speed"]) + "м/с\n")
	answer += ("Влажность: " + str(w.humidity) + "% \n\n")
	await message.answer(answer)

	if db.subscriber_exists(message.from_user.id) == 'da':
		pass
	else:
		# если юзера нет в базе, добавляем его
		db.add_subscriber(message)
		await bot.send_message(214196761, '{0} added\n{1} {2} \n{3}'.format(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username))
		



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
			await bot.send_message(214196761, "ошибка рассылки для " + str(db.all_users()[name][6]))
	else:
		try:
			observation = mgr.weather_at_place(message.text)
			w = observation.weather
			detailed_status = w.detailed_status
			not_detailed = w.status
			answer = ("В городе "+ message.text + " сейчас Ясно"+  str(emoji.get_emoji(not_detailed)) +"\n")
			answer += ("Температура: " + str(w.temperature('celsius')["temp"]) + "ºC \n")
			answer += ("Скорость ветра: " + str(w.wind()["speed"]) + "м/с\n")
			answer += ("Влажность: " + str(w.humidity) + "% \n\n")
			await message.answer(answer)
		except:
			await bot.send_message(message.chat.id, 'похоже произошла внутренняя ошибка \nпопробуй ещё раз')
		if db.subscriber_exists(message.from_user.id) == 'da':
			pass
		else:
			# если юзера нет в базе, добавляем его
			db.add_subscriber(message)
			await bot.send_message(214196761, '{0} added\n{1} {2} \n{3}'.format(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username))


	


async def time_check():
	while True:
		schedule.run_pending()
		await asyncio.sleep(1)


async def mailing():
	loop  =  asyncio.get_event_loop()
	subscriptions = db.get_subscriptions()
	for s in subscriptions:
		user_time = str(db.get_time(s[1])[0][0])
		city = str(db.subscription_city(s[1])[0])
		city = city[2:-3]
		observation = mgr.weather_at_place(city)
		w = observation.weather
		reference_time_1 = str(w.reference_time('iso')[11:16])[0:-3]
		if user_time == reference_time_1:
			fc1 = mgr.forecast_at_place(city,'3h')
			f = fc1.forecast
			reception_date = str(f)
			reception_date = reception_date[55:65]
			answer = ""
			for w in f:
				time = str(w.reference_time('iso') + 4)
				date = time[:10]
				if date == reception_date:
					time = str(time[11:16])
					temp = str(w.temperature('celsius')["temp"])
					detailed_status = w.detailed_status
					not_detailed = w.status
					answer1 = "{0}:\n{1}{3} {2}ºC\n\n".format(time,detailed_status,temp,emoji.get_emoji(not_detailed))
					answer = answer + answer1
			try:
				await bot.send_message(s[1],"⏰Время погоды🔔:")
				await bot.send_message(s[1],"Прогноз города {0}:\n{1}".format(city,answer))
			except:
				pass
		
		

def mailing123():
	asyncio.run_coroutine_threadsafe(mailing(), bot.loop)



schedule.every().day.at("00:00").do(mailing123)
schedule.every().day.at("01:00").do(mailing123)
schedule.every().day.at("02:00").do(mailing123)
schedule.every().day.at("03:00").do(mailing123)
schedule.every().day.at("04:00").do(mailing123)
schedule.every().day.at("05:00").do(mailing123)
schedule.every().day.at("06:00").do(mailing123)
schedule.every().day.at("07:00").do(mailing123)
schedule.every().day.at("08:00").do(mailing123) #время по гринвичу


if __name__ == '__main__':	
	dp.loop.create_task(time_check())
	executor.start_polling(dp, skip_updates=True)
