from PIL import Image
from logger import logger
from selenium import webdriver
from services.telegram_client import nexa_Telegram
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from time import sleep
import os
FIREFOX_DRIVER_PATH = './bin/geckodriver'



class Browser:
  def __init__(self):
    super(Browser, self).__init__()
    self.options = ('--none',)
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


  def _detect_noRobot_box(self):
    pass


  def openChart(self):
    logger.log("Browser -> getting aplication web.")
    self.instance.get('https://binomo.com/trading')
    sleep(8)
    self.send_screen_to_author()

    logger.log("Browser -> insering account login.")
    mail_input_wrapper = self.instance.find_element(By.TAG_NAME, "vui-input-text")
    mail_input = mail_input_wrapper.find_element(By.TAG_NAME, "input")
    password_input_wrapper = self.instance.find_element(By.TAG_NAME, "vui-input-password")
    password_input = password_input_wrapper.find_element(By.TAG_NAME, "input")
    mail_input.send_keys("emersonbritto987@gmail.com")
    password_input.send_keys(r"y1q8uw2a")
    password_input.send_keys(Keys.ENTER)

    logger.log("Browser -> sleeping.")
    sleep(4)
    self.send_screen_to_author()
    sleep(60)

    logger.log("Browser -> selecting assets box.")

    assets_tab_wrapper = self.instance.find_element(By.TAG_NAME, "vui-asset-tab")
    assets_tab = assets_tab_wrapper.find_element(By.TAG_NAME, "button")
    assets_tab.click()

    logger.log("Browser -> sleeping.")
    sleep(4)

    logger.log("Browser -> selecting asset (EUR/USD).")

    assets_block = self.instance.find_element(By.TAG_NAME, "assets-block")
    asset_search_wrapper = assets_block.find_element(By.TAG_NAME, "asset-search")
    asset_search = asset_search_wrapper.find_element(By.TAG_NAME, "input")
    asset_search.send_keys("EUR/USD")

    logger.log("Browser -> sleeping.")
    sleep(4)

    assets_result_wrapper = assets_block.find_element(By.TAG_NAME, "lib-platform-scroll")
    asset_body = assets_result_wrapper.find_element(By.CLASS_NAME, "asset-body")
    target_asset = asset_body.find_element(By.CLASS_NAME, "asset-row")
    target_asset.click()

    logger.log("Browser -> sleeping.")
    sleep(4)

    logger.log("Browser -> selecting chart time.")

    chart_settings = self.instance.find_element(By.TAG_NAME, "chart-settings")
    chart_Time_Button = chart_settings.find_element(By.ID, "qa_chartTimeButton")
    chart_Time_Button.click()

    sleep(4)

    time_period = self.instance.find_element(By.TAG_NAME, "time-period")
    fiveMChartTime = time_period.find_element(By.ID, "qa_5mChartTime")
    fiveMChartTime.click()

    logger.log("Browser -> chart ready.")

    sleep(2)


  def click_dealUpBtn(self):
    dealUpButton = self.instance.find_element(By.CLASS_NAME, "qa_trading_dealUpButton")
    dealUpButton.click()


  def click_dealDownBtn(self):
    dealDownButton = self.instance.find_element(By.CLASS_NAME, "qa_trading_dealDownButton")
    dealDownButton.click()


  def chart_price_screenshot(self):
    app_chart = self.instance.find_element(By.TAG_NAME, "app-chart")
    app_chart.screenshot('app_chart.png')
    img = Image.open('app_chart.png')
    w, h = img.size
    # (left, upper, right, lower)
    cropped_img = img.crop((int(w / 1.275), 0, w, h))
    return cropped_img


  def take_screenshot(self):
    self.instance.save_screenshot("screen.png")


  def send_screen_to_author(self):
    self.take_screenshot()
    nexa_Telegram.send_file_to_author("screen.png")


  def quit(self):
    self.instance.quit()



browser = Browser()


# os.environ.get('GECKODRIVER_PATH')