from entities.price import Price
from utils.screen import Screen
from entities.candle import Candle
from collections import deque
from time import sleep
from logger import logger
from utils.time import seconds, wait
from pytesseract import pytesseract
from configer import configer
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
		self._candles = deque([], maxlen=240)
		priceBarArea = configer.get("graphic.priceBarArea")
		self.priceBarArea = {
			"posX": priceBarArea["posX"] or (596 * self.width) // 900,
			"posY": priceBarArea["posY"] or (1050 * self.height) // 1600,
			"width": priceBarArea["width"] or (110 * self.width) // 900,
			"height": priceBarArea["height"] or (520 * self.height) // 1600
		}


	@property
	def candles(self):
		return self._candles


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
		logger.log("Graphic was started")


	def tradingWindow(self, callback, interval=0):
		self.trading = True
		tradingThr = threading.Thread(
			target=self._listenTrading,
			args=(callback, interval),
			kwargs={}
		)
		tradingThr.start()
		logger.log("Trading window was opened")


	def __closeWindow(self):
		self.trading = False


	def end(self):
		self.active = False
		self.closeWindow()


	def _listenPrice(self):
		logger.log("listening price")
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
					maxVariation = configer.get("graphic.priceListener.maxPriceVariation")
					if not self.price.last or abs(self.price.last - price) < maxVariation:
						self.price.update(price)
				except ValueError as e:
					print("not detected price. skipping interaction")
					logger.log("not detected price. skipping interaction")


	def _nextCandle(self):
		if self.currentCandle: self._candles.append(self.currentCandle)
		self.currentCandle = Candle(entry=self.price.current)


	def _processCandles(self):
		wait(lambda: self.price.current != 0)
		self._nextCandle()
		while self.active:
			sleep(1)
			if seconds() == 00:
				self._nextCandle()
				continue
			self.currentCandle.update(value=self.price.current)


	def _listenTrading(self, callback, interval):
		wait(lambda: self.price.current != 0 and self.currentCandle != None)
		while self.trading:
			callback(
				historic=self._candles,
				price=self.price,
				candle=self.currentCandle,
				close=self.__closeWindow
			)
			sleep(interval)
