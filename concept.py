from speculator import Speculator

speculator = Speculator()


def createFibonacci(self):
	pass


def registerPrice(self):
	pass


def deleteResistence(self):
	pass


def closeTrading(self):
	pass


def detectPrice(self, action):
	# logic > ... <
	action.newFibonnaci()
	# or ..
	action.registerPrice()
	action.deleteResistence()


def ifTrue(self):
	pass


def invalidFormatPrice(self, functionArgs):
	return True # cancel trigger execution


def syntaxError(self, error, action, functionArgs):
	print("error detected")
	print(error)
	if error: action.closeTrading()




speculator.trigger(
	name="analyzerTrading",
	function=detectPrice,
	constraints=["invalidFormatPrice"],
	exceptions=["syntaxError"]
)
speculator.action(
	name="newFibonnaci",
	function=createFibonacci,
	constraints=["invalidFormatPrice"],
	exceptions=["syntaxError"]
)
speculator.setVar("name", "jpeg")
speculator.action("registerPrice", registerPrice)
speculator.action("deleteResistence", deleteResistence)
speculator.allowance("ifTrue", ifTrue)
speculator.constraints("invalidFormatPrice", invalidFormatPrice)
speculator.exceptions("syntaxError", syntaxError)
