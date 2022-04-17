class Controller:
    def __init__(self):
        self.game_over = False
        self.game_close = False

    def set_gameover(self):
        self.game_over = True

    def set_gameclose(self):
        self.game_close = False

    def change_gameclose(self, param):
        if param != None:
            self.game_close = param

    def food_behind_border(self, foodx, foody, dis_width, dis_height):
        if foodx >= dis_width or foodx < 0 or foody >= dis_height or foody < 0:
            return True