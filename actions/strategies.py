from speculator import speculator
from logger import logger

def analyzerFiboZone(self, vars, actions):
	if vars.hasValidMatches and vars.isNotSaturatedZone:
		if vars.fibosMatches[0].label in ["f61x8", "f38x2"]:
			logger.log(f"speculator -> detected current fibonacci matches ({self.fibosMatches[0].label} - {self.fibosMatches[0]})")
			if (vars.hasMinMatches or vars.isInitialState) and vars.isRedCandle and vars.isUpTrend:
				self.purchase()
			elif (vars.hasMinMatches or vars.isInitialState) and vars.isGreenCandle and vars.isDownTrend:
				self.sell()
			self.createFibo(self.currentFibo.end, self.currentCandle.maxTraced)
		if self.fibosMatches[0].label in ["f50"] and 38.2 in vars.selfcurFiboMatchRange:
			logger.log(f"speculator -> detected current fibonacci matches ({self.fibosMatches[0].label} - {self.fibosMatches[0]})")
			if (vars.hasMinMatches or vars.isInitialState) and vars.isRedCandle:
				self.purchase()
			elif (vars.hasMinMatches or vars.isInitialState) and vars.isGreenCandle:
				self.sell()
			self.createFibo(self.currentFibo.end, self.currentCandle.maxTraced)


speculator.actions.create(
	name="analyzerFiboZone",
	action=analyzerFiboZone,
	constraints=[],
	exceptions=[]
)
