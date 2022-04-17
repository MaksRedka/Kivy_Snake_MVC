import random

class MyFood:
	def __init__(self):
		self.foodx = 0
		self.foody = 0

	def get_new_pos(self, dis_width, dis_height, snake_block):
		self.foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
		self.foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0

	def move(self, snake_block):
		side = random.randrange(0,100)

		if side < 25:
			self.foodx -= snake_block
		elif side > 25 and side < 50:
			self.foodx += snake_block
		elif side > 50:
			self.foody += snake_block
		else:
			self.foody -= snake_block
	
	def ret_food_pos(self):
		return [self.foodx,self.foody]

