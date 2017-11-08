from core import *
from kivy.core.window import Window
from kivy.clock import Clock as kivyClock
from kivy.uix.label import Label
from kivy.graphics.instructions import CanvasBase
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.core.image import Image

from random import random, randint
import numpy as np



class MainWidget1(BaseWidget) :
	def __init__(self):
		super(MainWidget1, self).__init__()
		
		scaling = 1.1
		horSize = 330 * scaling
		verSize = 180 * scaling
		rightPad = (Window.width - horSize*3) / 2
		topPad = Window.height - verSize*2 - 50
		print topPad
		cust = ["CustomerInfo.png", (Window.width-rightPad-horSize*3,Window.height-topPad-verSize*2), (horSize,verSize*2)]
		drug = ["DrugInformation.png", (Window.width-rightPad-horSize*2,Window.height-topPad-verSize), (horSize,verSize)]
		pres = ["PrescriberInfo.png", (Window.width-rightPad-horSize,Window.height-topPad-verSize), (horSize,verSize)]
		sig = ["SigLine.png", (Window.width-rightPad-horSize*2,Window.height-topPad-verSize*2), (horSize*2,verSize)]
		
		self.lastValue = None
		self.buttons = Buttons([cust, drug, pres, sig])

		faxRatio = 1.3
		faxSize = (int(671*faxRatio), int(517*faxRatio))
		bottomFaxPad = 50
		faxPos = (int((Window.width - faxSize[0])/2), int(Window.height-topPad+bottomFaxPad))
		#color, relpos, relsize
		custPos0, custSize0 = self.get_highlight_pos_and_size(faxPos, faxSize, faxRatio, 140, 60, 72,15)
		custPos1, custSize1 = self.get_highlight_pos_and_size(faxPos, faxSize, faxRatio, 549, 60, 618-549,15)
		custHighlight = [[(1.0,0.0,0.0,0.2),custPos0, custSize0], [(1.0,0.0,0.0,0.2),custPos1, custSize1]]

		drugPos0, drugSize0 = self.get_highlight_pos_and_size(faxPos, faxSize, faxRatio, 128,168, 269-128, 168-156)
		drugHighlight = [[(0,1.0,0,0.3), drugPos0, drugSize0]]

		presPos0, presSize0 = self.get_highlight_pos_and_size(faxPos, faxSize, faxRatio, 159,276,261-159,276-265)
		presPos1, presSize1 = self.get_highlight_pos_and_size(faxPos, faxSize, faxRatio, 147,312,222-147,312-298)
		presHighlight = [[(0,0.0,1.0,0.2),presPos0, presSize0], [(0.0,0.0,1.0,0.2),presPos1, presSize1]]

		sigPos0, sigSize0 = self.get_highlight_pos_and_size(faxPos, faxSize, faxRatio, 120,204,289-120,204-190)
		sigHighlight = [[(0.5,0,0.7,0.2), sigPos0,sigSize0]]
		faxHighlightInfo = [custHighlight, drugHighlight, presHighlight, sigHighlight]
		self.fax = Fax("dummyForm.png", faxPos,  faxSize, faxHighlightInfo)
		print "window size ", Window.width, " ", Window.height
		#self.fax = Fax()
		# for i in range(len(self.buttons)):
		# 	self.canvas.add(self.buttons[i])
		# 	self.canas.add()
		self.canvas.add(self.buttons)
		self.canvas.add(self.fax)
		print Window.width, Window.height
	def on_touch_down(self, touch) :
		pass

	def on_touch_up(self, touch) :
		
		print 'up', touch.pos

	def on_touch_move(self, touch) :

		pass

	def get_highlight_pos_and_size(self,faxPos, faxSize, faxRatio, leftX, bottomY, xSize, ySize):
		return ((faxPos[0] + int(leftX*faxRatio), faxPos[1] + faxSize[1] - int(faxRatio*bottomY)), (int(xSize*faxRatio), int(ySize*faxRatio)))

	# called every frame to update stuff (like the label)
	def on_update(self):
		if self.lastValue != self.buttons.checkOverlap(Window.mouse_pos):
			print self.buttons.checkOverlap(Window.mouse_pos)
			self.lastValue = self.buttons.checkOverlap(Window.mouse_pos)
			self.fax.show_highlight(self.lastValue)





class Buttons(CanvasBase):
	def __init__(self, imageList):
		super(Buttons, self).__init__()
		self.rectangles = []
		self.imageList = imageList
		with self:
			#self.color = Color(*color)
			for i in range(len(imageList)):
				self.rectangle = Rectangle(texture=Image(imageList[i][0]).texture,pos = imageList[i][1], size = imageList[i][2])


	def checkOverlap(self, mousePos):
		toReturn = None
		for i in range(len(self.imageList)):
			if self.contains(mousePos,self.imageList[i][1][0], self.imageList[i][1][1], self.imageList[i][2][0], self.imageList[i][2][1]):
				toReturn = i

		return toReturn

	def contains(self, point, xLeft, yBottom, width, height):
	    return (xLeft <= point[0] <= xLeft+width and
	            yBottom <= point[1] <= yBottom+height)
			





class Fax(CanvasBase):
	def __init__(self, image, pos, size, highlightInfo):
		super(Fax, self).__init__()
		with self:
			self.color = Color(1,1,1)
			self.rectangle = Rectangle(texture=Image(image).texture,pos = pos, size = size)
			self.highlight = Rectangle(pos=(0,0), size = (0,0))
		self.highlightInfo = highlightInfo
	def show_highlight(self,highlightIndex):
		if highlightIndex is not None:
			print "should be changing to"
			#super(Fax, self).remove(self.highlight)
			self.remove(self.highlight)
			self.highlight = Highlight(self.highlightInfo[highlightIndex])
			#super(Fax, self).add(self.highlight)
			print self.highlight
			self.add(self.highlight)
		else:
			self.remove(self.highlight)
			self.highlight = Rectangle(pos=(0,0), size = (0,0))
			self.add(self.highlight)
		





class Highlight(CanvasBase):
	def __init__(self, highlightInfo):
		super(Highlight, self).__init__()
		with self:
			#print "a new one at pos ", pos, " size ", size, " color ", color
			self.color = Color(*highlightInfo[0][0])
			#print "color is ", self.color.color
			self.rectangles = []
			for i in range(len(highlightInfo)):
				pos = highlightInfo[i][1]
				size = highlightInfo[i][2]
				self.rectangles.append(Rectangle(pos = pos, size = size)) 
			#self.highlights = highlights 

run(eval('MainWidget1'))