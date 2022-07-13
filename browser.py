from PIL import Image
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
FIREFOX_DRIVER_PATH = './bin/geckodriver'



class Browser:
  def __init__(self):
    super(Browser, self).__init__()
    self.options = ('--none',)
    self.instance = None
    self._init_firefox()


  def _init_firefox(self):
    firefox_options = webdriver.FirefoxOptions()

    # firefox_options.add_argument('--headless')
    if self.options is not None:
      for option in self.options:
        firefox_options.add_argument(option)

    firefox_service = Service(
      executable_path=FIREFOX_DRIVER_PATH,
    )

    browser = webdriver.Firefox(
      service=firefox_service,
      options=firefox_options
    )

    self.instance = browser


  def openChart(self):
    self.instance.get('https://binomo.com/trading')
    mail_input_wrapper = self.instance.find_element(By.TAG_NAME, "vui-input-text")
    mail_input = mail_input_wrapper.find_element(By.TAG_NAME, "input")
    password_input_wrapper = self.instance.find_element(By.TAG_NAME, "vui-input-password")
    password_input = password_input_wrapper.find_element(By.TAG_NAME, "input")
    mail_input.send_keys("emersonbritto987@gmail.com")
    password_input.send_keys(r"MY_PASSWORD")
    mail_input.send_keys(Keys.ENTER)

    sleep(15)

    assets_tab_wrapper = self.instance.find_element(By.TAG_NAME, "vui-asset-tab")
    assets_tab = assets_tab_wrapper.find_element(By.TAG_NAME, "button")
    assets_tab.click()

    sleep(4)

    assets_block = self.instance.find_element(By.TAG_NAME, "assets-block")
    asset_search_wrapper = assets_block.find_element(By.TAG_NAME, "asset-search")
    asset_search = asset_search_wrapper.find_element(By.TAG_NAME, "input")
    asset_search.send_keys("EUR/USD")

    sleep(4)

    assets_result_wrapper = assets_block.find_element(By.TAG_NAME, "lib-platform-scroll")
    asset_body = assets_result_wrapper.find_element(By.CLASS_NAME, "asset-body")
    target_asset = asset_body.find_element(By.CLASS_NAME, "asset-row")
    target_asset.click()

    sleep(4)

    chart_settings = self.instance.find_element(By.TAG_NAME, "chart-settings")
    chart_Time_Button = chart_settings.find_element(By.ID, "qa_chartTimeButton")
    chart_Time_Button.click()

    sleep(4)

    time_period = self.instance.find_element(By.TAG_NAME, "time-period")
    fiveMChartTime = time_period.find_element(By.ID, "qa_5mChartTime")
    fiveMChartTime.click()

    sleep(2)


  def click_dealUpBtn(self):
    dealUpButton = self.instance.find_element(By.CLASS_NAME, "qa_trading_dealUpButton")
    dealUpButton.click()


  def click_dealDownBtn(self):
    dealDownButton = self.instance.find_element(By.CLASS_NAME, "qa_trading_dealDownButton")
    dealDownButton.click()


  def chart_screenshot(self, region):
    # app_chart = self.instance.find_element(By.TAG_NAME, "app-chart")
    # app_chart.screenshot('app_chart.png')
    # (left, upper, right, lower)
    img = Image.open('app_chart.png')
    w, h = img.size
    cropped_img = img.crop(region)
    return cropped_img

  def quit(self):
    self.instance.quit()



browser = Browser()
