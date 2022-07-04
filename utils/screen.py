import pyautogui as pg


class Screen:
	def __init__(self):
		screenSize = pg.size()
		self.width = screenSize.width
		self.height = screenSize.height
		

	def take_screenshot(self, region):
		return pg.screenshot(region=region)
