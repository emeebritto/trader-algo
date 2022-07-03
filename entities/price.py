class Price:
	def __init__(self, value, maxV=None, minV=None):
		self.value = value
		self._maxValue = maxV or value
		self._minValue = minV or value


	def __repr__(self):
		return f"""
  price: {self.value}
  maxValue: {self._maxValue}
  minValue: {self._minValue}
"""


	@property
	def maxValue(self):
		return self._maxValue


	@property
	def minValue(self):
		return self._minValue


	@maxValue.setter
	def maxValue(self, val):
		if val > self._maxValue:
			self._maxValue = val


	@minValue.setter
	def minValue(self, val):
		if val < self._minValue:
			self._minValue = val


	def update(self, value):
		self.value = value
