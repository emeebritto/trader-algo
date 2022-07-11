from speculator import Actions


def analyzerFiboZone(owner, vars, actions):
	if vars.hasValidMatches and vars.isNotSaturatedZone:
		if vars.fibosMatches[0].label in ["f61x8", "f38x2"]:
			# logger.log(f"speculator -> detected current fibonacci matches ({owner.fibosMatches[0].label} - {owner.fibosMatches[0]})")
			if (vars.hasMinMatches or vars.isInitialState) and vars.isRedCandle and vars.isUpTrend:
				owner.purchase()
			elif (vars.hasMinMatches or vars.isInitialState) and vars.isGreenCandle and vars.isDownTrend:
				owner.sell()
			owner.createFibo(owner.currentFibo.end, owner.currentCandle.maxTraced)
		if owner.fibosMatches[0].label in ["f50"] and 38.2 in vars.ownercurFiboMatchRange:
			# logger.log(f"speculator -> detected current fibonacci matches ({owner.fibosMatches[0].label} - {owner.fibosMatches[0]})")
			if (vars.hasMinMatches or vars.isInitialState) and vars.isRedCandle:
				owner.purchase()
			elif (vars.hasMinMatches or vars.isInitialState) and vars.isGreenCandle:
				owner.sell()
			owner.createFibo(owner.currentFibo.end, owner.currentCandle.maxTraced)


strategies = Actions()

strategies.create(
	name="analyzerFiboZone",
	action=analyzerFiboZone,
	constraints=[],
	exceptions=[]
)
