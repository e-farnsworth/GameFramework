import arcade

# Screen Information
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Bullet(arcade.Sprite):
    ''' Projectile class '''

    def __init__(self, texture_list):
        super().__init__()

        self.current_texture = 0
        self.textures = texture_list

    def update(self):
        #only looking for vertical movment since x position does not change
        self.center_y +=self.change_y
        self.current_texture += 1
        self.set_texture((self.current_texture)%len(self.textures))

        if self.bottom > SCREEN_HEIGHT: # used to get rid of a bullet that moves off the top of the screen
            self.remove_from_sprite_lists()