# Start from https://arcade.academy/examples/array_backed_grid_sprites_1.html#array-backed-grid-sprites-1
"""
Array Backed Grid Shown By Sprites

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.

This version syncs the grid to the sprite list in one go using resync_grid_with_sprites.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.array_backed_grid_sprites_1
"""
import arcade
from typing import List, Optional

# Set how many rows and columns we will have
ROW_COUNT = 15
COLUMN_COUNT = 15

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Array Backed Grid Example"


class Ship:
    def __init__(self, length: int, row: int, column: int, orientation):
        self.length = length
        self.row = row
        self.column = column
        self.occupied_space = []
        self.hits = set()
        if orientation not in ["row", "column"]:
            raise ValueError("Unknown orientation {}".format(orientation))
        self.orientation = orientation
        self._compute_occupied_space()

    def _compute_occupied_space(self):
        if self.orientation == "row":
            for column in range(self.column, self.column + self.length):
                self.occupied_space.append((self.row, column))
        if self.orientation == "column":
            for row in range(self.row, self.row + self.length):
                self.occupied_space.append((row, self.column))
    
    def is_at(self, row: int, column: int) -> bool:
        return (row, column) in self.occupied_space

    def hit_at(self, row: int, column: int) -> bool:
        if not self.is_at(row, column):
            raise ValueError(f"Ship is not at {row}, {column}, so cannot get hit.")
        self.hits.add((row, column))

    def is_sunk(self) -> bool:
        return set(self.hits) == set(self.occupied_space)
        


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Set up the application.
        """
        super().__init__(width, height, title)

        self.ships: List[Ship] = []
        self._place_ships()

        # Create a 2 dimensional array. A two dimensional
        # array is simply a list of lists.
        self.grid = []
        for row in range(ROW_COUNT):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append("unknown")  # Append a cell

        arcade.set_background_color(arcade.color.BLACK)

        self.grid_sprite_list = arcade.SpriteList()

        # Create a list of solid-color sprites to represent each grid location
        for row in range(COLUMN_COUNT):
            for column in range(ROW_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)


    def _place_ships(self):
        ship = Ship(4, 4, 4, "column")
        self.ships.append(ship)

    def _get_ship_at(self, row: int, column: int) -> Optional[Ship]:
        for ship in self.ships:
            if ship.is_at(row, column):
                return ship
        return None


    def resync_grid_with_sprites(self):
        self.shape_list = arcade.ShapeElementList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # We need to convert our two dimensional grid to our
                # one-dimensional sprite list. For example a 10x10 grid might have
                # row 2, column 8 mapped to location 28. (Zero-basing throws things
                # off, but you get the idea.)
                # ALTERNATIVELY you could set self.grid_sprite_list[pos].texture
                # to different textures to change the image instead of the color.
                pos = row * COLUMN_COUNT + column
                grid_value = self.grid[row][column]
                if grid_value == "unknown":
                    self.grid_sprite_list[pos].color = arcade.color.WHITE
                elif grid_value == "ship":
                    self.grid_sprite_list[pos].color = arcade.color.BROWN
                elif grid_value == "sunk ship":
                    self.grid_sprite_list[pos].color = arcade.color.BLACK
                elif grid_value == "water":
                    self.grid_sprite_list[pos].color = arcade.color.BLUE
                else:
                    raise ValueError(f"Grid value {grid_value} not expected")

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        self.grid_sprite_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change the x/y screen coordinates to grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row < ROW_COUNT and column < COLUMN_COUNT:

            if self.grid[row][column] == "unknown":
                hit_ship = self._get_ship_at(row, column)
                if hit_ship is None:
                    self.grid[row][column] = "water"
                else:
                    hit_ship.hit_at(row, column)
                    if hit_ship.is_sunk():
                        for ship_row, ship_col in hit_ship.occupied_space:
                            self.grid[ship_row][ship_col] = "sunk ship"
                    else:
                        self.grid[row][column] = "ship"
            else:
                print(f"Grid Cell ({row}, {column}) was already known")

        self.resync_grid_with_sprites()


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
