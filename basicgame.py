import pygame
import random
import sys
from vec2d import vec2d
from pygame.sprite import Sprite
	

class Kanye(pygame.sprite.Sprite):
	def __init__(self, screen, img_filename, init_position, speed, health):
		Sprite.__init__(self)
		self.screen = screen
		self.health = health
		self.base_image = pygame.image.load(img_filename).convert_alpha()
		self.base_image = pygame.transform.scale(self.base_image, [64,64])
		self.image = self.base_image
		self.rect = self.image.get_rect()
		self.pos = vec2d(init_position)
		self.health = health
		self.speed = speed
		self.direction = vec2d([0,1]).normalized()

	def update(self, keypressed = None):
		self._change_direction(keypressed)
		self.image = pygame.transform.rotate(self.base_image, -self.direction.angle)
		if keypressed == pygame.K_w:
			displacement = vec2d(self.direction.x * self.speed, self.direction.y * self.speed)
		else:
			displacement = 0
		self.image_w, self.image_h = self.image.get_size()
		bounds_rect = self.screen.get_rect().inflate(-self.image_w, -self.image_h)
		self.pos += displacement
		if self.pos.x < bounds_rect.left:
			self.pos.x = bounds_rect.left
		elif self.pos.x > bounds_rect.right:
			self.pos.x = bounds_rect.right
		elif self.pos.y < bounds_rect.top:
			self.pos.y = bounds_rect.top
		elif self.pos.y > bounds_rect.bottom:
			self.pos.y = bounds_rect.bottom

	def blitit(self):
		draw_pos = self.image.get_rect().move(
			self.pos.x - self.image_w / 2, 
			self.pos.y - self.image_h / 2)
		self.rect.topleft = (self.pos.x,self.pos.y)
		self.screen.blit(self.image, draw_pos)
	def _change_direction(self, keypressed):
		if keypressed == pygame.K_a:
			self.direction.rotate(-90)
		if keypressed == pygame.K_d:
			self.direction.rotate(90)


class JayZ(pygame.sprite.Sprite):
	def __init__(   
		self, screen, img_filename, init_position, 
		init_direction, speed):
		Sprite.__init__(self)
		self.screen = screen
		self.speed = speed
		self.base_image = pygame.image.load(img_filename).convert_alpha()
		self.base_image = pygame.transform.scale(self.base_image, [64, 64])
		self.image = self.base_image
		self.rect = self.image.get_rect()

		self.pos = vec2d(init_position)
		self.direction = vec2d(init_direction).normalized()
			
	def update(self, time_passed):
		self._change_direction(time_passed)
		self.image = pygame.transform.rotate(self.base_image, -self.direction.angle)
		displacement = vec2d(self.direction.x * self.speed * time_passed, self.direction.y * self.speed * time_passed)
		self.pos += displacement
		self.image_w, self.image_h = self.image.get_size()
		bounds_rect = self.screen.get_rect().inflate(
						-self.image_w, -self.image_h)
		if self.pos.x < bounds_rect.left:
			self.pos.x = bounds_rect.left
			self.direction.x *= -1
		elif self.pos.x > bounds_rect.right:
			self.pos.x = bounds_rect.right
			self.direction.x *= -1
		elif self.pos.y < bounds_rect.top:
			self.pos.y = bounds_rect.top
			self.direction.y *= -1
		elif self.pos.y > bounds_rect.bottom:
			self.pos.y = bounds_rect.bottom
			self.direction.y *= -1
	
	def blitit(self):
		draw_pos = self.image.get_rect().move(
			self.pos.x - self.image_w / 2, 
			self.pos.y - self.image_h / 2)
		self.rect.topleft = (self.pos.x,self.pos.y)
		self.screen.blit(self.image, draw_pos)
			   
	_counter = 0
	
	def _change_direction(self, time_passed):
		self._counter += time_passed
		if self._counter > random.randint(400, 500):
			self.direction.rotate(90 * random.randint(-1, 1))
			self._counter = 0
	
def choice(lis):
	return lis[random.randrange(0,len(lis))]
def gamestart():
	pygame.init()
	screen = pygame.display.set_mode()
	clock = pygame.time.Clock()
	globMAX_FPS = 120
	ANGLE_TURN = 45
	myfont = pygame.font.SysFont("monospace", 30)
	score = 0
	color = [random.randint(0,255) for i in xrange(3)]
	RANGE = 3
	NUM_RAPS = 40
	IMGS = ['jayz.jpg','eminem.jpg']
	resolution = [pygame.display.Info().current_w,pygame.display.Info().current_h]
	SCREEN_WIDTH  = resolution[0]
	SCREEN_HEIGHT = resolution[1]
	kanye = Kanye(screen, 'ourGod.jpg', [random.randint(0, x) for x in resolution], 100, 100) 
	jayzs = [JayZ(screen, choice(IMGS), [random.randint(0, SCREEN_WIDTH),random.randint(0, SCREEN_HEIGHT)], [0, choice([-1,1])], 0.1) for i in range(NUM_RAPS)]


	while 1: 
		time_passed = clock.tick(50)
		color = [random.randint(i - RANGE, i + RANGE) % 255 for i in color]
		screen.fill(color)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				kanye.update(event.key)	


		if score == NUM_RAPS:	
			gamestart()
		for jayz in jayzs:
			jayz.update(time_passed)
			jayz.blitit()
		kanye.update()
		for jayz in jayzs:
			if pygame.sprite.collide_rect(jayz, kanye):
				jayzs.remove(jayz)
				score = score + 1
				label = myfont.render("YAY! " , 1, (255,255,0))
				screen.blit(label, (100, 100))
		screen.blit(myfont.render("SCORE : " + str(score), 1, (255, 255, 0)), (300, 100))
		kanye.blitit()	
	
		pygame.display.flip()

gamestart()