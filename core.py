from utils import screen
from datetime import datetime
from time import sleep

y=1100
x=287
h=450
w=25

traceCandleTop=0
candleBody=0
red=0
green=0
gray=0
traceCandleBottom=0

def cleanData():
	global red, green, gray, traceCandleTop, candleBody, traceCandleBottom
	traceCandleTop=0
	candleBody=0
	red=0
	green=0
	gray=0
	traceCandleBottom=0 

def detectCandleColor(b, g, r):
	global red, green, gray

	if r > 240: red = 1
	if g > 180 and r < 100: green = 1
	gray = 1 if red == 0 and green == 0 else 0


def detectCandleTrace(line):
	global traceCandleTop, candleBody, traceCandleBottom

	for index, (b, g, r) in enumerate(line):
		lastPixel = (0, 0, 0) if index == 0 else line[index - 1]
		currentPixel = (b, g, r)
		nextPixel = (0, 0, 0) if len(line) == index + 1 else line[index + 1]

		if currentPixel[0] < 50: continue # ignore empty pixels

		if currentPixel[1] == nextPixel[1]:
			candleBody += 1
			return

		if candleBody == 0 and currentPixel[1] != nextPixel[1]:
			traceCandleTop += 1
			return

		if candleBody > 0 and currentPixel[1] != nextPixel[1]:
			traceCandleBottom += 1
			return


def line_data(line):
	linePixels = []
	detectCandleTrace(line)
	for i, (b, g, r) in enumerate(line):
		detectCandleColor(b, g, r)
		linePixels.append((b, g, r))
	# print(linePixels)
	return linePixels


while True:
	print("registering candle..", datetime.now())
	screenshot = screen.take_screenshot(region=(x, y, w, h))
	for line in screenshot: line_data(line)

	print(traceCandleTop, candleBody, traceCandleBottom)

	print(red, green, gray)
	print(traceCandleTop > 0, traceCandleBottom > 0)

	cleanData()
	sleep(59)


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
