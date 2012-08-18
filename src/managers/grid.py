class GridManager(object):
    COLLIDE_LEFT = 0x1
    COLLIDE_RIGHT = 0x2
    COLLIDE_UP = 0x4
    COLLIDE_DOWN = 0x8
    COLLIDE_ALL = 0x10

    def __init__(self, rows, cols, tile_width, tile_height):
        self._rows = rows
        self._cols = cols
        self._tile_width = tile_width
        self._tile_height = tile_height
        self._grid = {}

    def set_collision(self, row, col, collision_sides=COLLIDE_ALL):
        if row < 0 or row > self._rows or col < 0 or col > self._cols:
            return
        self._grid[(row, col)] = collision_sides

    # Assumes all from/to differences will be: abs(diff) <= 1
    def check_move(self, from_row, from_col, to_row, to_col):
        row_diff = from_row - to_row
        col_diff = from_col - to_col
        from_tile, from_collision = self._grid[(from_row, from_col)]
        to_tile, to_collision = self._grid[(to_row, to_col)]
        ret_row = to_row
        ret_col = to_col
        # Check for collision with a tile on the x axis.
        if row_diff < 0:
            if to_collision & GridManager.COLLIDE_LEFT == GridManager.COLLIDE_LEFT:
                ret_row += 1
        elif row_diff > 0:
            if to_collision & GridManager.COLLIDE_RIGHT == GridManager.COLLIDE_RIGHT:
                ret_row -= 1
        # Check for collision with a tile on the y axis.
        if col_diff < 0:
            if to_collision & GridManager.COLLIDE_UP == GridManager.COLLIDE_UP:
                ret_col -= 1
        elif col_diff > 0:
            if to_collision & GridManager.COLLIDE_DOWN == GridManager.COLLIDE_DOWN:
                ret_col += 1
        return (ret_row * self._tile_width, ret_col * self._tile_height)
