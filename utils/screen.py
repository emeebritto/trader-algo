import pyautogui as pg


class Screen:
	def __init__(self):
		self.width = pg.size().width
		self.height = pg.size().height
		pg.moveTo(self.width / 2.5, self.height / 3, 0.5)
		

	def take_screenshot(self, region):
		return pg.screenshot(region=region)
