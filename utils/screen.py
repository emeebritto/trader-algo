import pyautogui as pg


class Screen:
	def __init__(self):
		screenSize = pg.size()
		self.width = screenSize.width
		self.height = screenSize.height
	

	def take_screenshot(self, region):
		return pg.screenshot(region=region)


	def locateOnScreen(self, baseFile, confidence, region):
		return pg.locateOnScreen(baseFile, confidence=confidence, region=region)
