import random



def get_emoji(status):
	status = status.lower()
	try:
		if status == 'clear':
			r = random.randint(0,1)
			if r == 0:
				return('☀')
			elif r == 1:
				return('🌞')
		elif status == 'clouds':
			r = random.randint(0,3)
			if r == 0:
				return('⛅')
			elif r == 1:
				return('☁')
			elif r == 2:
				return('🌥')
			elif r == 3:
				return('🌤')
		elif status == 'shower rain':
			r = random.randint(0,5)
			if r == 0:
				return('🌧')
			elif r == 2:
				return('🌂')
			elif r == 3:
				return('☂')
			elif r == 4:
				return('☔')
		elif status == 'rain':
			r = random.randint(0,1)
			if r == 0:
				return('⛆')
			elif r == 1:
				return('🌦')
		elif status == 'thunderstorm':
			r = random.randint(0,2)
			if r == 0:
				return('🌩')
			elif r == 1:
				return('🌪')
			elif r == 2:
				return('⛈')
		elif status == 'snow':
			r = random.randint(0,3)
			if r == 0:
				return('🌨')
			elif r == 1:
				return('⛄')
			elif r == 2:
				return('❄')
			elif r == 3:
				return('☃')
		elif status == 'mist':
			return('🌫')
		else:
			return('')
	except:
		return('')