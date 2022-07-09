import json

class Configer:
	def __init__(self):
		super(Configer, self).__init__()
		self._config = None


	def init(self, configPATH):
		with open(configPATH, "r") as configFile:
			data = json.load(configFile)
			self._config = data


	def get(self, propertyPath):
		propertyPath = propertyPath.split(".")
		currentProperty = self._config
		for prop in propertyPath:
			currentProperty = currentProperty.get(prop)
		return currentProperty


configer = Configer()