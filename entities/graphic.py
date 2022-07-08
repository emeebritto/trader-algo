from entities.price import Price
from utils.screen import Screen
from time import sleep
from pytesseract import pytesseract
import threading
import numpy as np
import cv2
import re


class Graphic(Screen):
	def __init__(self, timeframe=1):
		super(Graphic, self).__init__()
		self.timeframe = timeframe
		self.active = False
		self.trading = False
		self.price = Price(0)
		self.priceBarArea = {
			"posX": (596 * self.width) // 900,
			"posY": (1053 * self.height) // 1600,
			"width": (110 * self.width) // 900,
			"height": (520 * self.height) // 1600
		}


	def getPrice(self):
		return self.price


	def start(self):
		self.active = True
		thr = threading.Thread(
			target=self._listenPrice,
			args=(),
			kwargs={}
		)
		thr.start()


	def tradingWindow(self, callback, interval=0):
		self.trading = True
		thr = threading.Thread(
			target=self._listenTrading,
			args=(callback, interval),
			kwargs={}
		)
		thr.start()


	def __closeWindow(self):
		self.trading = False


	def end():
		self.active = False
		self.closeWindow()


	def _listenPrice(self):
		while self.active:
			priceBar = self.locateOnScreen(
				'priceBar_target.png',
				confidence=.6,
				region=(
					self.priceBarArea["posX"],
					self.priceBarArea["posY"],
					self.priceBarArea["width"],
					self.priceBarArea["height"]
				)
			)

			priceBarPosition = (priceBar.left, priceBar.top, priceBar.width, priceBar.height)
			screenshot = self.take_screenshot(region=priceBarPosition)
			thresh = cv2.threshold(np.array(screenshot), 150, 0, 76, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
			rawStr = pytesseract.image_to_string(thresh, config='--psm 6')
			priceFormat = r"[0-9]*\.[0-9]*"
			matches = re.findall(priceFormat, rawStr)
			if len(matches):
				self.price.update(format(float(matches[len(matches) -1]), ".7f"))


	def _listenTrading(self, callback, interval):
		while self.trading:
			callback(price=self.price, close=self.__closeWindow)
			sleep(interval)
