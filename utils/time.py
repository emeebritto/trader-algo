from datetime import datetime
from time import sleep

def seconds():
	return datetime.now().time().second


def wait(testFc):
	while testFc() == False: sleep(1)