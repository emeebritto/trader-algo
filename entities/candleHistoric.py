from collections import deque

class CandleHistoric:
	def __init__(self, initialList=[], maxlen=None):
		super(CandleHistoric, self).__init__()
		self.__historic = deque(initialList, maxlen=maxlen)


	@property
	def current(self):
		return self.__historic[-1:]
	

	def append(self, value):
		self.__historic.append(value)


	def insert(self, pos, value):
		self.__historic.insert(pos, value)


	def maxValue(self):
		return max([candle.maxValue for candle in self.__historic])


	def minValue(self):
		return min([candle.minValue for candle in self.__historic])


	def maxTraced(self):
		return [candle.maxTraced for candle in self.__historic]


	def minTraced(self):
		return [candle.minTraced for candle in self.__historic]


	def valuesRange(self, start, end, base):
		values = []
		for attr in base:
			values.extend([getattr(candle, attr) for candle in self.__historic])

		startIndex = None
		endIndex = len(values)
		for index, value in enumerate(values):
			if value == start: startIndex = index
			if value == end: endIndex = index + 1

		return values[startIndex:endIndex] if startIndex else None