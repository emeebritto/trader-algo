from tools.fibonacci import Fibonacci

class Analyzer:
	def __init__(self):
		self.maxValue = 0
		self.currentValue = 0
		self.minValue = 0
		self.fibonaccis = []


	def process(self):
		if len(self.fibonaccis) == 0: self.createFibo()
		matches = self.checkMatches()
		# if matches[0] == 61.8:
		# 	print("...")


	def setValues(self, maxV=None, currentValue=None, minV=None):
		self.maxValue = maxV if maxV != None else self.maxValue
		self.currentValue = currentValue if currentValue != None else self.currentValue
		self.minValue = minV if minV != None else self.minValue
		self.process()


	def checkMatches(self):
		matches = []
		for fibo in self.fibonaccis:
			matches.append(fibo.match(0, tolerance=20))
		print(matches)


	def createFibo(self):
		fibo = Fibonacci(self.maxValue, self.minValue, minDifference=300)
		self.fibonaccis.insert(0, fibo)