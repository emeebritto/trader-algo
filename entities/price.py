class Price:
	def __init__(self, value, maxV=None, minV=None):
		self.startedAt = value
		self._values = [value, value]
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
		return self._values[0]


	@property
	def last(self):
		return self._values[1]


	@property
	def maxValue(self):
		return self._maxValue


	@property
	def minValue(self):
		return self._minValue


	@current.setter
	def current(self, val):
		self._values.insert(0, val)
		self._values = self._values[0:2] 


	@maxValue.setter
	def maxValue(self, val):
		if val > self._maxValue:
			self._maxValue = val


	@minValue.setter
	def minValue(self, val):
		if val < self._minValue:
			self._minValue = val


	def strPrice(self):
		if self._values[0] > self._values[1]:
			return f"""
  ^ price (current): {self._values[0]}
  | price (last): {self._values[1]}"""
		elif self._values[0] == self._values[1]:
			return f"""
  - price (current): {self._values[0]}
  - price (last): {self._values[1]}"""
		else:
			return f"""
  | price (last): {self._values[1]}
  v price (current): {self._values[0]}"""	
