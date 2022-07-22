import sys
import os
import datetime
import threading
from PIL import Image
from logger import logger
from selenium import webdriver
from services.nexa import nexa
from utils.targets.binomo import Binomo
from utils.targets.iqoption import IqOption
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from time import sleep
FIREFOX_DRIVER_PATH = './bin/geckodriver'



class Browser(Binomo):
  def __init__(self):
    super(Browser, self).__init__()
    self.instance = None
    self._init_firefox()


  # force one instance
  def __new__(cls, *args, **kwargs):
    if not hasattr(cls, '_alreadyExists'):
      cls._alreadyExists = object.__new__(cls)
      
    return cls._alreadyExists


  def _init_firefox(self):
    logger.log("Browser -> initializing browser.")
    firefox_options = webdriver.FirefoxOptions()
    binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))

    if "-h" in sys.argv or os.environ.get("IS_SERVER"):
      firefox_options.add_argument('--headless')

    firefox_service = Service(
      executable_path=FIREFOX_DRIVER_PATH
    )

    browser = webdriver.Firefox(
      service=firefox_service,
      firefox_binary=binary,
      options=firefox_options
    )

    self.instance = browser


  def autoRefresh(self, interval=None):
    th = threading.Thread(
      target=self._autoRefresh,
      args=(),
      kwargs={"interval": interval}
    )
    th.start()


  def _autoRefresh(self, interval=None):
    if type(interval) != int: return
    logger.fullog(f"auto refresh was activated (interval: {interval})")
    while True:
      sleep(interval * 60)
      self.refresh()


  def refresh(self):
    logger.fullog("Refreshing Browser")
    self.instance.refresh()


  def _detect_noRobot_box(self):    
    try:
      return self.instance.find_element(By.TAG_NAME, "tbody")
    except Exception as e:
      return False


  def passCaptcha(self, targetNode):
    logger.fullog("bot was detected")
    imgs_box = targetNode.find_elements(By.CLASS_NAME, "rc-imageselect-tile")
    res = nexa.input("please, which box should I click?")
    res = res.split("-")
    for idx, box in enumerate(imgs_box):
      if str(idx) in res:
        box.click()


  def take_screenshot(self, filePath=None):
    time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
    filePathDefault = f"screenshots/screen_{time}.png"
    filePath = filePath if filePath else filePathDefault
    self.instance.save_screenshot(filePath)
    return filePath


  def send_msg_to_author(self, msg):
    nexa.send_to_author(msg)


  def send_screen_to_author(self, filePath=None):
    filePath = self.take_screenshot(filePath)
    nexa.send_file_to_author(filePath)


  def quit(self):
    self.instance.quit()



# browser = Browser()
# os.environ.get('GECKODRIVER_PATH')