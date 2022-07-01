import pyautogui as pg
import numpy as np
import cv2

def take_screenshot(region):
	screenshot = pg.screenshot(region=region)
	screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
	return screenshot
