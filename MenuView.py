import arcade
import random
import os
import arcade.gui

from arcade.experimental.uislider import UISlider
from arcade.gui.events import UIOnChangeEvent

from GameView import GameView

class MenuView(arcade.View):
    '''Main Menu'''

    def __init__(self):
        super().__init__()

        # a UIManager to handle the UI
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Background color
        arcade.set_background_color(arcade.color.DARK_JUNGLE_GREEN)

        #Creat a vertical Boxgroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Setting uniform button width
        BUTTON_WIDTH = 200

        ui_start_button = arcade.gui.UIFlatButton(text="Start", width=BUTTON_WIDTH)
        self.v_box.add(ui_start_button.with_space_around(bottom=20))

        # Handle Clicks
        @ui_start_button.event("on_click")
        def on_click_start_button(event):
            # print("Start Button pressed", event)
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        ui_settings_button = arcade.gui.UIFlatButton(text="Settings", width=BUTTON_WIDTH)
        self.v_box.add(ui_settings_button.with_space_around(bottom=20))

        # Handle Clicks
        @ui_settings_button.event("on_click")
        def on_click_settings_button(event):
            print("Settings Button pressed", event)
            setting_view = SettingView()
            self.window.show_view(setting_view)

        ui_howtoplay_button = arcade.gui.UIFlatButton(text="How to Play", width=BUTTON_WIDTH)
        self.v_box.add(ui_howtoplay_button.with_space_around(bottom=20))

        # Handle Clicks
        @ui_howtoplay_button.event("on_click")
        def on_click_howtoplay_button(event):
            print("How to Play Button pressed", event)
            instructions_view = InstructionView()
            self.window.show_view(instructions_view)

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y",child=self.v_box))

    def on_draw(self):
        #clears the screen
        self.clear()
        # Manager takes care of the drawing
        self.manager.draw()

class SettingView(arcade.View):
    '''
    player 1 and player 2 buttons
    '''

    def __init__(self):
        super().__init__()

        self.multi_player = False

        # a UIManager to handle the UI
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Background color
        arcade.set_background_color(arcade.color.DARK_JUNGLE_GREEN)

        # Level Set slider
        ui_level_slider = UISlider(value=1, min_value=1, max_value=20, width=300, height=50)
        label = arcade.gui.UILabel(text= f"{int(ui_level_slider.value)}")

        @ui_level_slider.event()
        def on_change(event: UIOnChangeEvent):
            label.text = f"{int(ui_level_slider.value)}"
            label.fit_content()

        self.manager.add(arcade.gui.UIAnchorWidget(child=ui_level_slider))
        self.manager.add(arcade.gui.UIAnchorWidget(child=label,align_y=100))

        # Setting uniform button width
        BUTTON_WIDTH = 200

        #Creat a horizontile Boxgroup to align buttons
        self.h_box = arcade.gui.UIBoxLayout(vertical=False)

        ui_player1_button = arcade.gui.UIFlatButton(text="1 Player", width=BUTTON_WIDTH)
        self.h_box.add(ui_player1_button.with_space_around(bottom=20))

        # Handle Clicks
        @ui_player1_button.event("on_click")
        def on_click_start_button(event):
            print("Start Button pressed", event)
            self.multi_player = False
            game_view = GameView(self.multi_player)
            game_view.setup(int(ui_level_slider.value))
            self.window.show_view(game_view)

        ui_player2_button = arcade.gui.UIFlatButton(text="2 Player", width=BUTTON_WIDTH)
        self.h_box.add(ui_player2_button.with_space_around(bottom=20))

        # Handle Clicks
        @ui_player2_button.event("on_click")
        def on_click_start_button(event):
            print("Start Button pressed", event)
            self.multi_player = True
            game_view = GameView(self.multi_player)
            game_view.setup(int(ui_level_slider.value))
            self.window.show_view(game_view)
    
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="bottom", child = self.h_box))
        
    def on_draw(self):
        self.clear()
        self.manager.draw()

class InstructionView(arcade.View):

    def __init__(self):
        super().__init__()
        
        # Sets background color
        arcade.set_background_color(arcade.color.BATTLESHIP_GREY)

    def on_draw(self):

        self.clear()

        # "How to Play" title centered x, -100 from window height
        arcade.draw_text("How to Play", self.window.width / 2, self.window.height - 100, arcade.color.WHITE, font_size=30, anchor_x="center")
        
        howtoplay_text1 = "Player 1 uses \"A\", \"S\", \"D\", \"W\" to move and \"SPACE\" to shoot."
        howtoplay_text2 = "Player 2 uses the arrow keys to move and \"M\" to shoot."
        howtoplay_text3 = "Destroy towers and collect pigs to earn points."

        arcade.draw_text(howtoplay_text1, 20, self.window.height-200, arcade.color.WHITE_SMOKE, font_size=20, anchor_x="left")
        arcade.draw_text(howtoplay_text2, 20, self.window.height-240, arcade.color.WHITE_SMOKE, font_size=20, anchor_x="left")
        arcade.draw_text(howtoplay_text3, 20, self.window.height-280, arcade.color.WHITE_SMOKE, font_size=20, anchor_x="left")

        arcade.draw_text("Click to go back", self.window.width/2, 100, arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        ''' when mouse is pressed '''
        menu_view = MenuView()
        self.window.show_view(menu_view)
