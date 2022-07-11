from utils.screen import Screen
from utils.time import seconds
from utils.sound import sound
from entities.graphic import Graphic
from speculator import speculator
from datetime import datetime
from configer import configer
from logger import logger
import actions.strategies
import pyautogui as ctr
import os


configer.init("config/default.json")
logger.init(folderPath="logs")
sound.folder("sounds")

graphic = Graphic()
screen = Screen()

graphic.start()

speculator.use("view", screen)
speculator.use("graphic", graphic)
speculator.use("controller", ctr)


def main(historic, price, candle, close):
	if not seconds() in [00, 31, 41, 51]: return

	os.system("clear")
	ctr.press('shift') # keep screen active

	print("registering candle..", datetime.now())
	speculator.speculate(candle=candle, price=price)

	print(candle)
	print(price)
	print(speculator.fibonaccis)

graphic.tradingWindow(main, interval=1)



# for name, val in strategies.__dict__.items():
# 	print(name, val)

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