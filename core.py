from utils import screen
from tools.fibonacci import Fibonacci
from analyzer import Analyzer
from datetime import datetime
from time import sleep
import cv2
import copy

# myFibo = Fibonacci(1000, 900, minDifference=0)
# myFibo2 = Fibonacci(900, 1000, minDifference=0)
# myFibo.show()
# myFibo2.show()
# myFibo.match(530.5, tolerance=10)

analyzer = Analyzer()

y=1055
x=287
h=550
w=25

maxPrice = 10000
price = 10000
minPrice = 10000

history = []


def updatePrice(candleType, candleMetrics):
	global maxPrice, price, minPrice

	traceCandleTop = candleMetrics["traceTop"]
	candleBody = candleMetrics["body"]
	traceCandleBottom = candleMetrics["traceBottom"]

	if candleType == 0: return
	if candleType == 1: price += candleBody
	if candleType == -1: price -= candleBody

	if price + traceCandleTop > maxPrice:
		maxPrice = price + traceCandleTop
	if price - traceCandleBottom < minPrice:
		minPrice = price - traceCandleBottom


def metricsPrice(price, candlePrice, candleMetrics, candleType):
	candlePrice = copy.deepcopy(candlePrice)
	traceCandleTop = candleMetrics["traceTop"]
	candleBody = candleMetrics["body"]
	traceCandleBottom = candleMetrics["traceBottom"]

	if candleType == 1:
		candlePrice["maxTraced"] = price + traceCandleTop
		candlePrice["start"] = price - candleBody
		candlePrice["end"] = price
		candlePrice["endTraced"] = price + traceCandleTop
		candlePrice["minTraced"] = (price - candleBody) - traceCandleBottom
	else:
		candlePrice["minTraced"] = (price + candleBody) + traceCandleTop
		candlePrice["start"] = price + candleBody
		candlePrice["end"] = price
		candlePrice["maxTraced"] = price - traceCandleBottom

	return candlePrice


def detectCandleColor(b, g, r):
	# 1 = Green | -1 = Red
	if r > 240: return -1
	if g > 180 and r < 100: return 1


def detectCandleMetrics(line, metrics):
	metrics = copy.deepcopy(metrics)

	for index in range(len(line)):
		lastPixel = (0, 0, 0) if index == 0 else line[index - 1]
		currentPixel = line[index]
		nextPixel = (0, 0, 0) if len(line) == index + 1 else line[index + 1]

		if currentPixel[0] < 50: continue # ignore empty/black pixels
		
		if metrics["body"] == 0 and currentPixel[1] != nextPixel[1]:
			metrics["traceTop"] += 1
			return metrics

		if currentPixel[1] == nextPixel[1]:
			metrics["body"] += 1
			return metrics

		if metrics["body"] > 0 and currentPixel[1] != nextPixel[1]:
			metrics["traceBottom"] += 1
			return metrics

	return metrics


def line_data(line, candle):
	candle["metrics"] = detectCandleMetrics(line, candle["metrics"])
	linePixels = []
	for (b, g, r) in line:
		candle["type"] = detectCandleColor(b, g, r) or candle["type"]
		linePixels.append((b, g, r))
	# print(linePixels)
	return linePixels


while True:
	print("registering candle..", datetime.now())

	candle = {
		"type": 0,
		"price": {
			"minTraced": 0,
			"start": 0,
			"end": 0,
			"maxTraced": 0,
		},
		"metrics": {
			"traceTop": 0,
			"body": 0,
			"traceBottom": 0,
		},
		"statistics": {
			"traceTopIsMax": 0,
			"hasTraceTop": 0,
			"traceDifference": 0,
			"hasTraceBottom": 0,
			"traceBottomIsMax": 0
		}
	}

	screenshot = screen.take_screenshot(region=(x, y, w, h))
	for line in screenshot: line_data(line, candle)

	updatePrice(candle["type"], candle["metrics"])

	traceCandleTop = candle["metrics"]["traceTop"]
	traceCandleBottom = candle["metrics"]["traceBottom"]
	traceDifference = abs(traceCandleTop - traceCandleBottom)
	traceTopIsMax = traceDifference > 10 and traceCandleTop > traceCandleBottom
	traceBottomIsMax = traceDifference > 10 and traceCandleBottom > traceCandleTop

	candle["price"] = metricsPrice(
		price=price,
		candlePrice=candle["price"],
		candleMetrics=candle["metrics"],
		candleType=candle["type"]
	)
	candle["statistics"]["traceDifference"] = traceDifference
	candle["statistics"]["hasTraceTop"] = traceCandleTop > 0
	candle["statistics"]["traceTopIsMax"] = traceTopIsMax
	candle["statistics"]["hasTraceBottom"] = traceCandleBottom > 0
	candle["statistics"]["traceBottomIsMax"] = traceBottomIsMax

	print(candle["type"])
	print(candle["metrics"])
	print(candle["statistics"])
	print(maxPrice, price, minPrice)

	analyzer.setValues(
		currentValue=price,
		maxV=maxPrice,
		minV=minPrice,
		candle=copy.deepcopy(candle)
	)

	history.insert(0, candle)
	history = history[0:2] # limiter (2 slots)

	print(history)

	# cv2.imshow("screenshot", screenshot)
	# cv2.waitKey(0)
	sleep(59.3)



# print(screenshot.getpixel((12, 205)))
# screenshot = cv2.imread("screenshot.png")
# screenshot = cv2.imread("screenshot.png")
# screenshot[y:y+h, x:x+w] = (0, 0, 255)
# croped = screenshot[y:y+h, x:x+w]
# print(list(map(lambda line: line_data(line), screenshot)))
# print(pg.locateOnScreen('green_dot.png', confidence=.6, region=(x, y, w, h)))
# cv2.imshow("screenshot", screenshot)
# cv2.waitKey(0)

# (121, 198, 20) VERDE
# (108, 100, 255) VERMELHO
# (34, 31, 30) EMPTY
