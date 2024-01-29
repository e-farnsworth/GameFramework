import arcade

# Screen Information
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Dragons & Castles"

class Player(arcade.Sprite):
    ''' Player Class '''
    
    # def __init__(self, texture_list):
    #     super().__init__()
    #     self.current_texture = 0
    #     self.textures = texture_list

    def update(self):
        '''move the player'''
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Chaecking fot bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
            # Since things are lefthand oriented, this is done to check right bound

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1
            # Since things are bottom oriented, this is done to check top bound
