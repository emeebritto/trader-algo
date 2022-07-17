import telebot
from logger import logger
from telethon.sync import TelegramClient
from telethon import TelegramClient
from services.nexa import nexa


class Nexa_Telegram:
  def __init__(self):
    super(Nexa_Telegram, self).__init__()
    self.api_id = "16533245"
    self.api_hash = "77a7ed7f8a140b7d3d124ed34e6f4170"
    self.phone = "+5573991973084"
    self.author = "Emerson_Britto"
    self.client = TelegramClient('session', self.api_id, self.api_hash)
    self.client.connect()
    self._verify_authorization()

  def _verify_authorization(self):
    if not self.client.is_user_authorized():
      self.client.send_code_request(self.phone)
      self.client.sign_in(self.phone, nexa.input('Enter the code (Telegram Code): '))


  def send_to_author(self, msg):
    return self.send_message(user=self.author, msg=msg)


  def received_from_author(self):
    return self.received_message(name=self.author.replace("_", " "))


  def send_file_to_author(self, filePATH):
    try:
      self.client.send_file(self.author, filePATH)
    except Exception as e:
      logger.outlog(e)


  def send_message(self, user, msg):
    try:
      self.client.send_message(user, msg)
    except Exception as e:
      logger.log(e)


  def received_message(self, name):
    for dialog in self.client.get_dialogs():
      if dialog.name == name:
        return dialog.message.message


  def wait_new_message(self, name):
    lastUpdate = self.received_message(name=name)
    def compareRequests():
      newRequest = self.received_message(name=name)
      return lastUpdate == newRequest

    while compareRequests(): sleep(1)
    return self.received_message(name=name)


  def disconnect(self):
    self.client.disconnect()


nexa_Telegram = Nexa_Telegram()
# nexa_Telegram.send_file_to_author("../app_chart.png")
# print(nexa_Telegram.received_message("Emerson Britto"))
# telegram.send_message(user="Emerson_Britto", msg="From Nexa")
