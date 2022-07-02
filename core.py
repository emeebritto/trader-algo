from utils import screen
from tools.fibonacci import Fibonacci
from entities.candle import Candle
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
h=540
w=25

maxPrice = 10000
price = 10000
minPrice = 10000

history = []


def detectCandleColor(b, g, r):
	isRed = r > 240
	isGreen = g > 180 and r < 100
	if isRed: return -1
	if isGreen: return 1


def line_data(line, candle):
	linePixels = []
	for (b, g, r) in line:
		candle.cType = detectCandleColor(b, g, r) or candle.cType
		linePixels.append((b, g, r))
	print(linePixels)

	# candle.cType = 1
	# candle.exitTraceLength = 6
	# candle.bodyLength = 100
	# candle.entryTraceLength = 20


	for index in range(len(line)):
		lastPixelRGB = (0, 0, 0) if index == 0 else line[index - 1]
		currentPixelRGB = line[index]
		nextPixelRGB = (0, 0, 0) if len(line) == index + 1 else line[index + 1]

		lastPixel = {
			"isGray": lastPixelRGB[0] < 50,
			"isGreen": lastPixelRGB[1] > 180 and lastPixelRGB[2] < 100,
			"isRed": lastPixelRGB[2] > 240
		}

		currentPixel = {
			"isGray": currentPixelRGB[0] < 50,
			"isGreen": currentPixelRGB[1] > 180 and currentPixelRGB[2] < 100,
			"isRed": currentPixelRGB[2] > 240
		}

		nextPixel = {
			"isGray": nextPixelRGB[0] < 50,
			"isGreen": nextPixelRGB[1] > 180 and nextPixelRGB[2] < 100,
			"isRed": nextPixelRGB[2] > 240
		}

		currentPixelIsCandle = currentPixel["isGreen"] or currentPixel["isRed"]
		nextPixelIsCandle = nextPixel["isGreen"] or nextPixel["isRed"]
		isCandleTrace = lastPixel["isGray"] and currentPixelIsCandle and nextPixel["isGray"]
		isCandleBody = currentPixelIsCandle and nextPixelIsCandle

		if currentPixelRGB[0] < 50: continue # ignore empty/black pixels
		
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
	print("registering candle..", datetime.now())
	candle = Candle()

	screenshot = screen.take_screenshot(region=(x, y, w, h))
	for line in screenshot: line_data(line, candle)
	print(candle.metrics)

	entryTraceLength = candle.entryTraceLength
	exitTraceLength = candle.exitTraceLength

	if candle.cType == 1: price += candle.body
	if candle.cType == -1: price -= candle.body

	candle.processPrices(exitPrice=price)

	if candle.maxValue > maxPrice:
		maxPrice = candle.maxValue
	if candle.minValue < minPrice:
		minPrice = candle.minValue


	print(candle)
	print(maxPrice, price, minPrice)

	analyzer.setValues(
		currentValue=price,
		maxV=maxPrice,
		minV=minPrice,
		candle=candle
	)

	history.insert(0, candle)
	history = history[0:2] # limiter (2 slots)

	# print(history)

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