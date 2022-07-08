from utils.screen import Screen
from tools.time import seconds
from entities.graphic import Graphic
from speculator import Speculator
from datetime import datetime
import pyautogui as ctr
import os

# myFibo = Fibonacci("test", 10000, 1000, minDifference=300)
# print(myFibo)
# myFibo.match(6572, tolerance=30)

graphic = Graphic()
graphic.start()
screen = Screen()
speculator = Speculator()

history = []
speculator.useView(screen)
speculator.useController(ctr)

selectedCandleArea = {
	"posX": (287 * screen.width) / 900,
	"posY": (1053 * screen.height) / 1600,
	"width": (25 * screen.width) / 900,
	"height": (520 * screen.height) / 1600
}


def main(historic, price, candle, close):
	if not seconds() in [31, 41, 59]: return

	os.system("clear")

	print("registering candle..", datetime.now())
	speculator.speculate(candle=candle, price=price)

	print(candle)
	print(price)
	print(speculator.fibonaccis)


graphic.tradingWindow(main, interval=1)




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