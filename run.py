import yaml
from modules import telegram
from time import sleep


token = None
channelID = None
whitelist = None

# Функция загрузки информации из yaml файла.
# Возвращает токен бота, ID канала, список слов.
def load_config(file_name):
	f = open(file_name)
	f = yaml.load(f, Loader=yaml.FullLoader)

	global token
	global channelID
	global whitelist

	token = f['Token']
	channelID = f['ChannelID']
	whitelist = f['WhiteList']


def prepare(upd):
	if upd.type != 'message': return

	if not upd.message.sender_chat: return
	if upd.message.sender_chat.id != channelID: return

	text = ''
	if upd.message.text: text = upd.message.text
	if upd.message.caption: text = upd.message.caption

	text = text.lower()

	is_del = True
	for e in whitelist: 
		if e in text: is_del = False

	if is_del:
		telegram.delete_message(token, upd.message.chat.id, upd.message.id)


def main():
	# Загрузка информации из config файла.
	load_config("config.yaml")

	first = True
	update_id = 0
	while True:
		# Получаем обновления.
		new_updates = telegram.get_updates(token, update_id)

		# Если полученных обновлений больше, чем 0:
		# Складываем их с теми, что уже в очереди.
		# Обновляем update_id по последнему из них.
		if len(new_updates) > 0:
			update_id = new_updates[-1].update_id
			for upd in new_updates: prepare(upd)
		if first: first = False
		sleep(1)


if __name__ == '__main__':
	main()