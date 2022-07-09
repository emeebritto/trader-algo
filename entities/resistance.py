class Resistance:
	def __init__(self, label, value, validadeWith=None):
		super(Resistance, self).__init__()
		self._isActive = True
		self._forceActive = True
		self.isSaturated = False
		self.label = label
		self.value = value
		self.__valuesMatches = []
		if validadeWith: self.validateWith(validadeWith)


	@property
	def valuesMatches(self):
		return self.__valuesMatches


	@property
	def isActive(self):
		return self._isActive


	@property
	def forceActive(self):
		return self._forceActive


	@property
	def matchesNumber(self):
		return len(self.__valuesMatches)


	@forceActive.setter
	def forceActive(self, val):
		self._forceActive = val
		self._isActive = self._forceActive


	def updateStatus(func):
		def function(*args, **kwargs):
			returnFc = func(*args, **kwargs)
			if args[0].matchesNumber > 3 or args[0].forceActive: args[0]._isActive = True
			else: args[0]._isActive = False
			return returnFc
		return function


	@updateStatus
	def isMatch(self, value, tolerance=70):
		if abs(value - self.value) <= tolerance:
			self.valuesMatches.append(value)
			if self._isActive: return True
		return False


	@updateStatus
	def validateWith(self, values, tolerance=70):
		self.forceActive = False
		for value in values:
			self.isMatch(value, tolerance)
