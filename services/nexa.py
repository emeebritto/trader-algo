import requests
import threading
from time import sleep


class Nexa:
	def __init__(self):
		super(Nexa, self).__init__()
		self.__token = "5435366586:AAE9L0ZVNTEkAIHg12LssdsVgtV36I7BYVc"
		self.__author = '1242558424'
		self.__author_name = "Emerson_Britto"
		self.api_url = f"https://api.telegram.org/bot{self.__token}"
		self._commands = {}
		th = threading.Thread(target=self._listenCommands, args=(), kwargs={})
		th.start()


	def learnModule(self, module):
		for name, val in module.__dict__.items():
			if callable(val): self.learn(label=name, action=val)


	def learn(self, label, action):
		print(f"Nexa learned to {label}")
		self._commands[label] = action


	def _listenCommands(self):
		while True:
			msg = self.wait_new_message(user=self.__author_name)
			command = self._commands.get(msg)
			if command: command()
			else: self.send_to_author(msg="sorry, I don't know how do it :(")


	def _request(self, link):
		response = requests.get(link)
		return response.json()


	def filter_msg(self, user, msgs):
		filtered_msg = []
		for msg in msgs:
			if not msg.get("message"): continue
			elif msg["message"]["from"]["username"] == user:
				filtered_msg.append(msg)
		return filtered_msg


	def input(self, label):
		self.send_to_author(msg=label)
		return self.wait_new_message(user=self.__author_name)


	def send_to_author(self, msg):
		return self.send_message(self.__author, msg)


	def send_file_to_author(self, filePATH):
		return self.send_file(filePATH, chatID=self.__author)


	def send_message(self, chatID, msg):
		params = f"chat_id={chatID}&parse_mode=Markdown&text={msg}"
		send_text = f"{self.api_url}/sendMessage?{params}"
		return self._request(send_text)


	def send_file(self, filePATH, chatID):
		with open(filePATH, "rb") as file:
		  return requests.post(
		  	f"{self.api_url}/sendDocument",
				data={'chat_id': chatID},
				files={'document': file}
		  ).json()


	def get_updates(self, user=None):
		updates = f"{self.api_url}/getUpdates"
		if user: return self.filter_msg(user, self._request(updates)["result"])
		return self._request(updates)["result"]


	def last_message(self, user=None):
		updates = self.get_updates(user=user)
		return updates[-1] if len(updates) else None


	def wait_new_message(self, user=None, metadata=False):
		lastUpdate = self.last_message(user=user)
		def compareRequests():
			newRequest = self.last_message(user=user)
			if not lastUpdate and newRequest: return False
			if not newRequest: return True
			return lastUpdate["update_id"] == newRequest["update_id"]

		while compareRequests(): sleep(1)
		lastUpdate = self.last_message(user=user)
		if metadata: return lastUpdate
		else: return lastUpdate["message"]["text"]



nexa = Nexa()




# nexa.learnModule(services.nexaActions)
# print("waiting your message..")
# print(nexa.last_message(user="Emerson-Britto"))
# print(nexa.wait_new_message(user="Emerson_Britto"))
# res = nexa.send_file_to_author("../app_chart.png")
# print(res)