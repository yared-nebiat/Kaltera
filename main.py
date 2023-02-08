from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.core.audio import SoundLoader
import random as r
import pickle

'''
# Resets the score
with open("total_score.pickle", "wb") as score:
	pickle.dump("0", score)
'''

bg_music = SoundLoader.load('Background music.mp3')
correct_sound = SoundLoader.load('Right.wav')
incorrect_sound = SoundLoader.load('Wrong.wav')

gobez_sound = SoundLoader.load('Gobez.wav')
andegna_sound = SoundLoader.load('Andegna.wav')
jegna_sound = SoundLoader.load('Jegna.wav')
anbessa_sound = SoundLoader.load('Anbessa.wav')

celebrate_sounds = ['gobez_sound', 'andegna_sound', 'jegna_sound', 'anbessa_sound']
sound_name = {'gobez_sound': gobez_sound, 'andegna_sound': andegna_sound, 'jegna_sound': jegna_sound, 'anbessa_sound': anbessa_sound}

bg_music.play()
bg_music.loop = True
bg_music.volume = 0.4
correct_sound.volume = 0.5
incorrect_sound.volume = 0.6
mute = False


Config.set('graphics', 'resizable', True)


class WindowManager(ScreenManager):
	pass


def total():
	try:
		with open("total_score.pickle", "rb") as total_score:
			my_score = pickle.load(total_score)
			return my_score
	except IOError as err:
		print("Error:", err)


class MainWindow(Screen):
	soundpic = ObjectProperty(None)
	def audio(self):
		global mute
		if mute == False:
			bg_music.volume = 0
			correct_sound.volume = 0
			incorrect_sound.volume = 0
			gobez_sound.volume = 0
			andegna_sound.volume = 0 
			jegna_sound.volume = 0
			anbessa_sound.volume = 0 
			mute = True
			self.soundpic.source = "mute.png"
		else:
			bg_music.volume = 0.4
			correct_sound.volume = 0.5
			incorrect_sound.volume = 0.6
			gobez_sound.volume = 0.5
			andegna_sound.volume = 0.5
			jegna_sound.volume = 0.5
			anbessa_sound.volume = 0.5 
			mute = False
			self.soundpic.source = "volume.png"


class InstructionWindow(Screen):
	pass


class GameWindow(Screen):
	def __init__(self, points=total(), **kwargs):
		# The line below is used to initialize the class using the parent class.
		# The lines below that are my modifications specific to this class.
		super(GameWindow, self).__init__(**kwargs)
		self.points = points
		self.letters = list("ቀወረተየአሰደፈገሀጀከለዘበነመጨቸሸጠፀ")
		r.shuffle(self.letters)
		self.choices = self.letters
		self.correct_words = []

		self.tl_initial = self.choices[0]
		self.tm_initial = self.choices[1]
		self.tr_initial = self.choices[2]

		self.ml_initial = self.choices[3]
		self.center_initial = self.choices[4]
		self.mr_initial = self.choices[5]

		self.bl_initial = self.choices[6]
		self.bm_initial = self.choices[7]
		self.br_initial = self.choices[8]


	score = ObjectProperty(None)
	word1 = ObjectProperty(None)
	word2 = ObjectProperty(None)
	word3 = ObjectProperty(None)
	firstline = ObjectProperty(None)
	secondline = ObjectProperty(None)
	thirdline = ObjectProperty(None)

	tl = ObjectProperty(None)
	tm = ObjectProperty(None)
	tr = ObjectProperty(None)
	ml = ObjectProperty(None)
	center = ObjectProperty(None)
	mr = ObjectProperty(None)
	bl = ObjectProperty(None)
	bm = ObjectProperty(None)
	br = ObjectProperty(None)

	# tells the program which line is in use
	line = 1
	active_line = word1

	def buttons(self):
		self.tl.text = self.choices[0]
		self.tm.text = self.choices[1]
		self.tr.text = self.choices[2]

		self.ml.text = self.choices[3]
		self.center.text = self.choices[4]
		self.mr.text = self.choices[5]

		self.bl.text = self.choices[6]
		self.bm.text = self.choices[7]
		self.br.text = self.choices[8]

	def tlpressed(self):
		if len(self.active_line.text) < 9:
			self.active_line.text += self.choices[0]

	def tmpressed(self):
		if len(self.active_line.text) < 9:
			self.active_line.text += self.choices[1]


	def trpressed(self):
		if len(self.active_line.text) < 9:
			self.active_line.text += self.choices[2]


	def mlpressed(self):
		if len(self.active_line.text) < 9:
			self.active_line.text += self.choices[3]


	def centerpressed(self):
		if len(self.active_line.text) < 9:
			self.active_line.text += self.choices[4]

	def mrpressed(self):
		if len(self.active_line.text) < 9:
			self.active_line.text += self.choices[5]


	def blpressed(self):
		if len(self.active_line.text) < 9:
			self.active_line.text += self.choices[6]

	def bmpressed(self):
		if len(self.active_line.text) < 9:
			self.active_line.text += self.choices[7]


	def brpressed(self):
		if len(self.active_line.text) < 9:
			self.active_line.text += self.choices[8]

	def backspace(self):
		self.active_line.text = self.active_line.text[:len(self.active_line.text)-1]

	def confirm(self):
		try:
			with open("Words.txt", encoding="utf8") as data:
				if self.active_line.text not in self.correct_words:
					for words in data:
						if words.strip() == self.active_line.text:
							self.correct_words.append(self.active_line.text)
							self.correct()
							if self.line == 4:
								self.congrats()
							break
					else:
						self.incorrect()
				else:
					self.incorrect()
		# Catches any errors in openning the file     
		except IOError as err:
			print("Error:", err)

	def correct(self):
		correct_sound.play()
		self.points = str(int(self.points) + len(self.active_line.text))
		self.score.text = self.points
		if self.line == 1:
			self.firstline.source = "greenline.png"
		elif self.line == 2:
			self.secondline.source = "greenline.png"
		elif self.line == 3:
			self.thirdline.source = "greenline.png"
		try:
			with open("total_score.pickle", "wb") as total_score:
				pickle.dump(self.points, total_score)
		except IOError as err:
			print("Error:", err)

		self.line += 1
		if self.line == 2:
			self.active_line = self.word2
		elif self.line == 3:
			self.active_line = self.word3

	def incorrect(self):
		incorrect_sound.play()
		if self.line == 1:
			self.firstline.source = "redline.png"
		elif self.line == 2:
			self.secondline.source = "redline.png"
		elif self.line == 3:
			self.thirdline.source = "redline.png"

		self.active_line.text = ''

	def congrats(self):
		# reinitializes everything I need for the game to continue
		self.manager.current = "advance"
		self.__init__(self.points)
		self.line = 1
		self.active_line = self.word1

		self.buttons()
		# calls my_callback function when sound is complete
		random_sound = r.choice(celebrate_sounds)
		sound_name[random_sound].bind(on_stop=self.my_callback)

		AdvanceWindow().celebration(random_sound)
		sound_name[random_sound].play()


	def my_callback(self, *args):
		self.manager.current = "game"


class AdvanceWindow(Screen):

	congratulate = ObjectProperty(None)

	def celebration(self, random_sound):
		# I need to find a way to call this function
		sound_to_text = {'gobez_sound': "Gobez", 'andegna_sound': "Andegna", 'jegna_sound': "Jegna", 'anbessa_sound': "Anbessa"}
		self.congratulate.text = sound_to_text[random_sound]



kv = Builder.load_file("design.kv")

class ቃልተራApp(App):
	def build(self):
		return kv

if __name__=='__main__':
	ቃልተራApp().run()
