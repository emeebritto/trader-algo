from utils import screen
from tools.fibonacci import Fibonacci
from tools.time import seconds
from entities.candle import Candle
from entities.price import Price
from analyzer import Analyzer
from datetime import datetime
from time import sleep
import cv2
import copy

# myFibo = Fibonacci("test", 10000, 1000, minDifference=300)
# print(myFibo)
# myFibo.match(6572, tolerance=30)

analyzer = Analyzer()

y=1029
x=287
h=520
w=25

price = Price(10000)
history = []


def detectCandleColor(b, g, r):
	isRed = r > 240
	isGreen = g > 180 and r < 100
	if isRed: return -1
	if isGreen: return 1


def line_data(line, candle):
	# linePixels = []
	for (b, g, r) in line:
		candle.cType = detectCandleColor(b, g, r) or candle.cType
		# linePixels.append((b, g, r))
	# print(linePixels)

	for index in range(len(line)):
		lastPixelBGR = (0, 0, 0) if index == 0 else line[index - 1]
		currentPixelBGR = line[index]
		nextPixelBGR = (0, 0, 0) if len(line) == index + 1 else line[index + 1]

		lastPixel = {
			"isGray": lastPixelBGR[0] < 50 and lastPixelBGR[1] < 50,
			"isGreen": lastPixelBGR[1] > 180 and lastPixelBGR[2] < 100,
			"isRed": lastPixelBGR[2] > 240 and lastPixelBGR[1] < 130
		}

		currentPixel = {
			"isGray": currentPixelBGR[0] < 50 and currentPixelBGR[1] < 50,
			"isGreen": currentPixelBGR[1] > 180 and currentPixelBGR[2] < 100,
			"isRed": currentPixelBGR[2] > 240 and currentPixelBGR[1] < 130
		}

		nextPixel = {
			"isGray": nextPixelBGR[0] < 50 and nextPixelBGR[1] < 50,
			"isGreen": nextPixelBGR[1] > 180 and nextPixelBGR[2] < 100,
			"isRed": nextPixelBGR[2] > 240 and nextPixelBGR[1] < 130
		}

		currentPixelIsCandle = currentPixel["isGreen"] or currentPixel["isRed"]
		nextPixelIsCandle = nextPixel["isGreen"] or nextPixel["isRed"]
		isCandleTrace = lastPixel["isGray"] and currentPixelIsCandle and nextPixel["isGray"]
		isCandleBody = currentPixelIsCandle and nextPixelIsCandle

		if currentPixel["isGray"]: continue # ignore empty/black pixels

		# NOTE:  VOCê está na branch "unstable"
		
		if candle.cType == 1:
			if candle.bodyLength == 0 and isCandleTrace:
				candle.exitTraceLength += 1
				break

			if isCandleBody:
				candle.bodyLength += 1
				break

			if candle.bodyLength > 0 and isCandleTrace:
				candle.entryTraceLength += 1
				break
		else:
			if candle.bodyLength == 0 and isCandleTrace:
				candle.entryTraceLength += 1
				break

			if isCandleBody and candle.cType == -1:
				candle.bodyLength += 1
				break

			if candle.bodyLength > 0 and isCandleTrace:
				candle.exitTraceLength += 1
				break

	# return linePixels


while True:
	print("waiting next candle...")
	while seconds() != 00: sleep(1)

	print("registering candle..", datetime.now())
	candle = Candle()

	screenshot = screen.take_screenshot(region=(x, y, w, h))
	for line in screenshot: line_data(line, candle)

	entryTraceLength = candle.entryTraceLength
	exitTraceLength = candle.exitTraceLength

	if candle.cType == 1: price.current += candle.body
	if candle.cType == -1: price.current -= candle.body

	candle.processPrices(exitPrice=price.current)

	price.maxValue = candle.maxValue
	price.minValue = candle.minValue

	print(candle)
	print(price)

	analyzer.setValues(price=price, candle=candle)

	print(analyzer.fibonaccis)

	history.insert(0, candle)
	history = history[0:2] # limiter (2 slots)

	# print(history)

	# cv2.imshow("screenshot", screenshot)
	# cv2.waitKey(0)



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

# print("exitTraceLengthPOSITIVO", exitTraceLengthPOSITIVO)
# print("exitTraceLengthNEGATIVE", exitTraceLengthNEGATIVE)
# print("entryTraceLengthPOSITIVO", entryTraceLengthPOSITIVO)
# print("entryTraceLengthNEGATIVO", entryTraceLengthNEGATIVO)
# print(candle.metrics)

# candle.cType = 1
# print(candle)
# candle.entryTraceLength += 20
# candle.bodyLength = 100
# candle.exitTraceLength += 6
# candle.exitTraceLength += 1