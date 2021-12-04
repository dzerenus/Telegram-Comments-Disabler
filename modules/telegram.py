import requests
import json

from modules.methods import post

# Функция получения обновлений бота.
# Возвращает update_id последнего сообщения и список сообщений
def get_updates(tg_token, update_id):
	# Отправляем пост запрос в tg и переводим ответ в json
	url = 'https://api.telegram.org/bot'+tg_token+'/getUpdates'
	headers = {'Content-Type': 'application/json; charset=utf-8'}
	payload = {
		"allowed_updates": '["callback_query","message"]',
		"offset": str(update_id + 1)
	}
	req_json = post(url=url, headers=headers, data=payload)

	upds = []
	if req_json['ok'] == True:
		for update_json in req_json['result']:
			upd = Update(update_json)
			upds.append(upd)

	return upds


def send_message(tg_token, chat_id, text, reply_markup=""):
	url = 'https://api.telegram.org/bot'+tg_token+'/sendMessage'
	headers = {'Content-Type': 'application/json; charset=utf-8'}
	payload = {
		"chat_id": str(chat_id),
		"text": text,
		"parse_mode": "HTML",
		"disable_web_page_preview": True,
		"reply_markup": reply_markup
	}
	post(url=url, headers=headers, data=payload)

def edit_message_text(tg_token, message_id, chat_id, text, reply_markup=""):
	url = 'https://api.telegram.org/bot'+tg_token+'/editMessageText'
	headers = {'Content-Type': 'application/json; charset=utf-8'}
	payload = {
		"chat_id": str(chat_id),
		"message_id": str(message_id),
		"text": text,
		"parse_mode": "HTML",
		"disable_web_page_preview": True,
		"reply_markup": reply_markup
	}
	post(url=url, headers=headers, data=payload)

def send_photo(tg_token, chat_id, photo, caption, reply_markup=""):
	url = 'https://api.telegram.org/bot'+tg_token+'/sendPhoto'
	headers = {'Content-Type': 'application/json; charset=utf-8'}
	payload = {
		"chat_id": str(chat_id),
		"caption": text,
		'reply_markup': reply_markup,
		'parse_mode': 'HTML',
		'photo': photo
	}
	
	post(url=url, headers=headers, data=payload)

def delete_message(tg_token, chat_id, message_id):
	url = 'https://api.telegram.org/bot'+tg_token+'/deleteMessage'
	headers = {'Content-Type': 'application/json; charset=utf-8'}
	payload = {
		"chat_id": str(chat_id),
		"message_id": str(message_id),
	}
	
	post(url=url, headers=headers, data=payload)

def answer_callback_query(tg_token, callback_query_id, text):
	url = 'https://api.telegram.org/bot'+tg_token+'/answerCallbackQuery'
	headers = {'Content-Type': 'application/json; charset=utf-8'}
	payload = {
		"show_alert": True,
		"callback_query_id": str(callback_query_id),
		"text": text
	}

	post(url=url, headers=headers, data=payload)

def leave_chat(tg_token, chat_id):
	url = f'https://api.telegram.org/bot{tg_token}/leaveChat'
	headers = {'Content-Type': 'application/json; charset=utf-8'}
	payload = {
		"chat_id": str(chat_id),
	}

	post(url=url, headers=headers, data=payload)


# Класс Update TG бота с некоторыми упрощениями
class Update(object):
	"""docstring for ClassName"""
	def __init__(self, json_update):
		self.update_id = json_update['update_id']
		
		if 'message' in json_update.keys():
			self.type = 'message'
			self.message = Message(json_update['message'])
		if 'callback_query' in json_update.keys():
			self.type = 'callback_query'
			self.callback_query = CallbackQuery(json_update['callback_query'])

# Класс CallbackQuery TG бота с некоторыми упрощениями
class CallbackQuery(object):
	def __init__(self, callback_json):
		self.id = callback_json['id']
		self.from_id = callback_json['from']['id']

		if 'message' in callback_json.keys():
			self.message = Message(callback_json['message'])
		else:
			self.message = None

		if 'data' in callback_json.keys():
			self.data = callback_json['data']
		else:
			self.data = None

# Класс Message TG бота с некоторыми упрощениями
class Message(object):
	def __init__(self, json_msg):
		self.id = json_msg['message_id']
		self.chat= Chat(json_msg['chat'])
		self.date = json_msg['date']
		self.sender = None
		self.sender_chat = None
		self.forward_from = None
		self.forward_from_chat = None
		self.text = None
		self.caption = None
		self.entities = None

		keys = json_msg.keys()
		if 'from' in keys: 
			self.sender = User(json_msg['from']) 

		if 'sender_chat' in keys:
			self.sender_chat = Chat(json_msg['sender_chat'])
		
		if 'forward_from' in keys:
			self.forward_from = User(json_msg['forward_from']) 

		if 'forward_from_chat' in keys:
			self.forward_from_chat = Chat(json_msg['forward_from_chat'])

		if 'text' in keys:
			self.text = json_msg['text']

		if 'caption' in keys:
			self.caption = json_msg['caption']

		if 'entities' in keys:
			self.entities = []

			for ent in json_msg['entities']:
				e = MessageEntity(ent)
				self.entities.append(e)


class MessageEntity(object):
	def __init__(self, js):
		self.type = js['type']
		self.offset = js['offset']
		self.length = js['length']

		if self.type == 'text_link':
			self.url = js['url']

		if self.type == 'text_mention':
			self.user = User(js['user'])

		if self.type == 'pre':
			self.language = js['language']


# Класс пользователя Telegram.
class User(object):
	def __init__(self, js):
		self.id = js['id']
		self.is_bot = js['is_bot']
		self.first_name = js['first_name']


class Chat(object):
	def __init__(self, js):
		self.id = js['id']
		self.type = js['type']

		if 'title' in js.keys():
			self.title = js['title']

		if 'username' in js.keys():
			self.username = js['username']



def InlineKeyboardButton(text, callback_data) -> dict:
	d = {
		'text': text, 
		'callback_data': callback_data
		}

	return d


def InlineKeyboardMarkup(buttons) -> dict:
	data = {
		"inline_keyboard": []
	}

	for button in buttons:
		data["inline_keyboard"].append(button)

	return data		
	
