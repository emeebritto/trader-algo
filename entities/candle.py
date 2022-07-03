class Candle:
	def __init__(self, **kwargs):
		self.entry = kwargs.get("entry") or 0
		self.exit = kwargs.get("exit") or self.entry
		self._type = kwargs.get("type") or self.detectType()
		self.minTraced = kwargs.get("minTraced") or self.entry
		self.maxTraced = kwargs.get("maxTraced") or self.exit

		self._maxValue = self.maxTraced if self.maxTraced > self.minTraced else self.minTraced
		self._minValue = self.minTraced if self.maxTraced > self.minTraced else self.maxTraced

		self.body = abs(self.entry - self.exit)
		self.processTracesLength()
		self.processTraces()


	def __repr__(self):
		return f"""
  type: {self._type}
  entryTraceIsMax: {self.entryTraceIsMax}
  hasEntryTrace: {self.hasEntryTrace}
  traceDifference: {self.traceDifference}
  hasExitTrace: {self.hasExitTrace}
  exitTraceIsMax: {self.exitTraceIsMax}
  > prices =======================
   - minTraced: {self.minTraced}
   - entry: {self.entry}
   - exit: {self.exit}
   - maxTraced: {self.maxTraced}
  > metrics ======================
   - entryTraceLength: {self.traceLength["entry"]}
   - body: {self.body}
   - exitTraceLength: {self.traceLength["exit"]}
"""


	@property
	def cType(self):
		return self._type


	@property
	def metrics(self):
		return {
			"entryTraceLength": self.traceLength["entry"],
			"exitTraceLength": self.traceLength["exit"],
			"body": self.body
		}


	@property
	def prices(self):
		return {
			"entry": self.entry,
			"exit": self.exit,
			"minTraced": self.minTraced,
			"maxTraced": self.maxTraced
		}


	@property
	def maxValue(self):
		return self._maxValue


	@property
	def minValue(self):
		return self._minValue


	@property
	def entryTraceLength(self):
		return self.traceLength["entry"]


	@property
	def exitTraceLength(self):
		return self.traceLength["exit"]


	@property
	def bodyLength(self):
		return self.body


	@entryTraceLength.setter
	def entryTraceLength(self, val):
		self.traceLength["entry"] = val
		self.processTraces()


	@exitTraceLength.setter
	def exitTraceLength(self, val):
		self.traceLength["exit"] = val
		self.processTraces()


	@bodyLength.setter
	def bodyLength(self, val):
		self.body = val


	@cType.setter
	def cType(self, val):
		if val in [-1, 0, 1]:
			self._type = val


	def processTracesLength(self):
		self.traceLength = {
			"entry": abs(self.entry - self.minTraced),
			"exit": abs(self.exit - self.maxTraced)
		}


	def processTraces(self):
		self.hasEntryTrace = self.traceLength["entry"] > 2
		self.hasExitTrace = self.traceLength["exit"] > 2

		self.traceDifference = abs(self.traceLength["entry"] - self.traceLength["exit"])
		entryTraceIsMax = self.traceLength["entry"] > self.traceLength["exit"]
		exitTraceIsMax = self.traceLength["entry"] < self.traceLength["exit"]
		isValidDifference = self.traceDifference > 5
		self.entryTraceIsMax = isValidDifference and entryTraceIsMax
		self.exitTraceIsMax = isValidDifference and exitTraceIsMax		


	def setType(self, cType):
		if cType in [-1, 0, 1]:
			self._type = cType


	def detectType(self):
		if self.entry > self.exit:
			return 1
		elif self.exit > self.entry:
			return -1
		else:
			return 0


	def processPrices(self, exitPrice):
		entryTraceLength = self.traceLength["entry"]
		exitTraceLength = self.traceLength["exit"]

		if self._type == 1:
			self.maxTraced = exitPrice + exitTraceLength
			self.entry = exitPrice - self.body
			self.exit = exitPrice
			self.minTraced = (exitPrice - self.body) - entryTraceLength
		else:
			self.minTraced = (exitPrice + self.body) + entryTraceLength
			self.entry = exitPrice if self._type == 0 else (exitPrice + self.body)
			self.exit = exitPrice
			self.maxTraced = exitPrice - exitTraceLength

		self.processTracesLength()
		self.processTraces()
		self._maxValue = self.maxTraced if self.maxTraced > self.minTraced else self.minTraced
		self._minValue = self.minTraced if self.maxTraced > self.minTraced else self.maxTraced


	def setMetrics(self, **kwargs):
		self.traceLength["entry"] = kwargs.get("entryTraceLength") or self.traceLength["entry"]
		self.traceLength["exit"] = kwargs.get("exitTraceLength") or self.traceLength["exit"]
		self.body = kwargs.get("bodyLength") or self.body


	def setPrices(self, **kwargs):
		self.entry = kwargs.get("entry") or self.entry
		self.exit = kwargs.get("exit") or self.exit
		self.minTraced = kwargs.get("minTraced") or self.minTraced
		self.maxTraced = kwargs.get("maxTraced") or self.maxTraced
