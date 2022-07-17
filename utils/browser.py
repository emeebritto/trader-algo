from PIL import Image
from logger import logger
from selenium import webdriver
from services.nexa import nexa
from utils.targets.binomo import Binomo
from utils.targets.iqoption import IqOption
from services.telegram_client import nexa_Telegram
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from time import sleep
import os
FIREFOX_DRIVER_PATH = './bin/geckodriver'



class Browser(Binomo):
  def __init__(self):
    super(Browser, self).__init__()
    self.options = ('--none', '--headless',)
    self.instance = None
    self._init_firefox()


  def _init_firefox(self):
    logger.log("Browser -> initializing browser.")
    firefox_options = webdriver.FirefoxOptions()
    binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))

    # firefox_options.add_argument('--headless')
    if self.options is not None:
      for option in self.options:
        firefox_options.add_argument(option)

    firefox_service = Service(
      executable_path=FIREFOX_DRIVER_PATH
    )

    browser = webdriver.Firefox(
      service=firefox_service,
      firefox_binary=binary,
      options=firefox_options
    )

    self.instance = browser


  def take_screenshot(self):
    self.instance.save_screenshot("screen.png")


  def send_msg_to_author(self, msg):
    nexa.send_to_author(msg)


  def send_screen_to_author(self):
    self.take_screenshot()
    nexa_Telegram.send_file_to_author("screen.png")


  def quit(self):
    self.instance.quit()



browser = Browser()


# os.environ.get('GECKODRIVER_PATH')