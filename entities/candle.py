class Candle:
	def __init__(self, entry):
		self.entry = entry or 0
		self.exit = self.entry
		self._type = 0
		self.body = 0
		self._minTraced = self.entry
		self._maxTraced = self.exit
		self._maxValue = self.entry
		self._minValue = self.entry
		self._defineCandleType()
		self._defineBodyLength()
		self._defineCandleTraces()
		self._defineStatistics()


	def __repr__(self):
		return f"""
  type: {self._type}
  entryTraceIsMax: {self.entryTraceIsMax}
  hasEntryTrace: {self.hasEntryTrace}
  traceDifference: {self.traceDifference}
  hasExitTrace: {self.hasExitTrace}
  exitTraceIsMax: {self.exitTraceIsMax}
  > prices =======================
   - minTraced: {self._minTraced}
   - entry: {self.entry}
   - exit: {self.exit}
   - maxTraced: {self._maxTraced}
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
			"minTraced": self._minTraced,
			"maxTraced": self._maxTraced
		}


	@property
	def maxValue(self):
		return self._maxValue


	@property
	def minValue(self):
		return self._minValue


	@property
	def maxTraced(self):
		return self._maxTraced


	@property
	def minTraced(self):
		return self._minTraced


	def update(self, value):
		self.exit = value
		if value > self._maxValue:
			self._maxValue = value
		if value < self._minValue:
			self._minValue = value

		self._defineCandleType()
		self._defineBodyLength()
		self._defineCandleTraces()
		self._defineStatistics()


	def _defineCandleType(self):
		if self.entry < self.exit:
			self._type = 1
		elif self.entry == self.exit:
			self._type = 0
		else:
			self._type = -1


	def _defineBodyLength(self):
		self.body = abs(self.entry - self.exit)


	def _defineCandleTraces(self):
		if self._type == 1:
			self._maxTraced = self._maxValue
			self._minTraced = self._minValue
		else:
			self._maxTraced = self._minValue
			self._minTraced = self._maxValue

		self.traceLength = {
			"entry": abs(self.entry - self._minTraced),
			"exit": abs(self.exit - self._maxTraced)
		}


	def _defineStatistics(self):
		self.hasEntryTrace = self.traceLength["entry"] > 0
		self.hasExitTrace = self.traceLength["exit"] > 0
		self.traceDifference = abs(self.traceLength["entry"] - self.traceLength["exit"]) 
		self.entryTraceIsMax = self.traceLength["entry"] > self.traceLength["exit"]
		self.exitTraceIsMax = self.traceLength["entry"] < self.traceLength["exit"]
