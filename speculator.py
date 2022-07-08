from tools.fibonacci import FibonacciFactory
from random import randint
from itertools import count


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


	def speculate(self, candle, price=None):
		self.maxValue = price.maxValue if price != None else self.maxValue
		self.currentValue = price.current if price != None else self.currentValue
		self.minValue = price.minValue if price != None else self.minValue
		self.currentCandle = candle

		if len(self.fibonaccis) == 0: self.createFiboFromCandle(self.currentCandle)
		fibosMatches = self.checkFiboMatches(self.currentValue)
		currentFiboMatches = self.currentFibo.matchRange(
			start=self.currentCandle.entry,
			end=self.currentCandle.exit
		)

		print("fibosMatches", fibosMatches)
		print("currentFiboMatches", currentFiboMatches)

		# isInitialState = len(fibosMatches) == 1 and len(self.fibonaccis) == 1
		# hasMinMatches = len(fibosMatches) > 1 and len(self.fibonaccis) > 1
		hasValidMatches = bool(fibosMatches[0])
		hasMinMatches = (len(fibosMatches) - fibosMatches.count(None)) > 1
		isGreenCandle = candle.cType == 1
		isRedCandle = candle.cType == -1
		isUpTrend = self.currentFibo.direction == 1
		isDownTrend = self.currentFibo.direction == -1
		isFirstFiboSaturatedZone = fibosMatches[0] and fibosMatches[0].isSaturated

		if hasValidMatches and isFirstFiboSaturatedZone:
			if fibosMatches[0].label in ["f61x8", "f38x2"]:
				if hasMinMatches and isRedCandle and isUpTrend:
					self.purchase()
				elif hasMinMatches and isGreenCandle and isDownTrend:
					self.sell()
				self.createFibo(self.currentFibo.end, candle.maxTraced)
			if fibosMatches[0].label in ["f50"] and 38.2 in currentFiboMatches:
				if hasMinMatches and isRedCandle:
					self.purchase()
				elif hasMinMatches and isGreenCandle:
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


	def checkFiboMatches(self, value):
		matches = []
		for fibo in self.fibonaccis:
			result = fibo.match(value, tolerance=70)
			matches.append(result)
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
		fibo = FibonacciFactory.create(fiboName, start, end, minDifference=600)
		self.fibonaccis.insert(0, fibo)
		self.fibonaccis = self.fibonaccis[0:4]


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