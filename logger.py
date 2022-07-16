from datetime import datetime, date
from services.nexa import nexa
import os


class Logger:
	def __init__(self):
		super(Logger, self).__init__()
		self.folderPath = "logs"


	def init(self, folderPath="logs"):
		self.folderPath = folderPath
		if not os.path.exists(f"{self.folderPath}/log.txt"):
			with open(f"{self.folderPath}/{date.today()}.txt", 'a') as logFile:
				logFile.write(f"\n[{datetime.now()}]: initialized log file.\n")


	def log(self, msgs):
		if not self.folderPath: raise AttributeError("folder path was not provided")
		if type(msgs) == list:
			for msg in msgs: self._createLog(msg)
		else: self._createLog(msgs)


	def _createLog(self, msg):
		self._createNewLine(msg)
		nexa.send_to_author(f"[log]: {msg}")


	def _createNewLine(self, lineContent):
		with open(f"{self.folderPath}/{date.today()}.txt", 'a') as logFile:
			logFile.write(f"[{datetime.now()}]: {lineContent}\n")


logger = Logger()
