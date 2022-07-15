import telebot
from telethon.sync import TelegramClient
from telethon import TelegramClient
from services.nexa import nexa


class Nexa_Telegram:
  def __init__(self):
    super(Telegram, self).__init__()
    self.api_id = "16533245"
    self.api_hash = "77a7ed7f8a140b7d3d124ed34e6f4170"
    self.phone = "+5573991973084"
    self.client = TelegramClient('session', self.api_id, self.api_hash)
    self.client.connect()
    self._verify_authorization()

  def _verify_authorization(self):
    if not self.client.is_user_authorized():
      self.client.send_code_request(self.phone)
      self.client.sign_in(self.phone, input('Enter the code: '))


  def send_message(self, user, msg):
    try:
      self.client.send_message(user, msg)
    except Exception as e:
      print(e);


  def received_message(self, name):
    for dialog in self.client.get_dialogs():
      if dialog.name == name:
        return dialog.message.message


  def disconnect(self):
    self.client.disconnect()


nexa_Telegram = Nexa_Telegram()
print(nexa_Telegram.received_message("Emerson Britto"))
#telegram.send_message(user="Emerson_Britto", msg="From Nexa")
