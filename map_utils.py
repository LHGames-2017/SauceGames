from structs import *

#Vrai map (taille reelle)
class GlobalMap:
    def __init__(self):
        self.grid = []
        for i in range(1000):
            self.grid.append([])
            for j in range(1000):
                self.grid[i].append(None)

    def __str__(self):
        result = ''
        for line in self.grid:
            result += ' '.join(str(tile) if tile is not None else '' for tile in line) + '\n'
        return result

    def update_grid(self, grid):
        for row in grid:
            for tile in row:
                if tile.Content is not None:
                    self.grid[tile.X][tile.Y] = tile.Content 

    @staticmethod
    def _get_weight(cell):
        UNREACHABLE_WEIGHT = 100
        if cell == TileContent.Empty or\
            cell == TileContent.House:
            return 0
        # elif cell == TileContent.Wall or\
        #      cell == TileContent.Lava or\
        #      cell == TileContent.Player or\
        #      cell == TileContent.Resource or\
        #      cell == TileContent.Shop:
        return UNREACHABLE_WEIGHT

    def get_weights(self):
        return [[GlobalMap._get_weight(cell) for cell in line] for line in self.grid]   

    
        