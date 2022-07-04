from utils.screen import Screen
from tools.time import seconds
from entities.candle import Candle
from entities.price import Price
from speculator import Speculator
from datetime import datetime
from time import sleep
import os
import copy

# myFibo = Fibonacci("test", 10000, 1000, minDifference=300)
# print(myFibo)
# myFibo.match(6572, tolerance=30)

screen = Screen()
speculator = Speculator()
price = Price(10000)

history = []
speculator.useView(screen)

selectedCandleArea = {
	"posX": (287 * screen.width) / 900,
	"posY": (1053 * screen.height) / 1600,
	"width": (25 * screen.width) / 900,
	"height": (520 * screen.height) / 1600
}


while True:
	print("waiting next candle...")
	while seconds() != 00: sleep(1)

	os.system("clear")

	print("registering candle..", datetime.now())
	screenshot = speculator.readView(region=selectedCandleArea)
	candle = speculator.analyzeCandle(screenshot)

	if candle.cType == 1: price.current += candle.body
	if candle.cType == -1: price.current -= candle.body

	candle.processPrices(exitPrice=price.current)

	price.maxValue = candle.maxValue
	price.minValue = candle.minValue

	print(candle)
	print(price)

	speculator.speculate(candle=candle, price=price)

	print(speculator.fibonaccis)

	history.insert(0, candle)
	history = history[0:2] # limiter (2 slots)

	# print(history)




# print(screenshot.getpixel((12, 205)))
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
# candle.entryTraceLength += 20
# candle.bodyLength = 100
# candle.exitTraceLength += 6