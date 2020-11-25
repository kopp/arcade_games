"""
Find the fastest way from start to end.
"""

import random
import arcade
import copy

class FindFastestWay(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height, "Find Fastest Way")
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.initial_obstacles = []  # obstacles on init (useful for restart)
        self.obstacles = arcade.SpriteList()  # active/visible obstacles

        self.goal = arcade.Sprite(":resources:images/enemies/slimeGreen.png")
        self.goal.center_x = 0.9 * screen_width
        self.goal.center_y = 0.95 * screen_height

        self.player = arcade.Sprite(":resources:images/enemies/frog.png")

        self.setup(True)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self, new_obstacles=False):
        self.player.stop()
        self.won = False
        self.lost = False
        self.distance_traveled = 0
        self.number_of_obstacles_removed = 0
        self.player.position = (0, 0)
        if new_obstacles:
            for sprite in self.obstacles:
                sprite.remove_from_sprite_lists()
            self._create_obstacles()
        self._set_obstacles_to_initial_obstacles()

    def _create_obstacles(self, number_of_obstacles: int = 17):
        self.initial_obstacles = []
        for i in range(number_of_obstacles):
            obstacle = arcade.Sprite(":resources:images/tiles/boxCrate_double.png")
            obstacle.center_x = random.random() * self.screen_width
            obstacle.center_y = random.random() * self.screen_height
            # Note: Unless https://github.com/pythonarcade/arcade/issues/752 is
            # resolved, do not scale by setting width or height of the sprites
            self.initial_obstacles.append(obstacle)

    def _set_obstacles_to_initial_obstacles(self):
        self.obstacles = arcade.SpriteList()
        for obstacle in self.initial_obstacles:
            self.obstacles.append(copy.deepcopy(obstacle))

    def _increase_speed_of_obstacles(self):
        for obstacle in self.obstacles:
            if obstacle.change_x == 0:
                obstacle.change_angle = 0.2 * random.random()
                obstacle.change_x = 0.6 * random.random()
                obstacle.change_y = 0.6 * random.random()
            else:
                obstacle.change_angle += 0.1 * random.random()
                obstacle.change_x += random.random()
                obstacle.change_y += random.random()


    def remove_obstacles_around_player(self, max_distance=200):
        for obstacle in self.obstacles:
            distance = arcade.get_distance_between_sprites(self.player, obstacle)
            if distance < max_distance:
                obstacle.remove_from_sprite_lists()
                self.number_of_obstacles_removed += 1
        self._increase_speed_of_obstacles()

    def on_draw(self):
        arcade.start_render()
        self.obstacles.draw()
        self.goal.draw()
        self.player.draw()  # draw later -> draw over other objects
        if self.lost:
            arcade.draw_text("You lost :-(", self.width/3, 0.7 * self.height, arcade.color.RED, 34)
        if self.won:
            arcade.draw_text("You made it", self.width/3, 0.7 * self.height, arcade.color.RED, 34)
            arcade.draw_text(f"Distance traveled {self.distance_traveled}", self.width/3, 0.5 * self.height, arcade.color.BLACK, 24)
            arcade.draw_text(f"Obstacles removed {self.number_of_obstacles_removed}", self.width/3, 0.4 * self.height, arcade.color.BLACK, 24)

    def _increment_distance_traveled(self, old_position, new_position):
        # use Manhattan distance as the sprite can only move in x or y direction
        delta_x = abs(old_position[0] - new_position[0])
        delta_y = abs(old_position[1] - new_position[1])
        self.distance_traveled += delta_x + delta_y

    def on_update(self, delta_time):
        if self.lost or self.won:
            return

        old_position = self.player.position
        self.player.update()  # applies change_x, change_y, change_angle
        new_position = self.player.position
        self._increment_distance_traveled(old_position, new_position)

        goal_reached = arcade.check_for_collision(self.player, self.goal)
        if goal_reached:
            self.won = True

        hit_obstacles = arcade.check_for_collision_with_list(self.player, self.obstacles)
        if hit_obstacles:
            self.lost = True

        self.obstacles.update()

        if self.lost or self.won:
            self.player.stop()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q:
            raise SystemExit()
        if key == arcade.key.R:
            self.setup(new_obstacles=False)
        if key == arcade.key.N:
            self.setup(new_obstacles=True)
        if key == arcade.key.SPACE:
            self.remove_obstacles_around_player()
        elif key == arcade.key.LEFT:
            self.player.change_x = -5
            self.player.change_y = 0
        elif key == arcade.key.RIGHT:
            self.player.change_x = +5
            self.player.change_y = 0
        elif key == arcade.key.UP:
            self.player.change_x = 0
            self.player.change_y = +5
        elif key == arcade.key.DOWN:
            self.player.change_x = 0
            self.player.change_y = -5


def main():
    """ Main method """
    window = FindFastestWay(1000, 800)
    arcade.run()


if __name__ == "__main__":
    main()
