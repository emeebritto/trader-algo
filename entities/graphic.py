from entities.price import Price
from entities.candle import Candle
from entities.candleHistoric import CandleHistoric
from collections import deque
from time import sleep
from logger import logger
from services.nexa import nexa
from utils.time import seconds, wait, time
from pytesseract import pytesseract
from configer import configer
from utils.screen import Screen
from utils.browser import Browser
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
		self.currentCandle1m = None
		self.currentCandle5m = None
		self.browser = Browser()
		self._candles1m = CandleHistoric([], maxlen=240)  # 1 minutes
		self._candles5m = CandleHistoric([], maxlen=240) # 5 minutes


	@property
	def candles(self):
		return self._candles1m


	def getPrice(self):
		return self.price


	def start(self):
		logger.fullog("Starting Graphic")
		self.browser.openChart()
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
		logger.fullog("Graphic was started")


	def tradingWindow(self, callback, interval=0):
		self.trading = True
		tradingThr = threading.Thread(
			target=self._listenTrading,
			args=(callback, interval),
			kwargs={}
		)
		tradingThr.start()
		logger.outlog(f"Trading window was opened (timeframe: {self.timeframe})")


	def __closeWindow(self):
		self.trading = False


	def end(self):
		self.active = False
		self.__closeWindow()


	def purchase(self):
		self.browser.purchase()


	def sell(self):
		self.browser.sell()


	def _listenPrice(self):
		logger.log("listening price")
		while self.active:
			screenshot = self.browser.chart_price_screenshot()
			if not screenshot: continue

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
			# cv2.imshow("thresh", thresh)
			# cv2.waitKey(0)
			priceFormat = r"[0-9]*\.[0-9]*"
			matches = re.findall(priceFormat, rawStr)

			if not len(matches):
				# print("not detected price. trying second method")
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
					logger.outlog("not detected price. skipping interaction")


	def _nextCandle1m(self):
		if self.currentCandle1m: self._candles1m.append(self.currentCandle1m)
		self.currentCandle1m = Candle(entry=self.price.current)


	def _nextCandle5m(self):
		if self.currentCandle5m: self._candles5m.append(self.currentCandle5m)
		self.currentCandle5m = Candle(entry=self.price.current)


	def _processCandles(self):
		wait(lambda: self.price.current != 0)
		self._nextCandle1m()
		self._nextCandle5m()
		while self.active:
			sleep(1)
			if seconds() == 00:
				self._nextCandle1m()
			if f"{time().minute}"[1] in ['0', '5']:
				self._nextCandle5m()
			self.currentCandle1m.update(value=self.price.current)
			self.currentCandle5m.update(value=self.price.current)


	def _listenTrading(self, callback, interval):
		wait(lambda: self.price.current != 0 and self.currentCandle1m != None)
		while self.trading:
			callback(
				historic=self._candles1m,
				price=self.price,
				candle=self.currentCandle1m,
				close=self.__closeWindow
			)
			sleep(interval)



graphic = Graphic()
browser = graphic.browser

nexa.learn(
  label="/take_screenshot",
  action=lambda: browser.send_screen_to_author(filePath="screen_to_author.png")
)
nexa.learn(
  label="/refresh_browser",
  action=browser.refresh
)
nexa.learn(
  label="/purchase",
  action=graphic.purchase
)
nexa.learn(
  label="/sell",
  action=graphic.sell
)