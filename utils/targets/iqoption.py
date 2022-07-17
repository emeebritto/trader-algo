from logger import logger
from PIL import Image
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class IqOption:
	def __init__(self):
		super(IqOption, self).__init__()


	def openChart(self):
		logger.log("Browser -> getting aplication web.")
		self.instance.get('https://login.iqoption.com/en/login')
		sleep(8)
		self.send_screen_to_author()

	# 	logger.log("Browser -> insering account login.")
	# 	mail_input_wrapper = self.instance.find_element(By.TAG_NAME, "vui-input-text")
	# 	mail_input = mail_input_wrapper.find_element(By.TAG_NAME, "input")
	# 	password_input_wrapper = self.instance.find_element(By.TAG_NAME, "vui-input-password")
	# 	password_input = password_input_wrapper.find_element(By.TAG_NAME, "input")
	# 	mail_input.send_keys("emersonbritto987@gmail.com")
	# 	password_input.send_keys(r"y1q8uw2a")
	# 	password_input.send_keys(Keys.ENTER)

	# 	logger.log("Browser -> sleeping.")
	# 	sleep(4)
	# 	self.send_screen_to_author()
	# 	sleep(60)

	# 	logger.log("Browser -> selecting assets box.")

	# 	assets_tab_wrapper = self.instance.find_element(By.TAG_NAME, "vui-asset-tab")
	# 	assets_tab = assets_tab_wrapper.find_element(By.TAG_NAME, "button")
	# 	assets_tab.click()

	# 	logger.log("Browser -> sleeping.")
	# 	sleep(4)

	# 	logger.log("Browser -> selecting asset (EUR/USD).")

	# 	assets_block = self.instance.find_element(By.TAG_NAME, "assets-block")
	# 	asset_search_wrapper = assets_block.find_element(By.TAG_NAME, "asset-search")
	# 	asset_search = asset_search_wrapper.find_element(By.TAG_NAME, "input")
	# 	asset_search.send_keys("EUR/USD")

	# 	logger.log("Browser -> sleeping.")
	# 	sleep(4)

	# 	assets_result_wrapper = assets_block.find_element(By.TAG_NAME, "lib-platform-scroll")
	# 	asset_body = assets_result_wrapper.find_element(By.CLASS_NAME, "asset-body")
	# 	target_asset = asset_body.find_element(By.CLASS_NAME, "asset-row")
	# 	target_asset.click()

	# 	logger.log("Browser -> sleeping.")
	# 	sleep(4)

	# 	logger.log("Browser -> selecting chart time.")

	# 	chart_settings = self.instance.find_element(By.TAG_NAME, "chart-settings")
	# 	chart_Time_Button = chart_settings.find_element(By.ID, "qa_chartTimeButton")
	# 	chart_Time_Button.click()

	# 	sleep(4)

	# 	time_period = self.instance.find_element(By.TAG_NAME, "time-period")
	# 	fiveMChartTime = time_period.find_element(By.ID, "qa_5mChartTime")
	# 	fiveMChartTime.click()

	# 	logger.log("Browser -> chart ready.")

	# 	sleep(2)


	# def click_dealUpBtn(self):
	# 	dealUpButton = self.instance.find_element(By.CLASS_NAME, "qa_trading_dealUpButton")
	# 	dealUpButton.click()


	# def click_dealDownBtn(self):
	# 	dealDownButton = self.instance.find_element(By.CLASS_NAME, "qa_trading_dealDownButton")
	# 	dealDownButton.click()


	# def chart_price_screenshot(self):
	# 	app_chart = self.instance.find_element(By.TAG_NAME, "app-chart")
	# 	app_chart.screenshot('app_chart.png')
	# 	img = Image.open('app_chart.png')
	# 	w, h = img.size
	# 	# (left, upper, right, lower)
	# 	cropped_img = img.crop((int(w / 1.275), 0, w, h))
	# 	return cropped_img


	# def send_screen_to_author(self):
	# 	pass
