from tools.fibonacci import FibonacciFactory
from services.nexa import nexa
from random import randint
from itertools import count
from configer import configer
from logger import logger
from utils.sound import sound


class Speculator:
	def __init__(self, reverseMode=False):
		self.maxValue = 0
		self.minValue = 0
		self.currentCandle = None
		self.price = None
		self.fibonaccis = []
		self._isTrading = True
		self._counter = count()
		self.__modules = []
		self._reverseMode = reverseMode
		if reverseMode: self.__reverseOperations()


	@property
	def currentFibo(self):
		return self.fibonaccis[0]


	@property
	def currentValue(self):
		return self.price.current


	@property
	def activeModules(self):
		return self.__modules


	@property
	def reverseMode(self):
		return self._reverseMode


	@property
	def isTrading(self):
		return self._isTrading


	@isTrading.setter
	def isTrading(self, val):
		if type(val) == bool and val != self._isTrading:
			isTradingLog = "speculator is trading now"
			isNotTradingLog = "speculator isn't trading, only analyzing"
			self._isTrading = val
			logger.fullog(isTradingLog if val == True else isNotTradingLog)


	@reverseMode.setter
	def reverseMode(self, val):
		if type(val) == bool and val != self._reverseMode:
			self._reverseMode = val
			self.__reverseOperations()
		elif val == self._reverseMode:
			logger.fullog(f"reverseMode already changed to {val}")


	def __reverseOperations(self):
		status = "Activated" if self._reverseMode else "Desactivated"
		logger.fullog(f"speculator -> ReverseMode was {status}")
		temp = getattr(self, "purchase")
		setattr(self, "purchase", getattr(self, "sell"))
		setattr(self, "sell", temp)


	def use(self, name, element):
		setattr(self, name, element)
		self.__modules.append(name)


	def remove(self, name):
		delattr(self, name)
		self.__modules.remove(name)


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
		hasValidMatches = bool(fibosMatches[0])
		isNotSaturatedZone = fibosMatches[0] and not fibosMatches[0].isSaturated

		if self.currentFibo.height >= 3000: self.createFiboFromCandle(self.currentCandle)
		else: self.updateCurrentFibo()

		if hasValidMatches and isNotSaturatedZone:
			self._analyzeFiboZone(fibosMatches, curFiboMatchRange)


	def _analyzeFiboZone(self, fibosMatches, curFiboMatchRange):
		if fibosMatches[0].label in ["f61x8", "f38x2"]:
			self._analyzeOperation(fibosMatches, curFiboMatchRange)
		if fibosMatches[0].label in ["f50"] and 38.2 in curFiboMatchRange:
			self._analyzeOperation(fibosMatches, curFiboMatchRange)


	def _analyzeOperation(self, fibosMatches, curFiboMatchRange):
		logger.fullog(f"speculator -> detected current fibonacci matches ({fibosMatches[0].label} - {fibosMatches[0]})")
		isInitialState = len(fibosMatches) == 1 and len(self.fibonaccis) == 1
		isGreenCandle = self.currentCandle.cType == 1
		isRedCandle = self.currentCandle.cType == -1
		isUpTrend = self.currentFibo.direction == 1
		isDownTrend = self.currentFibo.direction == -1
		hasMinMatches = (len(fibosMatches) - fibosMatches.count(None)) >= 1

		logiclog = f"""
isInitialState: {isInitialState}
isGreenCandle: {isGreenCandle}
isRedCandle: {isRedCandle}
isUpTrend: {isUpTrend}
isDownTrend: {isDownTrend}
hasMinMatches: {hasMinMatches}"""

		logger.fullog(logiclog)

		if (hasMinMatches or isInitialState) and self.isTrading:
			if isRedCandle and isUpTrend:
				self.purchase()
			elif isGreenCandle and isDownTrend:
				self.sell()
		self.createFibo(self.currentFibo.end, self.currentCandle.maxTraced)


	def purchase(self):
		self.graphic.purchase()
		sound.play("notifications_11.mp3")
		logger.fullog("speculator -> bought")


	def sell(self):
		self.graphic.sell()
		sound.play("notifications_11.mp3")
		logger.fullog("speculator -> sold")


	def checkFiboMatches(self, value):
		matches = []
		tolerance = configer.get("fibonacci.zoneTolerance")
		for fibo in self.fibonaccis:
			result = fibo.match(value, tolerance=tolerance)
			matches.append(result)
		return matches


	def updateCurrentFibo(self):
		currentFibo = self.fibonaccis[0]
		outF100, outF0 = currentFibo.isOutRange(self.currentCandle.maxTraced)
		revalidateWith = self.graphic.candles.maxTraced()

		if outF0:
			logger.log("price was out of range (f0) of the current fibonacci")
			currentFibo.update(
				end=self.currentCandle.maxTraced,
				revalidateWith=revalidateWith
			)
		if outF100:
			logger.log("price was out of range (f100) of the current fibonacci")
			currentFibo.update(
				start=currentFibo.end,
				end=self.currentCandle.maxTraced,
				revalidateWith=revalidateWith
			)


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
			validateWith=self.graphic.candles.maxTraced()
		)
		self.fibonaccis.insert(0, fibo)
		self.fibonaccis = self.fibonaccis[0:maxActiveFibonaccis]



speculator = Speculator(reverseMode=False)

nexa.learn(
  label="/reverse_mode",
  action=lambda: setattr(speculator, "reverseMode", not speculator.reverseMode)
)
nexa.learn(
  label="/pause_trading",
  action=lambda: setattr(speculator, "isTrading", False)
)
nexa.learn(
  label="/return_trading",
  action=lambda: setattr(speculator, "isTrading", True)
)


# ctr.moveTo(self.view.width / 2.5, self.view.height / 3, 0.3)
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