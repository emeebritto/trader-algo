class Fibonacci:
	def __init__(self, name, start, end, minDifference=0):
		self.name = name
		self.start = start
		self.end = end
		self.minDifference = minDifference
		self.direction = -1 if self.start >= self.end else 1
		self.inactive = False
		self.processValues()


	def __repr__(self):
		return f"""
  name: {self.name}
  inactive: {self.inactive}
  difference: {self.difference} (require: {self.minDifference})
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
		if self.difference < self.minDifference:
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


	def update(self, start=None, end=None):
		self.start = start or self.start
		self.end = end or self.end
		self.direction = -1 if self.start >= self.end else 1
		self.processValues()


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


	def match(self, value, tolerance=0):
		if self.inactive: return None

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
