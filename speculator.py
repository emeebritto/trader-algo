from tools.fibonacci import FibonacciFactory
from random import randint
from itertools import count
from configer import configer
from logger import logger
from utils.sound import sound



class Vars:
	def __init__(self):
		super(Vars, self).__init__()
		self.__vars = []


	def create(self, values):
		for key, value in values.items():
			setattr(self, key, value)
			self.__vars.append(key)


	def use(self, key):
		return getattr(self, key)



class Actions:
	def __init__(self, owner):
		super(Actions, self).__init__()
		self.owner = owner
		self.__actions = []


	def create(self, name, action, constraints, exceptions):
		if not name or not action: return
		func = lambda: action(self=self.owner, vars=self.owner.vars, actions=self)
		setattr(self, name, func)
		self.__actions.append(name)


	def execute(self, name, args=[], kwargs={}):
		method = getattr(self, key)
		return method(*args, **kwargs)



class Speculator:
	def __init__(self):
		self.maxValue = 0
		self.minValue = 0
		self.currentCandle = None
		self.price = None
		self.fibonaccis = []
		self._counter = count()
		self.__modules = []
		self.vars = Vars()
		self.actions = Actions(owner=self)
		self.exceptions = None
		self.constraints = None
		self.allowance = None


	@property
	def currentFibo(self):
		return self.fibonaccis[0]


	@property
	def currentValue(self):
		return self.price.current


	@property
	def activeModules(self):
		return self.__modules


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

		self.vars.create({
			"fibosMatches": fibosMatches,
			"isInitialState": len(fibosMatches) == 1 and len(self.fibonaccis) == 1,
			"hasValidMatches": bool(fibosMatches[0]),
			"hasMinMatches": (len(fibosMatches) - fibosMatches.count(None)) > 1,
			"isGreenCandle": candle.cType == 1,
			"isRedCandle": candle.cType == -1,
			"isUpTrend": self.currentFibo.direction == 1,
			"isDownTrend": self.currentFibo.direction == -1,
			"isNotSaturatedZone": fibosMatches[0] and not fibosMatches[0].isSaturated
		})

		# self.vars.create({
		# 	"hasMinMatches": len(fibosMatches) > 1 and len(self.fibonaccis) > 1
		# })

		self.actions.analyzerFiboZone()
		self.updateCurrentFibo()

	
	def purchase(self):
		lastMousePosition = self.controller.position()
		positionBtn = configer.get("buttons.purchase")
		posX = positionBtn["posX"] or (randint(750, 860) * self.view.width) / 900
		posY = positionBtn["posY"] or (randint(1275, 1290) * self.view.height) / 1600
		self.controller.click(x=posX, y=posY)
		sound.play("notifications_11.mp3")
		logger.log("speculator -> bought")
		self.controller.moveTo(lastMousePosition[0], lastMousePosition[1], 0.3)


	def sell(self):
		lastMousePosition = self.controller.position()
		positionBtn = configer.get("buttons.sell")
		posX = positionBtn["posX"] or (randint(750, 860) * self.view.width) / 900
		posY = positionBtn["posY"] or (randint(1335, 1350) * self.view.height) / 1600
		self.controller.click(x=posX, y=posY)
		sound.play("notifications_11.mp3")
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
		revalidateWith = [candle.maxTraced for candle in self.graphic.candles]

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
			validateWith=[candle.maxTraced for candle in self.graphic.candles]
		)
		self.fibonaccis.insert(0, fibo)
		self.fibonaccis = self.fibonaccis[0:maxActiveFibonaccis -1]


speculator = Speculator()



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
