import arcade

#Obstical Information
OBSTICAL_SPEED = 3

class Pig(arcade.Sprite):
    ''' Pig Class '''

    def update(self):
        self.center_y -= OBSTICAL_SPEED #y for vertical movment

        if self.top < 0: # used to get rid of an obstical that moves off the bottom of the screen
            self.remove_from_sprite_lists()