from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import *
from kivy.graphics import *
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.vector import Vector
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ListProperty
import random
from snake import MySnake
from food import MyFood
from controller import Controller as cont
import constants as ct

Builder.load_file("worm.kv")

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
SNAKE_BLOCK = 20
Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)


class Food(Widget, MyFood):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.get_new_pos(WINDOW_WIDTH, WINDOW_HEIGHT, SNAKE_BLOCK)

    def set_pos(self, x, y):
        self.pos = (x, y)

    def move_(self):
        self.move(SNAKE_BLOCK)
        self.pos = self.ret_food_pos()
        
        if cont.food_behind_border(self, self.foodx, self.foody, WINDOW_WIDTH, WINDOW_HEIGHT):
            self.get_new_pos(WINDOW_WIDTH, WINDOW_HEIGHT, SNAKE_BLOCK)
        

class Snake(Widget, MySnake):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_x1_y1(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.nodes = []

    def create_node(self, canvas):
        self.pos = (self.x1, self.y1)
        self.nodes.append(Rectangle(pos=self.pos, size=(SNAKE_BLOCK, SNAKE_BLOCK)))
        with canvas:
            Color(1, 1, 1)
        canvas.add(self.nodes[-1])

    def move_(self, canvas):
        self.change_x1_y1()
        self.pos = (self.x1, self.y1)
        self.create_node(canvas)

    def control_snake_size_(self, canvas):
        if len(self.nodes) > self.Length_of_snake:
            canvas.remove(self.nodes[0])
            del self.nodes[0]
        self.control_snake_size()

class SnakeGame(Widget):
    food = ObjectProperty(None)
    score = StringProperty()
    score_color = ListProperty([1, 0, 0, 1])
    up_score_color = ListProperty([0, 1, 1, 0])

    def start(self):
        self.score = str(0)
        self.snake = Snake(food=self.food)
        self.snake.create_node(self.canvas)
        self.cur_dir = None
        self.contr = cont()

    def clear(self):
        for node in self.snake.nodes:
            self.canvas.remove(node)

    def on_touch_down(self, touch):
        if self.contr.game_over is False:
            touch_pos = touch.pos

            ws = touch.x / WINDOW_WIDTH
            hs = touch.y / WINDOW_HEIGHT
            aws = 1 - ws
            if ws > hs and aws > hs:
                cur_dir = (0, -SNAKE_BLOCK)         # Down
            elif ws > hs >= aws:
                cur_dir = (SNAKE_BLOCK, 0)          # Right
            elif ws <= hs < aws:
                cur_dir = (-SNAKE_BLOCK, 0)         # Left
            else:
                cur_dir = (0, SNAKE_BLOCK)           # Up

            if self.cur_dir is not None and self.cur_dir[0] == -cur_dir[0] and self.cur_dir[1] == -cur_dir[1]:
                return

            self.cur_dir = cur_dir

            self.snake.change_x1y1_change(cur_dir[0], cur_dir[1])
        else:
            self.clear()
            self.start()
            self.score_color[-1] = 1
            self.up_score_color[-1] = 0

    def update(self, dt):
        if self.contr.game_over is False:
            self.snake.move_(self.canvas)
            self.snake.add_snake_head()
            
            if self.snake.inc_snake_length() is True:
                self.score = str(self.snake.Length_of_snake - 1)
                pos = self.food.ret_food_pos()
                self.food.set_pos(pos[0], pos[1])
            
            self.snake.control_snake_size_(self.canvas)
            
            if self.snake.self_death() is True or self.snake.is_border_death(WINDOW_WIDTH, WINDOW_HEIGHT):
                self.contr.set_gameover()
                self.score_color[-1] = 0
                self.up_score_color[-1] = 1
                
    def food_move(self, dt):
        self.food.move_()

class WormApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SnakeGame = SnakeGame()

    def build(self, **kwargs):
        self.SnakeGame.start()
        Clock.schedule_interval(self.SnakeGame.food_move, 1.0 / 0.5)
        Clock.schedule_interval(self.SnakeGame.update, 1.0 / 8.0)
        
        return self.SnakeGame


if __name__ == '__main__':
    WormApp().run()