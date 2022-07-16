from entities.price import Price
from entities.candle import Candle
from entities.candleHistoric import CandleHistoric
from collections import deque
from time import sleep
from logger import logger
from utils.time import seconds, wait
from pytesseract import pytesseract
from configer import configer
from utils.screen import Screen
from utils.browser import browser
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
		self._candles = CandleHistoric([], maxlen=240)


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
			screenshot = browser.chart_price_screenshot()
			priceBar = self.locateOnImage(
				screenshot,
				needleImage='priceBar_target.png',
				confidence=.6
			)

			if not priceBar: continue

			priceBarPosition = (
				priceBar.left+23,
				priceBar.top+10,
				priceBar.width+priceBar.left,
				priceBar.top+priceBar.height-4
			)

			cropped_img = screenshot.crop(priceBarPosition)
			# 140, 40, 136 or 180, 80, 226
			thresh = cv2.threshold(np.array(cropped_img), 140, 40, 136, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
			rawStr = pytesseract.image_to_string(thresh, config='--psm 6')
			# print("rawStr: ", rawStr)
			# cv2.imshow("thresh", thresh)
			# cv2.waitKey(0)
			priceFormat = r"[0-9]*\.[0-9]*"
			matches = re.findall(priceFormat, rawStr)

			if not len(matches):
				print("not detected price. trying second method")
				thresh = cv2.threshold(np.array(cropped_img), 180, 80, 226, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
				rawStr = pytesseract.image_to_string(thresh, config='--psm 6')
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
