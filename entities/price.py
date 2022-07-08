from collections import deque

class Price:
	def __init__(self, value, maxV=None, minV=None):
		self.startedAt = value
		self._values = deque([value], maxlen=2)
		self._maxValue = maxV or value
		self._minValue = minV or value


	def __repr__(self):
		return f"""
  started at {self.startedAt}
  maxValue: {self._maxValue}{self.strPrice()}
  minValue: {self._minValue}
"""


	@property
	def current(self):
		return self._values[-1]


	@property
	def last(self):
		try:
			return self._values[-2]
		except IndexError as e:
			return None


	@property
	def maxValue(self):
		return self._maxValue


	@property
	def minValue(self):
		return self._minValue


	@current.setter
	def current(self, val):
		self._values.append(val) 


	@maxValue.setter
	def maxValue(self, val):
		if val > self._maxValue:
			self._maxValue = val


	@minValue.setter
	def minValue(self, val):
		if val < self._minValue:
			self._minValue = val


	def update(self, value):
		value = value
		self._values.append(value)
		if value > self._maxValue:
			self._maxValue = value
		if value < self._minValue or self._minValue == 0:
			self._minValue = value


	def strPrice(self):
		if not self.last: return f"""
  - price (current): {self.current}"""
		if self.current > self.last:
			return f"""
  ^ price (current): {self.current}
  | price (last): {self.last}"""
		elif self.current == self.last:
			return f"""
  - price (current): {self.current}
  - price (last): {self.last}"""
		else:
			return f"""
  | price (last): {self.last}
  v price (current): {self.current}"""