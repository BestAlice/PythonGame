import arcade
import os
from math import atan2
#что-то вроде масштаба спрайта, хз как работает
SPRITE_SCALING = 0.5
#парамерты окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Play"

MOVEMENT_SPEED = 5  # скорость персонажа


class Player(arcade.Sprite): #создаём класс и пишем перемещение
#                                   персонажа
    def __init__(self):
        super().__init__("knight.jpg", SPRITE_SCALING)
        
    def update(self):
        #self.on_mouse_motion()
        self.center_x += self.change_x
        self.center_y += self.change_y

        #проверки чтобы не выходил за окно
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

    def update_angle(self, mouse_list):
        self.radians = atan2(mouse_list['y'] - self.center_y, mouse_list['x'] - self.center_x)
        

class MyGame(arcade.Window):# основной класс игры

    def __init__(self, width, height, title):
        # делаем super тк по сути мы наследуем от класса Window
        super().__init__(width, height, title)

        # без этой херни не хочет искать изображения в нашем каталоге
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        #по идее эта переменная служит, чтобы наш перс потом смог
        #взаимодействовать с другими спрайтами
        self.player_list = None
        # создаём спрайт нашего перса
        self.player_sprite = None
        # фон
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):# хз зачем тут setup
        #Еее теперь наш перс находится в списке, где будут находится
        #вообще все спрайты(не точно)
        self.player_list = arcade.SpriteList()
        #рисуем нашего перса, тут же используется масштаб
        self.player_sprite = Player()
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        #добавляем спрайт перса в основной список спрайтов
        self.player_list.append(self.player_sprite)
        self.mouse =arcade.View()
        self.mouse_pos = {'x': self.player_sprite.center_x, 'y': self.player_sprite.center_y, 'dx': 0, 'dy': 0}

    def on_draw(self):
        #без неё мы не сможем рисовать, как работает хз
        arcade.start_render()
        #рисуем перса
        self.player_list.draw()

    def on_update(self, delta_time):# обновление для всех спрайтов
        self.player_list.update()
        self.player_sprite.update_angle(self.mouse_pos)

    def on_key_press(self, key, modifiers):# обработка клавиатуры при нажатии
        # всё должно быть понятно, кроме того что такое modifiers
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED#скорость перса
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):#обработка клавы при
        #отпускании клавиш
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = {'x': x, 'y': y, 'dx': dx, 'dy': dy}


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
