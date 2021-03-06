# https://arcade.academy/examples/array_backed_grid_sprites_1.html#array-backed-grid-sprites-1
"""
Array Backed Grid Shown By Sprites

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.

This version syncs the grid to the sprite list in one go using resync_grid_with_sprites.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.array_backed_grid_sprites_1
"""
import arcade
from typing import Tuple, Optional
from random import choice, randint



class GridCell:
    """Grid cell "content" without margin.
    This exposes the geometric properties of the grid cell and allows to
    modify the value of the structure storing all values of a grid.
    """
    def __init__(self, position_lower_left_corner: Tuple[float, float], length: float, flat_index: int, row: int, column: int, value_container):
        self.x_min = position_lower_left_corner[0]
        self.y_min = position_lower_left_corner[1]
        self.length = length
        self.x_max = self.x_min + length
        self.y_max = self.y_min + length
        self.x_center = self.x_min + length / 2
        self.y_center = self.y_min + length / 2
        self.flat_index = flat_index
        self.row = row
        self.column = column
        self._value_container = value_container

    @property
    def value(self):
        return self._value_container[self.flat_index]

    @value.setter
    def value(self, value):
        self._value_container[self.flat_index] = value


class GridOfSquares:
    def __init__(self, row_count: int, column_count: int, grid_length: float, margin_width: float, initial_value=None):
        self.row_count = row_count
        self.column_count = column_count
        self.grid_length = grid_length
        self.margin_width = margin_width
        self.width = grid_length * column_count + margin_width * (column_count + 1)
        self.height = grid_length * row_count + margin_width * (row_count + 1)
        self.data = self.row_count * self.column_count * [initial_value]

    def _index_from(self, row: int, column: int) -> int:
        if row >= self.row_count:
            raise IndexError(f"Grid has only {self.row_count} rows, row {row} was requested.")
        if column >= self.column_count:
            raise IndexError(f"Grid has only {self.column_count} column, column {column} was requested.")
        index = row * self.column_count + column
        return index

    def _row_column_from(self, index: int) -> Tuple[int, int]:
        column = index % self.column_count
        row = index // self.column_count
        return row, column

    def __getitem__(self, key) -> GridCell:
        if isinstance(key, int):
            index = key
            row, column = self._row_column_from(index)
        elif len(key) == 2:
            row, column = key
            index = self._index_from(row, column)
        else:
            raise KeyError(f"Unable to handle index type {type(key)}.")

        if index >= len(self.data):
            raise IndexError
        else:
            x = self.margin_width + column * (self.grid_length + self.margin_width)
            y = self.margin_width + row * (self.grid_length + self.margin_width)
            return GridCell((x, y), self.grid_length, index, row, column, self.data)


    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.data[key] = value
        elif len(key) == 2:
            index = self._index_from(key[0], key[1])
            self.data[index] = value
        else:
            raise KeyError
    
    def cell_at(self, position: Tuple[float, float]) -> Optional[GridCell]:
        x, y = position
        column = int(x // (self.grid_length + self.margin_width))
        row = int(y // (self.grid_length + self.margin_width))
        if 0 <= row < self.row_count and 0 <= column < self.column_count:
            return self[row, column]
        else:
            return None




class Schatzsuche(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, row_count: int, column_count: int, grid_length_px: int, margin_width_px: int, title: str):
        """
        Set up the application.
        """
        # We can store/access the data in this grid using index [row, column].
        self.grid = GridOfSquares(row_count, column_count, grid_length_px, margin_width_px, "unknown")

        super().__init__(self.grid.width, self.grid.height, title)

        self.goal_row = randint(1, row_count-2)
        self.goal_column = randint(1, column_count-2)

        self.number_of_search_operations = 0

        arcade.set_background_color(arcade.color.BLACK)

        # We use the sprites for drawing the grid cells.
        self.grid_sprite_list = arcade.SpriteList()

        for cell in self.grid:
            sprite = self._make_sprite("unknown", cell)
            # show goal for debugging/learning
            # if cell.row == self.goal_row and cell.column == self.goal_column:
                # sprite.color = arcade.color.GREEN
            self.grid_sprite_list.append(sprite)

    def _make_sprite(self, direction: str, cell: GridCell) -> arcade.Sprite:
        if direction in ["right", "up", "down"]:
            resource = ":resources:images/tiles/signRight.png"
        elif direction == "left":
            resource = ":resources:images/tiles/signLeft.png"
        elif direction == "goal":
            resource = ":resources:images/items/gold_1.png"
        elif direction == "unknown":
            resource = ":resources:images/tiles/sandCenter.png"
        else:
            raise ValueError(f"Unknown direction {direction}")

        new_sprite = arcade.Sprite(
            resource,
            center_x=cell.x_center,
            center_y=cell.y_center,
        )

        if direction == "up":
            new_sprite.angle = 90
        elif direction == "down":
            new_sprite.angle = 270

        new_sprite.width = cell.length
        new_sprite.height = cell.length

        return new_sprite

    def resync_grid_with_sprites(self):
        for cell in self.grid:
            if cell.value == "unknown":
                continue
            else:
                new_sprite = self._make_sprite(cell.value, cell)
                self.grid_sprite_list[cell.flat_index] = new_sprite

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        self.grid_sprite_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q:
            raise SystemExit()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        cell = self.grid.cell_at((x, y))
        if cell is not None:
            if cell.value == "unknown":
                if self.goal_row == cell.row and self.goal_column == cell.column:
                    cell.value = "goal"
                    print(f"Yay -- you found it with {self.number_of_search_operations} tries.")
                else:
                    self.number_of_search_operations += 1
                    possible_directions = []
                    if cell.row < self.goal_row:
                        possible_directions.append("up")
                    elif cell.row > self.goal_row:
                        possible_directions.append("down")
                    if cell.column < self.goal_column:
                        possible_directions.append("right")
                    elif cell.column > self.goal_column:
                        possible_directions.append("left")

                    cell.value = choice(possible_directions)

        self.resync_grid_with_sprites()


def main():
    game = Schatzsuche(25, 35, 30, 5, "Schatzsuche")
    arcade.run()


if __name__ == "__main__":
    main()

