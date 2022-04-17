import constants

class MySnake:

	def __init__(self, food):
		self.x1 = None
		self.y1 = None
		self.x1_change = 0
		self.y1_change = 0
		self.snake_List = []
		self.Length_of_snake = 1
		self.snake_Head = []
		self.food = food

	def set_x1_y1(self, dis_width, dis_height):
		self.x1 = dis_width / 2
		self.y1 = dis_height / 2

	def change_x1y1_change(self, x1_change, y1_change):
		self.x1_change = x1_change 
		self.y1_change = y1_change
	
	def is_border_death(self, dis_width, dis_height):
		if self.x1 >= dis_width or self.x1 < 0 or self.y1 >= dis_height or self.y1 < 0:
			return True

	def change_x1_y1(self):
		self.x1 += self.x1_change
		self.y1 += self.y1_change

	def add_snake_head(self):
		self.snake_Head = []
		self.snake_Head.append(self.x1)
		self.snake_Head.append(self.y1)
		self.snake_List.append(self.snake_Head)

	def control_snake_size(self):
		if len(self.snake_List) > self.Length_of_snake:
			del self.snake_List[0]

	def self_death(self):
		for x in self.snake_List[:-1]:
			if x == self.snake_Head:
				return True
    
	def inc_snake_length(self):
		if self.x1 == self.food.foodx and self.y1 == self.food.foody:
			self.food.get_new_pos(constants.dis_width,constants.dis_height,constants.snake_block)
			self.Length_of_snake += 1
			return True
		return False