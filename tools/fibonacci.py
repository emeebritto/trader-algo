from collections import deque
from configer import configer
from logger import logger
from utils.sound import sound
from entities.resistance import Resistance


class FibonacciLine(Resistance):
	def __init__(self, parent, label, value=0):
		super().__init__(label, value)
		self.parent = parent


	def __repr__(self):
		if not self._isActive: return f"""{self.value} (matches: {self.matchesNumber}) [inactive]"""
		if self.isSaturated: return f"""{self.value} (matches: {self.matchesNumber}) [saturated]"""
		return f"""{self.value} (matches: {self.matchesNumber})"""



class Fibonacci:
	def __init__(self, name, start=0, end=0, minDifference=0):
		self.name = name
		self.start = start
		self.end = end
		self._minDifference = minDifference
		self.direction = -1 if self.start >= self.end else 1
		self._inactive = False  # fibonacci status
		self._startChild = None
		self._endChild = None
		dequeMaxLen = configer.get("fibonacci.dequeMaxLen")
		self._matchesHistoric = deque([], maxlen=dequeMaxLen)

		self.f100 = FibonacciLine(parent=self, label="f100")
		self.f61x8 = FibonacciLine(parent=self, label="f61x8")
		self.f50 = FibonacciLine(parent=self, label="f50")
		self.f38x2 = FibonacciLine(parent=self, label="f38x2")
		self.f0 = FibonacciLine(parent=self, label="f0")

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
	def inactive(self):
		return self._inactive


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


	@inactive.setter
	def inactive(self, val):
		self._inactive = val
		if not self._inactive:
			sound.play("notice.mp3")
			logger.log([
				f"{self.name} -> Fibonacci is active now",
				f"{self.name} -> Fibonacci heigth is {self.difference}"
			])


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


	def validateZoneWith(self, values):
		for zone in [self.f100, self.f61x8, self.f50, self.f38x2, self.f0]:
			zone.validateWith(values)


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
		logger.log(f"updating Fibonacci ({self.name} - From {start} to {end}))")
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
				args[0]._matchesHistoric.append(None)
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
			print(f"{self.name} -> detected touch at f50")
			logger.log(f"{self.name} -> detected touch at f50")
			return self.f50
		elif self.f61x8.isMatch(value, tolerance):
			print(f"{self.name} -> detected touch at f61.8")
			logger.log(f"{self.name} -> detected touch at f61.8")
			return self.f61x8
		elif self.f38x2.isMatch(value, tolerance):
			print(f"{self.name} -> detected touch at f38.2")
			logger.log(f"{self.name} -> detected touch at f38.2")
			return self.f38x2
		elif self.f100.isMatch(value, tolerance):
			print(f"{self.name} -> detected touch at f100")
			logger.log(f"{self.name} -> detected touch at f100")
			return self.f100
		elif self.f0.isMatch(value, tolerance):
			print(f"{self.name} -> detected touch at f0")
			logger.log(f"{self.name} -> detected touch at f0")
			return self.f0
		else:
			print(f"{self.name} -> not detected any touch")
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

		if len(matches): logger.log(f"{self.name} -> detected match range {matches}")
		return matches



class FibonacciFactory:
	@staticmethod
	def create(name, start, end, minDifference, validateWith):
		logger.log(f"creating Fibonacci ({name} - From {start} to {end})")
		fibonacci = Fibonacci(name, start, end, minDifference)
		fibonacci.validateZoneWith(validateWith)
		fibonacci.startChild = Fibonacci("start_child_1", minDifference=minDifference)
		fibonacci.endChild = Fibonacci("end_child_2", minDifference=minDifference)
		return fibonacci
