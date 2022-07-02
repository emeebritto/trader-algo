from tools.fibonacci import Fibonacci

class Analyzer:
	def __init__(self):
		self.maxValue = 0
		self.currentValue = 0
		self.minValue = 0
		self.currentCandle = {}
		self.fibonaccis = []


	def process(self):
		if len(self.fibonaccis) == 0:
			maxTraced = self.currentCandle.maxTraced
			minTraced = self.currentCandle.minTraced
			self.createFibo(maxTraced, minTraced)

		matches = self.checkMatches()
		self.updateCurrentFibo()


	def setValues(self, candle, maxV=None, currentValue=None, minV=None):
		self.maxValue = maxV if maxV != None else self.maxValue
		self.currentValue = currentValue if currentValue != None else self.currentValue
		self.minValue = minV if minV != None else self.minValue
		self.currentCandle = candle
		self.process()


	def checkMatches(self):
		matches = []
		for fibo in self.fibonaccis:
			matches.append(fibo.match(0, tolerance=20))
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
		fibo = Fibonacci(start, end, minDifference=300)
		self.fibonaccis.insert(0, fibo)


# f0Difference = abs(self.fibonaccis[0].f0 - candlePrice["maxTraced"])
# f38x2Difference = abs(self.fibonaccis[0].f38x2 - candlePrice["maxTraced"])