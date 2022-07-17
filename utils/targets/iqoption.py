from logger import logger
from PIL import Image
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class IqOption:
	def __init__(self):
		super(IqOption, self).__init__()

	
	def _createLog(self, msg):
		logger.fullog(msg)


	def openChart(self):
		self._createLog("Browser -> getting aplication web.")
		self.instance.get('https://login.iqoption.com/en/login')
		sleep(8)
		self.send_screen_to_author()

		self._createLog("Browser -> insering account login.")
		mail_input = self.instance.find_element(By.NAME, "identifier")
		password_input = self.instance.find_element(By.NAME, "password")
		mail_input.send_keys("emersonbritto987@gmail.com")
		password_input.send_keys(r"y1q8uw2a")
		password_input.send_keys(Keys.ENTER)

		self._createLog("Browser -> sleeping.")
		sleep(4)
		self.send_screen_to_author()
		sleep(20)

		self._createLog("Browser -> selecting Trade Now (Button).")

		header = self.instance.find_element(By.TAG_NAME, "header")
		tradeNowButton = header.find_element(By.CLASS_NAME, "Button_orange")
		tradeNowButton.click()

		self._createLog("Browser -> sleeping.")
		# incomplete steps
		pass


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


	def send_screen_to_author(self):
		pass
