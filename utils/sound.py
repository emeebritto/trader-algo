from playsound import playsound
import threading


class Sound:
	def __init__(self):
		super(Sound, self).__init__()
		self._folderPath = ""


	def folder(self, folderPath):
		self._folderPath = f"{folderPath}/" if folderPath else ""


	def play(self, soundName):
		soundThr = threading.Thread(
			target=self._playsound,
			args=(),
			kwargs={"soundName": soundName}
		)
		soundThr.start()


	def _playsound(self, soundName):
		playsound(self._folderPath + soundName)


sound = Sound()
