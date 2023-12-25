import pygame
import sys 

#button class
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale) + 50, int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class Input():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.active_color = pygame.Color('lightskyblue3') 
		self.passive_color = pygame.Color('black')
		self.currentColor = self.passive_color
		self.active = False
		self.clock = pygame.time.Clock()
		self.rectangle = pygame.Rect(x, y, 300, 32) 
		self.font = pygame.font.Font(None, 30)
		self.user_text = ""
	def draw(self, surface):
		txt_surface = self.font.render(self.user_text, True, self.currentColor)
		# width = max(200, txt_surface.get_width()+10)
		# self.rectangle.w = width
		surface.blit(txt_surface, (self.rectangle.x+5, self.rectangle.y+5))
		pygame.draw.rect(surface, self.currentColor, self.rectangle, 2)

class Label:
    def __init__(self, screen, text, x, y, size=20, color="black"):
        self.font = pygame.font.Font(None, 30)
        self.image = self.font.render(text, 1, color)
        _, _, w, h = self.image.get_rect()
        self.rect = pygame.Rect(x, y, w, h)
        self.screen = screen
        self.text = text
    def draw(self, screen):
	    self.screen.blit(self.image, (self.rect))