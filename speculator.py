from tools.fibonacci import FibonacciFactory
from entities.candle import Candle
from random import randint
from itertools import count
import numpy as np
import cv2


class Speculator:
	def __init__(self):
		self.maxValue = 0
		self.currentValue = 0
		self.minValue = 0
		self.currentCandle = {}
		self.fibonaccis = []
		self._counter = count()
		self.view = None
		self.controller = None


	@property
	def currentFibo(self):
		return self.fibonaccis[0]


	def useView(self, view):
		self.view = view


	def useController(self, ctr):
		ctr.moveTo(self.view.width / 2.5, self.view.height / 3, 0.3)
		self.controller = ctr


	def readView(self, region):
		region = (region["posX"], region["posY"], region["width"], region["height"])
		screenshot = self.view.take_screenshot(region=region)
		screenshot.save("algo-view.png")
		screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
		return screenshot


	def __detectCandleColor(self, b, g, r):
		isRed = r > 240
		isGreen = g > 180 and r < 100
		if isRed: return -1
		if isGreen: return 1


	def speculate(self, candle, price=None):
		self.maxValue = price.maxValue if price != None else self.maxValue
		self.currentValue = price.current if price != None else self.currentValue
		self.minValue = price.minValue if price != None else self.minValue
		self.currentCandle = candle

		if len(self.fibonaccis) == 0: self.createFiboFromCandle(self.currentCandle)
		fiboMatches = self.checkMatches()

		print("fiboMatches", fiboMatches)

		if fiboMatches[0] in [61.8, 38.2]:
			if self.currentCandle.cType == -1 and self.currentFibo.direction == 1:
				self.purchase()
			elif self.currentCandle.cType == 1 and self.currentFibo.direction == -1:
				self.sell()
			self.createFibo(self.currentFibo.end, candle.maxTraced)
		self.updateCurrentFibo()


	def purchase(self):
		lastMousePosition = self.controller.position()
		posX = (randint(750, 860) * self.view.width) / 900
		posY = (randint(1275, 1290) * self.view.height) / 1600
		self.controller.click(x=posX, y=posY)
		self.controller.moveTo(lastMousePosition[0], lastMousePosition[1], 0.3)


	def sell(self):
		lastMousePosition = self.controller.position()
		posX = (randint(750, 860) * self.view.width) / 900
		posY = (randint(1335, 1350) * self.view.height) / 1600
		self.controller.click(x=posX, y=posY)
		self.controller.moveTo(lastMousePosition[0], lastMousePosition[1], 0.3)


	def checkMatches(self):
		matches = []
		for fibo in self.fibonaccis:
			matches.append(fibo.match(self.currentValue, tolerance=45))
		return matches


	def updateCurrentFibo(self):
		candleType = self.currentCandle.cType
		currentFibo = self.fibonaccis[0]
		outF100, outF0 = currentFibo.isOutRange(self.currentCandle.maxTraced)

		if outF0:
			currentFibo.update(end=self.currentCandle.maxTraced)
		if outF100:
			currentFibo.update(start=currentFibo.end, end=self.currentCandle.maxTraced)


	def createFiboFromCandle(self, candle):
		self.createFibo(candle.minTraced, candle.maxTraced)


	def createFibo(self, start, end):
		fiboName = f"Fibo_{next(self._counter)}"
		fibo = FibonacciFactory.create(fiboName, start, end, minDifference=400)
		self.fibonaccis.insert(0, fibo)
		self.fibonaccis = self.fibonaccis[0:3]


	def analyzeCandle(self, frame):
		candle = Candle()
		for line in frame: 
			for (b, g, r) in line:
				candle.cType = self.__detectCandleColor(b, g, r) or candle.cType

			for index in range(len(line)):
				lastPixelBGR = (0, 0, 0) if index == 0 else line[index - 1]
				currentPixelBGR = line[index]
				nextPixelBGR = (0, 0, 0) if len(line) == index + 1 else line[index + 1]

				isGray = lambda pixelBGR: pixelBGR[0] < 50 and pixelBGR[1] < 50
				isGreen = lambda pixelBGR: pixelBGR[1] > 180 and pixelBGR[2] < 100
				isRed = lambda pixelBGR: pixelBGR[2] > 240 and pixelBGR[1] < 130

				currentPixelIsCandle = isGreen(currentPixelBGR) or isRed(currentPixelBGR)
				nextPixelIsCandle = isGreen(nextPixelBGR) or isRed(nextPixelBGR)
				isCandleTrace = isGray(lastPixelBGR) and currentPixelIsCandle and isGray(nextPixelBGR)
				isCandleBody = currentPixelIsCandle and nextPixelIsCandle

				if isGray(currentPixelBGR): continue # ignore empty/black pixels
				
				if candle.cType == 1:
					if candle.bodyLength == 0 and isCandleTrace:
						candle.exitTraceLength += 1
						break

					if isCandleBody:
						candle.bodyLength += 1
						break

					if candle.bodyLength > 0 and isCandleTrace:
						candle.entryTraceLength += 1
						break
				else:
					if candle.bodyLength == 0 and isCandleTrace:
						candle.entryTraceLength += 1
						break

					if isCandleBody and candle.cType == -1:
						candle.bodyLength += 1
						break

					if candle.bodyLength > 0 and isCandleTrace:
						candle.exitTraceLength += 1
						break
		return candle


# if self.currentCandle.cType == -1 and self.currentFibo.direction == 1:
# 	self.purchase()

# f0Difference = abs(self.fibonaccis[0].f0 - candlePrice["maxTraced"])
# f38x2Difference = abs(self.fibonaccis[0].f38x2 - candlePrice["maxTraced"])