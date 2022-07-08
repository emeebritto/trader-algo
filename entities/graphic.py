from entities.price import Price
from utils.screen import Screen
from entities.candle import Candle
from time import sleep
from tools.time import seconds, wait
from pytesseract import pytesseract
import threading
import numpy as np
import cv2
import re


class Graphic(Screen):
	def __init__(self):
		super(Graphic, self).__init__()
		self.timeframe = 1
		self.active = False
		self.trading = False
		self.price = Price(0)
		self.currentCandle = None
		self._candles = []
		self.priceBarArea = {
			"posX": (596 * self.width) // 900,
			"posY": (1050 * self.height) // 1600,
			"width": (110 * self.width) // 900,
			"height": (520 * self.height) // 1600
		}


	def getPrice(self):
		return self.price


	def start(self):
		self.active = True
		priceThr = threading.Thread(
			target=self._listenPrice,
			args=(),
			kwargs={}
		)
		candlesThr = threading.Thread(
			target=self._processCandles,
			args=(),
			kwargs={}
		)
		priceThr.start()
		candlesThr.start()


	def tradingWindow(self, callback, interval=0):
		self.trading = True
		tradingThr = threading.Thread(
			target=self._listenTrading,
			args=(callback, interval),
			kwargs={}
		)
		tradingThr.start()


	def __closeWindow(self):
		self.trading = False


	def end(self):
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

			if not priceBar: continue

			priceBarPosition = (priceBar.left, priceBar.top, priceBar.width, priceBar.height)
			screenshot = self.take_screenshot(region=priceBarPosition)
			thresh = cv2.threshold(np.array(screenshot), 150, 0, 76, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
			rawStr = pytesseract.image_to_string(thresh, config='--psm 6')
			priceFormat = r"[0-9]*\.[0-9]*"
			matches = re.findall(priceFormat, rawStr)
			if len(matches) and matches[len(matches) -1]:
				try:
					price = int(matches[len(matches) -1].replace(".", ""))
					if not self.price.last or abs(self.price.last - price) < 50000:
						self.price.update(price)
				except ValueError as e:
					print("not detected price. skipping interaction")


	def _nextCandle(self):
		self._candles.append(self.currentCandle)
		self.currentCandle = Candle(entry=self.price.current)


	def _processCandles(self):
		wait(lambda: self.price.current != 0)
		self.currentCandle = Candle(entry=self.price.current)
		while self.active:
			sleep(1)
			if seconds() == 00:
				self._nextCandle()
				continue
			self.currentCandle.update(value=self.price.current)


	def _listenTrading(self, callback, interval):
		while self.trading:
			callback(
				historic=self._candles,
				price=self.price,
				candle=self.currentCandle,
				close=self.__closeWindow
			)
			sleep(interval)
