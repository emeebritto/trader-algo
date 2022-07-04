import pyautogui as pg
import numpy as np
import cv2

class Screen:
	def __init__(self):
		self.width = pg.size().width
		self.height = pg.size().height
		

	def take_screenshot(self, region):
		region = (region["posX"], region["posY"], region["width"], region["height"])
		screenshot = pg.screenshot(region=region)
		screenshot.save("algo-view.png")
		screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
		return screenshot
