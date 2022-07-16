# import pyautogui as pg
import os
import pyscreeze

class Screen:
	def __init__(self):
		self.hasDisplay = not bool(os.environ.get("NO_DISPLAY"))
		# if self.hasDisplay: self._getScreenSize()


	# def _getScreenSize(self):
	# 	screenSize = pg.size()
	# 	self.width = screenSize.width
	# 	self.height = screenSize.height
	

	# def take_screenshot(self, region):
	# 	return pg.screenshot(region=region)


	# def locateOnScreen(self, baseFile, confidence, region):
	# 	return pg.locateOnScreen(baseFile, confidence=confidence, region=region)


	def locateOnImage(self, image, needleImage, confidence):
		return pyscreeze.locate(needleImage, image, confidence=confidence)
