class Fibonacci:
	def __init__(self, start, end, minDifference=0):
		self.start = start
		self.end = end
		self.minDifference = minDifference
		self.inactive = False
		self.processValues()


	def processValues(self):
		self.difference = abs(self.start - self.end)

		if self.difference < self.minDifference:
			self.inactive = True
			return
		elif self.start > self.end:
			self.inactive = False
			self.f100 = self.end + self.difference
			self.f61x8 = self.end + ((self.difference * 61.8) / 100)
			self.f50 = self.end + ((self.difference * 50) / 100)
			self.f38x2 = self.end + ((self.difference * 38.2) / 100)
			self.f0 = self.end + ((self.difference * 0) / 100)
		else:
			self.inactive = False
			self.f100 = self.end - self.difference
			self.f61x8 = self.end - ((self.difference * 61.8) / 100)
			self.f50 = self.end - ((self.difference * 50) / 100)
			self.f38x2 = self.end - ((self.difference * 38.2) / 100)
			self.f0 = self.end - ((self.difference * 0) / 100)


	def update(self, start=None, end=None):
		self.start = start or self.start
		self.end = end or self.end
		self.processValues()


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


	def show(self):
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
		print(fibo)










# 1000 | 100
# 300  |  x

# 100  | 10000
# 61.8 |   x
