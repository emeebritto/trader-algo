from tools.fibonacci import FibonacciFactory
from random import randint
from itertools import count
from configer import configer
from logger import logger


class Speculator:
	def __init__(self):
		self.maxValue = 0
		self.minValue = 0
		self.currentCandle = None
		self.price = None
		self.fibonaccis = []
		self._counter = count()
		self.view = None
		self.graphic = None
		self.controller = None


	@property
	def currentFibo(self):
		return self.fibonaccis[0]


	@property
	def currentValue(self):
		return self.price.current


	def useView(self, view):
		self.view = view


	def useGraphic(self, graphic):
		self.graphic = graphic


	def useController(self, ctr):
		ctr.moveTo(self.view.width / 2.5, self.view.height / 3, 0.3)
		self.controller = ctr


	def speculate(self, candle, price):
		self.price = price
		self.currentCandle = candle

		if len(self.fibonaccis) == 0: self.createFiboFromCandle(self.currentCandle)
		fibosMatches = self.checkFiboMatches(self.currentValue)
		curFiboMatchRange = self.currentFibo.matchRange(
			start=self.currentCandle.entry,
			end=self.currentCandle.exit
		)

		print("fibosMatches", fibosMatches)
		print("curFiboMatchRange", curFiboMatchRange)

		isInitialState = len(fibosMatches) == 1 and len(self.fibonaccis) == 1
		# hasMinMatches = len(fibosMatches) > 1 and len(self.fibonaccis) > 1
		hasValidMatches = bool(fibosMatches[0])
		hasMinMatches = (len(fibosMatches) - fibosMatches.count(None)) > 1
		isGreenCandle = candle.cType == 1
		isRedCandle = candle.cType == -1
		isUpTrend = self.currentFibo.direction == 1
		isDownTrend = self.currentFibo.direction == -1
		isNotSaturatedZone = fibosMatches[0] and not fibosMatches[0].isSaturated

		if hasValidMatches and isNotSaturatedZone:
			if fibosMatches[0].label in ["f61x8", "f38x2"]:
				logger.log("speculator -> detected current fibonacci matches (f61x8 - f38x2)")
				if (hasMinMatches or isInitialState) and isRedCandle and isUpTrend:
					self.purchase()
				elif (hasMinMatches or isInitialState) and isGreenCandle and isDownTrend:
					self.sell()
				self.createFibo(self.currentFibo.end, candle.maxTraced)
			if fibosMatches[0].label in ["f50"] and 38.2 in curFiboMatchRange:
				logger.log("speculator -> detected current fibonacci matches (f50)")
				if (hasMinMatches or isInitialState) and isRedCandle:
					self.purchase()
				elif (hasMinMatches or isInitialState) and isGreenCandle:
					self.sell()
				self.createFibo(self.currentFibo.end, candle.maxTraced)
		self.updateCurrentFibo()


	def purchase(self):
		lastMousePosition = self.controller.position()
		positionBtn = configer.get("buttons.purchase")
		posX = positionBtn["posX"] or (randint(750, 860) * self.view.width) / 900
		posY = positionBtn["posY"] or (randint(1275, 1290) * self.view.height) / 1600
		self.controller.click(x=posX, y=posY)
		logger.log("speculator -> bought")
		self.controller.moveTo(lastMousePosition[0], lastMousePosition[1], 0.3)


	def sell(self):
		lastMousePosition = self.controller.position()
		positionBtn = configer.get("buttons.sell")
		posX = positionBtn["posX"] or (randint(750, 860) * self.view.width) / 900
		posY = positionBtn["posY"] or (randint(1335, 1350) * self.view.height) / 1600
		self.controller.click(x=posX, y=posY)
		logger.log("speculator -> sold")
		self.controller.moveTo(lastMousePosition[0], lastMousePosition[1], 0.3)


	def checkFiboMatches(self, value):
		matches = []
		tolerance = configer.get("fibonacci.zoneTolerance")
		for fibo in self.fibonaccis:
			result = fibo.match(value, tolerance=tolerance)
			matches.append(result)
		return matches


	def updateCurrentFibo(self):
		candleType = self.currentCandle.cType
		currentFibo = self.fibonaccis[0]
		outF100, outF0 = currentFibo.isOutRange(self.currentCandle.maxTraced)

		if outF0:
			logger.log("price was out of range (f0) of the current fibonacci")
			currentFibo.update(end=self.currentCandle.maxTraced)
		if outF100:
			logger.log("price was out of range (f100) of the current fibonacci")
			currentFibo.update(start=currentFibo.end, end=self.currentCandle.maxTraced)


	def createFiboFromCandle(self, candle):
		self.createFibo(candle.minTraced, candle.maxTraced)


	def createFibo(self, start, end):
		fiboName = f"Fibo_{next(self._counter)}"
		minDifference = configer.get("fibonacci.activeIfHeight")
		maxActiveFibonaccis = configer.get("speculator.maxActiveFibonaccis")
		fibo = FibonacciFactory.create(
			name=fiboName,
			start=start,
			end=end,
			minDifference=minDifference,
			validateWith=[candle.maxTraced for candle in self.graphic.candles]
		)
		self.fibonaccis.insert(0, fibo)
		self.fibonaccis = self.fibonaccis[0:maxActiveFibonaccis -1]




# if self.currentCandle.cType == -1 and self.currentFibo.direction == 1:
# 	self.purchase()

# f0Difference = abs(self.fibonaccis[0].f0 - candlePrice["maxTraced"])
# f38x2Difference = abs(self.fibonaccis[0].f38x2 - candlePrice["maxTraced"])

# priceBar = self.view.locateOnScreen(
# 	'priceBar_target.png',
# 	confidence=.6,
# 	region=priceBarRegion
# )

# priceBarPosition = (priceBar.left, priceBar.top, priceBar.width, priceBar.height)