import arcade
import random
import os

from Explosion import Explosion
from Bullet import Bullet
from Player import Player
from Obstical import Obstical
from Pig import Pig

# Player Sprite Information
SPRITE_SCALING_Player = 0.4
MOVMENT_SPEED = 5

# Projectile Information
SPRITE_SCALING_FIRE = 0.15
BULLET_SPEED = 7

# Obstical Information
SPRITE_SCALING_OBSTICAL = 0.17
OBSTICAL_SPEED = 3
OBSTICAL_COUNT = 5

# Pig Information
SPRITE_SCALING_PIG = 0.05
PIG_SPEED = 3
PIG_COUNT = 3

# Screen Information
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Dragons & Castles"

''' Game Classes '''

class GameView(arcade.View):
    '''Main Application class'''

    def __init__(self, multi_player=False):
        '''initializer'''
        
        #calls the parent class initilizer
        super().__init__()

        # Player amount deals with 2 players
        self.multi_player = multi_player

        #variables that will hold sprite lists
        self.pig_list = None
        self.obstical_list = None
        self.explosions_list = None
        self.bullet_list = None
        self.player1_list = None
        self.player2_list = None

        #set up player info
        self.player1_sprite = None
        self.player2_sprite = None

        #track the current state of what key is pressed
        # Start will all of the keys not being pressed
        self.A_pressed = False
        self.D_pressed = False
        self.W_pressed = False
        self.S_pressed = False

        # Player 2
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Sets level information
        self.level = 1

        #sets up score information
        self.score = 0

        # Sets plain background color
        arcade.set_background_color(arcade.color.AO)

        '''Preloading Sprite Sheets'''
        # loads the explosion sprite sheet
        self.explosion_texture_list = []

        columns = 6 # how many columns on the sheet
        count = 42 # how many images on the sheet?
        sprite_width = 66 # pixle hight and width for each sprite
        sprite_height = 66
        file_name = "Resources/Explosion_sprite_sheet2.png"

        self.explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

        # loads fire animation sheet
        columns = 2 # how many columns on the sheet
        count = 4 # how many images on the sheet?
        sprite_width = 50 # pixle hight and width for each sprite
        sprite_height = 50
        file_name = "Resources/Fire_animate2.png"

        self.bullet_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

        # loads player 1 animation sheet
        # columns = 4 # how many columns on the sheet
        # count = 16 # how many images on the sheet?
        # sprite_width = 205 # pixle hight and width for each sprite
        # sprite_height = 161
        # file_name = "Resources/Red_Dragon_final.png"

        # self.player1_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

    def setup(self, level=1):
        ''' Set up the game and initialize the variables'''

        self.level = level
        self.score = 0

        #sprite lists
        self.bullet_list = arcade.SpriteList()
        self.obstical_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.pig_list = arcade.SpriteList()
        self.player1_list = arcade.SpriteList()


        # Creates and sets location for player sprite
        self.player1_sprite = Player("Resources/Red_Dragon.png", SPRITE_SCALING_Player)
        self.player1_sprite.center_x = SCREEN_HEIGHT/2
        self.player1_sprite.center_y = 100
        self.player1_list.append(self.player1_sprite)

        if self.multi_player == True:
            self.player2_list = arcade.SpriteList()
            self.player2_sprite = Player("Resources/White_Dragon.png", SPRITE_SCALING_Player)
            self.player2_sprite.center_x = 3 * SCREEN_HEIGHT/4
            self.player2_sprite.center_y = 100
            self.player2_list.append(self.player2_sprite)

        self.game_level()

    def game_level(self):
        
        # Increased the number of obsticals per level
        for i in range(self.level * OBSTICAL_COUNT):
            
            # Sets a max level of 50 (250 towers)
            if self.level == 50:
                self.level = 50                

            #create the obstical instance
            obstical = Obstical("Resources/Obstical1.png", SPRITE_SCALING_OBSTICAL)

            ''' Making sure objects are not on each other'''
            obstical_placed_successfully = False

            while not obstical_placed_successfully:
                #position obstical
                obstical.center_x = random.randrange(SCREEN_WIDTH)
                obstical.center_y = random.randrange(SCREEN_HEIGHT + 20, SCREEN_HEIGHT*3)

                #creates list of tower with tower collisions
                obstical_hit_list = arcade.check_for_collision_with_list(obstical, self.obstical_list)

                if len(obstical_hit_list) == 0:
                    obstical_placed_successfully = True

            self.obstical_list.append(obstical)

        pig_amount = random.randrange(self.level * PIG_COUNT)

        for i in range(pig_amount):
            pig = Pig("Resources/Pig_health.png", SPRITE_SCALING_PIG)

            ''' Making suer objects are not on each other'''
            pig_placed_successfully = False

            while not pig_placed_successfully:
                #position obstical
                pig.center_x = random.randrange(SCREEN_WIDTH)
                pig.center_y = random.randrange(SCREEN_HEIGHT + 20, SCREEN_HEIGHT*3)

                obstical_hit_list = arcade.check_for_collision_with_list(pig, self.obstical_list)
                pig_hit_list = arcade.check_for_collision_with_list(pig, self.pig_list)


                if len(obstical_hit_list) == 0 and len(pig_hit_list) == 0:
                    pig_placed_successfully = True

            self.pig_list.append(pig)

    def on_draw(self):
        ''' Render the Screen '''
        
        #this command has to happen before drawing
        self.clear()

        # draw all the sprites. Place in reverse order of top to bottom
        self.pig_list.draw()
        self.obstical_list.draw()
        self.explosions_list.draw()
        self.bullet_list.draw()
        self.player1_list.draw() # Has to be drawn last to be on "top"

        if self.multi_player == True:
            self.player2_list.draw()

        # Level text on the screen
        level_text = f"Level: {self.level}"
        arcade.draw_text(level_text, 10, 20, arcade.color.BLACK, 15)
        
        # Score text on the screen
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 40, arcade.color.BLACK, 15)

    def update_player1_speed(self):
        ''' Handles player Movement '''

        #calculate speed based on the keys pressed
        self.player1_sprite.change_x = 0
        self.player1_sprite.change_y = 0

        # Checks which buttons are pressed
        if self.W_pressed and not self.S_pressed: #if up and not down, then up
            self.player1_sprite.change_y = MOVMENT_SPEED
        elif self.S_pressed and not self.W_pressed: #if down and not up, then down
            self.player1_sprite.change_y = -MOVMENT_SPEED
        elif self.D_pressed and not self.A_pressed: #if right and not left, then right
            self.player1_sprite.change_x = MOVMENT_SPEED
        elif self.A_pressed and not self.D_pressed: #if left and not right, then left
            self.player1_sprite.change_x = -MOVMENT_SPEED

        # Allows for diagonal movment
        if self.W_pressed and self.A_pressed: #if up and left, go both
            self.player1_sprite.change_y = MOVMENT_SPEED
            self.player1_sprite.change_x = -MOVMENT_SPEED
        elif self.W_pressed and self.D_pressed: #if up and right, go both
            self.player1_sprite.change_y = MOVMENT_SPEED
            self.player1_sprite.change_x = MOVMENT_SPEED
        if self.S_pressed and self.A_pressed: #if down and left, go both
            self.player1_sprite.change_y = -MOVMENT_SPEED
            self.player1_sprite.change_x = -MOVMENT_SPEED
        if self.S_pressed and self.D_pressed: #if down and right, go both
            self.player1_sprite.change_y = -MOVMENT_SPEED
            self.player1_sprite.change_x = MOVMENT_SPEED  
    
    def update_player2_speed(self):
        ''' Handles player Movement '''

        #calculate speed based on the keys pressed
        self.player2_sprite.change_x = 0
        self.player2_sprite.change_y = 0

        # Checks which buttons are pressed
        if self.up_pressed and not self.down_pressed: #if up and not down, then up
            self.player2_sprite.change_y = MOVMENT_SPEED
        elif self.down_pressed and not self.up_pressed: #if down and not up, then down
            self.player2_sprite.change_y = -MOVMENT_SPEED
        elif self.right_pressed and not self.left_pressed: #if right and not left, then right
            self.player2_sprite.change_x = MOVMENT_SPEED
        elif self.left_pressed and not self.right_pressed: #if left and not right, then left
            self.player2_sprite.change_x = -MOVMENT_SPEED

        # Allows for diagonal movment
        if self.up_pressed and self.left_pressed: #if up and left, go both
            self.player2_sprite.change_y = MOVMENT_SPEED
            self.player2_sprite.change_x = -MOVMENT_SPEED
        elif self.up_pressed and self.right_pressed: #if up and right, go both
            self.player2_sprite.change_y = MOVMENT_SPEED
            self.player2_sprite.change_x = MOVMENT_SPEED
        if self.down_pressed and self.left_pressed: #if down and left, go both
            self.player2_sprite.change_y = -MOVMENT_SPEED
            self.player2_sprite.change_x = -MOVMENT_SPEED
        if self.down_pressed and self.right_pressed: #if down and right, go both
            self.player2_sprite.change_y = -MOVMENT_SPEED
            self.player2_sprite.change_x = MOVMENT_SPEED  

    def on_key_press(self, key, modifiers):
        ''' Called when a key in pressed '''

        # Changes the state of button presses in code to feed into update player speed
        if key == arcade.key.W:
            self.W_pressed = True
            self.update_player1_speed()
        elif key == arcade.key.S:
            self.S_pressed = True
            self.update_player1_speed()
        elif key == arcade.key.D:
            self.D_pressed = True
            self.update_player1_speed()
        elif key == arcade.key.A:
            self.A_pressed = True
            self.update_player1_speed()

        if key == arcade.key.SPACE:
            #create a bullet
            bullet = Bullet(self.bullet_texture_list)

            #give bullet speed
            bullet.change_y = BULLET_SPEED

            #position the bullet
            bullet.center_x = self.player1_sprite.center_x
            bullet.center_y = self.player1_sprite.top

            bullet.update()

            #add bullet to the apropriate lists
            self.bullet_list.append(bullet)

        # Player 2
        if self.multi_player == True:
                    
            if key == arcade.key.UP:
                self.up_pressed = True
                self.update_player2_speed()
            elif key == arcade.key.DOWN:
                self.down_pressed = True
                self.update_player2_speed()
            elif key == arcade.key.RIGHT:
                self.right_pressed = True
                self.update_player2_speed()
            elif key == arcade.key.LEFT:
                self.left_pressed = True
                self.update_player2_speed()

            if key == arcade.key.M:
                #create a bullet
                bullet = Bullet(self.bullet_texture_list)

                #give bullet speed
                bullet.change_y = BULLET_SPEED

                #position the bullet
                bullet.center_x = self.player2_sprite.center_x
                bullet.center_y = self.player2_sprite.top

                bullet.update()

                #add bullet to the apropriate lists
                self.bullet_list.append(bullet)
                        
            
    def on_key_release(self, key, modifiers):
        ''' Called when a key is released '''

        # Changes the state of button presses in code to feed into update player speed
        if key == arcade.key.W:
            self.W_pressed = False
            self.update_player1_speed()
        elif key == arcade.key.S:
            self.S_pressed = False
            self.update_player1_speed()
        elif key == arcade.key.D:
            self.D_pressed = False
            self.update_player1_speed()
        elif key == arcade.key.A:
            self.A_pressed = False
            self.update_player1_speed()

        # Player 2
        if self.multi_player == True:
            if key == arcade.key.UP:
                self.up_pressed = False
                self.update_player2_speed()
            elif key == arcade.key.DOWN:
                self.down_pressed = False
                self.update_player2_speed()
            elif key == arcade.key.RIGHT:
                self.right_pressed = False
                self.update_player2_speed()
            elif key == arcade.key.LEFT:
                self.left_pressed = False
                self.update_player2_speed()

    def on_update(self, delta_time):
        ''' Movment and game logic'''
        # This makes the computer talk and move the things around

        # Updates the position and state of the listed variables
        self.bullet_list.update()
        self.obstical_list.update()
        self.explosions_list.update()
        self.pig_list.update()
        self.player1_list.update()

        if self.multi_player == True:
            self.player2_list.update()

        # Checking bullet collision
        for bullet in self.bullet_list:

            # hit_list is checking one sprite against a list of sprites
            hit_list = arcade.check_for_collision_with_list(bullet, self.obstical_list)

            if len(hit_list) > 0: #If the bullet hit something
                bullet.remove_from_sprite_lists()

                explosion = Explosion(self.explosion_texture_list)

                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y

                explosion.update()

                self.explosions_list.append(explosion)

                self.score += 1
            
            for obstical in hit_list: #removes the obsticals it hit
                obstical.remove_from_sprite_lists()

        # Changing the level of the game
        if len(self.obstical_list) == 0:
            self.level += 1
            self.game_level()

        # Checking for player collision with pig
        player1_pig_list = arcade.check_for_collision_with_list(self.player1_sprite, self.pig_list)

        for pig in player1_pig_list:
            pig.remove_from_sprite_lists()
            self.score += 5

        # Checking for player collision with obstical
        player1_obstical_list = arcade.check_for_collision_with_list(self.player1_sprite, self.obstical_list)

        if len(player1_obstical_list) > 0:
            self.setup()
            return
        
        # PLayer 2
        if self.multi_player == True:
            # Checking for player collision with pig
            player2_pig_list = arcade.check_for_collision_with_list(self.player2_sprite, self.pig_list)

            for pig in player2_pig_list:
                pig.remove_from_sprite_lists()
                self.score += 5

            # Checking for player collision with obstical
            player2_obstical_list = arcade.check_for_collision_with_list(self.player2_sprite, self.obstical_list)

            if len(player2_obstical_list) > 0:
                self.setup()
                return
            