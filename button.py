import pygame

BLACK = (0, 0, 0)

class Button():
	def __init__(self, color: tuple[int, int, int], left_corner_x: int, left_corner_y: int, width: int, height: int, font: pygame.font.SysFont, text: str = '',):
		self.color = color
		self.left_corner_x = left_corner_x
		self.left_corner_y = left_corner_y
		self.width = width
		self.height = height
		self.text = text
		self.font = font

	def draw(self, window: pygame.display, outline: tuple[int, int, int] = None):
		#Call this method to draw the button on the screen
		if outline:
			pygame.draw.rect(window, outline, (self.left_corner_x-2,self.left_corner_y-2,self.width+4,self.height+4),0)
			
		pygame.draw.rect(window, self.color, (self.left_corner_x,self.left_corner_y,self.width,self.height),0)
		
		if self.text != '':
			text = self.font.render(self.text, 1, (0,0,0))
			window.blit(text, (self.left_corner_x + (self.width/2 - text.get_width()/2), self.left_corner_y + (self.height/2 - text.get_height()/2)))
	
	def remove(self, window: pygame.display):
		pygame.draw.rect(window, BLACK, (self.left_corner_x,self.left_corner_y,self.width,self.height),0)

	def is_over_mouse(self, pos: tuple[int, int]) -> bool:
		#Pos is the mouse position or a tuple of (x,y) coordinates
		if pos[0] > self.left_corner_x and pos[0] < self.left_corner_x + self.width and pos[1] > self.left_corner_y and pos[1] < self.left_corner_y + self.height:
				return True
		return False
	
	def get_x(self) -> int:
		return self.left_corner_x
	
	def get_y(self) -> int:
		return self.left_corner_y
	
	def get_width(self) -> int:
		return self.width
	
	def get_height(self) -> int:
		return self.height

	def change_color(self, new_color: tuple[int, int, int]):
		self.color = new_color

	def change_left_corner_y(self, new_left_corner_y: int):
		self.left_corner_y = new_left_corner_y

	def get_font(self) -> pygame.font.SysFont:
		return self.font