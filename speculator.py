from tools.fibonacci import Fibonacci
from entities.candle import Candle
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

		if len(self.fibonaccis) == 0:
			maxTraced = self.currentCandle.maxTraced
			minTraced = self.currentCandle.minTraced
			self.createFibo(maxTraced, minTraced)

		matches = self.checkMatches()
		self.updateCurrentFibo()


	def purchase(self):
		lastMousePosition = self.controller.position()
		self.controller.click(x=780, y=1280)
		self.controller.moveTo(lastMousePosition[0], lastMousePosition[1], 0.3)


	def sell(self):
		lastMousePosition = self.controller.position()
		self.controller.click(x=780, y=1340)
		self.controller.moveTo(lastMousePosition[0], lastMousePosition[1], 0.3)


	def checkMatches(self):
		matches = []
		for fibo in self.fibonaccis:
			matches.append(fibo.match(self.currentValue, tolerance=30))
		print(matches)


	def updateCurrentFibo(self):
		candleType = self.currentCandle.cType
		currentFibo = self.fibonaccis[0]
		outF100, outF0 = currentFibo.isOutRange(self.currentCandle.maxTraced)

		if outF0:
			currentFibo.update(end=self.currentCandle.maxTraced)
		if outF100:
			self.createFibo(currentFibo.end, self.currentCandle.maxTraced)
			self.fibonaccis.pop()


	def createFibo(self, start, end):
		fibo = Fibonacci(f"Fibo_{next(self._counter)}", start, end, minDifference=400)
		self.fibonaccis.insert(0, fibo)


	def analyzeCandle(self, frame):
		candle = Candle()
		for line in frame: 
			for (b, g, r) in line:
				candle.cType = self.__detectCandleColor(b, g, r) or candle.cType

			for index in range(len(line)):
				lastPixelBGR = (0, 0, 0) if index == 0 else line[index - 1]
				currentPixelBGR = line[index]
				nextPixelBGR = (0, 0, 0) if len(line) == index + 1 else line[index + 1]

				lastPixel = {
					"isGray": lastPixelBGR[0] < 50 and lastPixelBGR[1] < 50,
					"isGreen": lastPixelBGR[1] > 180 and lastPixelBGR[2] < 100,
					"isRed": lastPixelBGR[2] > 240 and lastPixelBGR[1] < 130
				}

				currentPixel = {
					"isGray": currentPixelBGR[0] < 50 and currentPixelBGR[1] < 50,
					"isGreen": currentPixelBGR[1] > 180 and currentPixelBGR[2] < 100,
					"isRed": currentPixelBGR[2] > 240 and currentPixelBGR[1] < 130
				}

				nextPixel = {
					"isGray": nextPixelBGR[0] < 50 and nextPixelBGR[1] < 50,
					"isGreen": nextPixelBGR[1] > 180 and nextPixelBGR[2] < 100,
					"isRed": nextPixelBGR[2] > 240 and nextPixelBGR[1] < 130
				}

				currentPixelIsCandle = currentPixel["isGreen"] or currentPixel["isRed"]
				nextPixelIsCandle = nextPixel["isGreen"] or nextPixel["isRed"]
				isCandleTrace = lastPixel["isGray"] and currentPixelIsCandle and nextPixel["isGray"]
				isCandleBody = currentPixelIsCandle and nextPixelIsCandle

				if currentPixel["isGray"]: continue # ignore empty/black pixels
				
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


# f0Difference = abs(self.fibonaccis[0].f0 - candlePrice["maxTraced"])
# f38x2Difference = abs(self.fibonaccis[0].f38x2 - candlePrice["maxTraced"])