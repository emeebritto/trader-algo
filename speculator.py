from tools.fibonacci import Fibonacci
from itertools import count

class Speculator:
	def __init__(self):
		self.maxValue = 0
		self.currentValue = 0
		self.minValue = 0
		self.currentCandle = {}
		self.fibonaccis = []
		self.counter = count()


	def process(self):
		if len(self.fibonaccis) == 0:
			maxTraced = self.currentCandle.maxTraced
			minTraced = self.currentCandle.minTraced
			self.createFibo(maxTraced, minTraced)

		matches = self.checkMatches()
		self.updateCurrentFibo()


	def setValues(self, candle, price=None):
		self.maxValue = price.maxValue if price != None else self.maxValue
		self.currentValue = price.current if price != None else self.currentValue
		self.minValue = price.minValue if price != None else self.minValue
		self.currentCandle = candle
		self.process()


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
		fibo = Fibonacci(f"Fibo_{next(self.counter)}", start, end, minDifference=400)
		self.fibonaccis.insert(0, fibo)


# f0Difference = abs(self.fibonaccis[0].f0 - candlePrice["maxTraced"])
# f38x2Difference = abs(self.fibonaccis[0].f38x2 - candlePrice["maxTraced"])