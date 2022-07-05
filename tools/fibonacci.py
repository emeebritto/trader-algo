class Fibonacci:
	def __init__(self, name, start=0, end=0, minDifference=0):
		self.name = name
		self.start = start
		self.end = end
		self._minDifference = minDifference
		self.direction = -1 if self.start >= self.end else 1
		self.inactive = False
		self._startChild = None
		self._endChild = None
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
			"100": self.f100,
			"61.8": self.f61x8,
			"50": self.f50,
			"38.2": self.f38x2,
			"0": self.f0
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
			start=self.f100,
			end=self.f61x8,
			minDifference=self._minDifference
		)
		self._startChild = child


	@endChild.setter
	def endChild(self, child):
		child.update(
			start=self.f38x2,
			end=self.f0,
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
			self.f100 = self.end + self.difference
			self.f61x8 = self.end + ((self.difference * 61.8) / 100)
			self.f50 = self.end + ((self.difference * 50) / 100)
			self.f38x2 = self.end + ((self.difference * 38.2) / 100)
			self.f0 = self.end + ((self.difference * 0) / 100)
		else:
			self.f100 = self.end - self.difference
			self.f61x8 = self.end - ((self.difference * 61.8) / 100)
			self.f50 = self.end - ((self.difference * 50) / 100)
			self.f38x2 = self.end - ((self.difference * 38.2) / 100)
			self.f0 = self.end - ((self.difference * 0) / 100)


	def updateChildren(self):
		if self._startChild: self._startChild.update(start=self.f100, end=self.f61x8)
		if self._endChild: self._endChild.update(start=self.f38x2, end=self.f0)


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
			if value > self.f100:
				# out of range on top (f100)
				return (True, False)
			elif value < self.f0:
				# out of range on bottom (f0)
				return (False, True)
		else:
			if value < self.f100:
				# out of range on bottom (f100)
				return (True, False)
			elif value > self.f0:
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


	def match(self, value, tolerance=0):
		if self.inactive: return None

		hasChildrenMatches = self._checkChildrenMatches(value, tolerance)
		if hasChildrenMatches: return hasChildrenMatches

		if abs(value - self.f50) <= tolerance:
			print("detected touch at f50")
			return 50
		elif abs(value - self.f61x8) <= tolerance:
			print("detected touch at f61.8")
			return 61.8
		elif abs(value - self.f38x2) <= tolerance:
			print("detected touch at f38.2")
			return 38.2
		elif abs(value - self.f100) <= tolerance:
			print("detected touch at f100")
			return 100
		elif abs(value - self.f0) <= tolerance:
			print("detected touch at f0")
			return 0
		else:
			print("not detected any touch")
			return None


class FibonacciFactory:
	@staticmethod
	def create(name, start, end, minDifference):
		fibonacci =  Fibonacci(name, start, end, minDifference)
		fibonacci.startChild = Fibonacci("start_child_1")
		fibonacci.endChild = Fibonacci("end_child_2")
		return fibonacci
		