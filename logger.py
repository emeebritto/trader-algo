from datetime import datetime, date
import os


class Logger:
	def __init__(self):
		super(Logger, self).__init__()
		self.folderPath = ""


	def init(self, folderPath):
		self.folderPath = folderPath
		if not os.path.exists(f"{self.folderPath}/log.txt"):
			with open(f"{self.folderPath}/{date.today()}.txt", 'a') as logFile:
				logFile.write(f"\n[{datetime.now()}]: initialized log file.\n")


	def log(self, msgs):
		if not self.folderPath: raise AttributeError("folder path was not provided")
		if type(msgs) == list:
			for msg in msgs: self._createNewLine(msg)
		else: self._createNewLine(msgs)


	def _createNewLine(self, lineContent):
		with open(f"{self.folderPath}/{date.today()}.txt", 'a') as logFile:
			logFile.write(f"[{datetime.now()}]: {lineContent}\n")


logger = Logger()
