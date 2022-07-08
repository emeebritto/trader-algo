from collections import deque

class FibonacciLine:
	def __init__(self, parent, label, value=0):
		self._isActive = True
		self.isSaturated = False
		self.parent = parent
		self.label = label
		self.value = value
		self._sleep = 0


	def __repr__(self):
		if not self._isActive: return f"""{self.value} [inactive]"""
		if self.isSaturated: return f"""{self.value} [saturated]"""
		return f"""{self.value}"""


	@property
	def isActive(self):
		return self._isActive


	@property
	def sleep(self):
		return self._sleep


	@sleep.setter
	def sleep(self, val):
		if type(val) != int: return
		self._sleep = val
		self.isActive = not bool(self._sleep)


	def countSleep(func):
		def function(*args, **kwargs):
			returnFc = func(*args, **kwargs)
			if args[0]._sleep: args[0].sleep -= 1
			return returnFc
		return function


	@countSleep
	def isMatch(self, value, tolerance=0):
		"""Return 'None' if FibonacciLine is inactive"""
		"""Return 'True/False' if FibonacciLine is active"""
		if not self.isActive: return None
		return abs(value - self.value) <= tolerance



class Fibonacci:
	def __init__(self, name, start=0, end=0, minDifference=0):
		self.name = name
		self.start = start
		self.end = end
		self._minDifference = minDifference
		self.direction = -1 if self.start >= self.end else 1
		self.inactive = False  # fibonacci status
		self._startChild = None
		self._endChild = None
		self._matchesHistoric = deque([], maxlen=9)

		self.f100 = FibonacciLine(parent=self, label="f100", value=0)
		self.f61x8 = FibonacciLine(parent=self, label="f61x8", value=0)
		self.f50 = FibonacciLine(parent=self, label="f50", value=0)
		self.f38x2 = FibonacciLine(parent=self, label="f38x2", value=0)
		self.f0 = FibonacciLine(parent=self, label="f0", value=0)

		self.processValues()


	def __repr__(self):
		return f"""
  name: {self.name}
  inactive: {self.inactive}
  difference: {self.difference} (require: {self._minDifference})
  start: {self.start}
  end: {self.end}
{self.strMetrics()}
"""


	@property
	def fiboMetrics(self):
		if self.inactive:
			print("inactive Fibonacci")
			return

		fibo = {
			"100": self.f100.value,
			"61.8": self.f61x8.value,
			"50": self.f50.value,
			"38.2": self.f38x2.value,
			"0": self.f0.value
		}
		return fibo


	@property
	def startChild(self):
		return self._startChild


	@property
	def endChild(self):
		return self._endChild


	@startChild.setter
	def startChild(self, child):
		child.update(
			start=self.f100.value,
			end=self.f61x8.value,
			minDifference=self._minDifference
		)
		self._startChild = child


	@endChild.setter
	def endChild(self, child):
		child.update(
			start=self.f38x2.value,
			end=self.f0.value,
			minDifference=self._minDifference
		)
		self._endChild = child


	def strMetrics(self):
		if self.start > self.end:
			return f"""
  | metrics =====================
  | 100: {self.f100}
  | 61.8: {self.f61x8}
  | 50: {self.f50}
  | 38.2: {self.f38x2}
  v 0: {self.f0}
"""
		else:
			return f"""
  ^ metrics =====================
  | 0: {self.f0}
  | 38.2: {self.f38x2}
  | 50: {self.f50}
  | 61.8: {self.f61x8}
  | 100: {self.f100}
"""			


	def processValues(self):
		self.difference = abs(self.start - self.end)
		if self.difference < self._minDifference:
			self.inactive = True
		else:
			self.inactive = False

		if self.start > self.end:
			self.f100.value = self.end + self.difference
			self.f61x8.value = self.end + ((self.difference * 61.8) / 100)
			self.f50.value = self.end + ((self.difference * 50) / 100)
			self.f38x2.value = self.end + ((self.difference * 38.2) / 100)
			self.f0.value = self.end + ((self.difference * 0) / 100)
		else:
			self.f100.value = self.end - self.difference
			self.f61x8.value = self.end - ((self.difference * 61.8) / 100)
			self.f50.value = self.end - ((self.difference * 50) / 100)
			self.f38x2.value = self.end - ((self.difference * 38.2) / 100)
			self.f0.value = self.end - ((self.difference * 0) / 100)


	def updateChildren(self):
		if self._startChild: self._startChild.update(start=self.f100.value, end=self.f61x8.value)
		if self._endChild: self._endChild.update(start=self.f38x2.value, end=self.f0.value)


	def update(self, start=None, end=None, minDifference=None):
		self.start = start or self.start
		self.end = end or self.end
		self._minDifference = minDifference or self._minDifference
		self.direction = -1 if self.start >= self.end else 1
		self.processValues()
		self.updateChildren()


	def isOutRange(self, value):
		"""return (outF100, outF0)"""
		if self.start > self.end:
			if value > self.f100.value:
				# out of range on top (f100)
				return (True, False)
			elif value < self.f0.value:
				# out of range on bottom (f0)
				return (False, True)
		else:
			if value < self.f100.value:
				# out of range on bottom (f100)
				return (True, False)
			elif value > self.f0.value:
				# out of range on top (f0)
				return (False, True)

		return (False, False)


	def _checkChildrenMatches(self, value, tolerance):
		if self._startChild:
			startChildMatches = self._startChild.match(value, tolerance)
			if startChildMatches in [61.8, 38.2]:
				self._startChild = None
				return startChildMatches
		if self._endChild:
			endChildMatches = self._endChild.match(value, tolerance)
			if endChildMatches in [61.8, 38.2]:
				self._endChild = None
				return endChildMatches


	def registerHistoric(func):
		def function(*args, **kwargs):
			returnFc = func(*args, **kwargs)
			if not returnFc:
				return None
			elif not returnFc.label in args[0]._matchesHistoric:
				returnFc.isSaturated = False
				args[0]._matchesHistoric.append(returnFc.label)
				return returnFc
			else:
				returnFc.isSaturated = True
				return returnFc
		return function


	@registerHistoric
	def match(self, value, tolerance=0):
		if self.inactive: return None

		hasChildrenMatches = self._checkChildrenMatches(value, tolerance)
		if hasChildrenMatches: return hasChildrenMatches

		if self.f50.isMatch(value, tolerance):
			print("detected touch at f50")
			return self.f50
		elif self.f61x8.isMatch(value, tolerance):
			print("detected touch at f61.8")
			return self.f61x8
		elif self.f38x2.isMatch(value, tolerance):
			print("detected touch at f38.2")
			return self.f38x2
		elif self.f100.isMatch(value, tolerance):
			print("detected touch at f100")
			return self.f100
		elif self.f0.isMatch(value, tolerance):
			print("detected touch at f0")
			return self.f0
		else:
			print("not detected any touch")
			return None


	def matchRange(self, start, end):
		matches = []
		if start >= self.f50.value and end <= self.f50.value and not 50 in self._matchesHistoric:
			matches.append(50)
		if start >= self.f61x8.value and end <= self.f61x8.value and not 61.8 in self._matchesHistoric:
			matches.append(61.8)
		if start >= self.f38x2.value and end <= self.f38x2.value and not 38.2 in self._matchesHistoric:
			matches.append(38.2)
		if start >= self.f100.value and end <= self.f100.value and not 100 in self._matchesHistoric:
			matches.append(100)
		if start >= self.f0.value and end <= self.f0.value and not 0 in self._matchesHistoric:
			matches.append(0)
		return matches



class FibonacciFactory:
	@staticmethod
	def create(name, start, end, minDifference):
		fibonacci =  Fibonacci(name, start, end, minDifference)
		fibonacci.startChild = Fibonacci("start_child_1")
		fibonacci.endChild = Fibonacci("end_child_2")
		return fibonacci
		