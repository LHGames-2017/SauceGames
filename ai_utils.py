import numpy
from structs import *
from heapq import *


def is_resource(cell):
    return cell.Content == TileContent.Resource

def find_closest_resource(grid, player):
    closest_so_far = None
    closest_dist = 100000000
    for row in grid:
        for tile in row:
            tile_pos = Point(tile.X, tile.Y)
            resource_dist =  Point.Distance(player.Position, tile_pos)
            if is_resource(tile) and resource_dist < closest_dist:
                closest_so_far = tile_pos
                closest_dist = resource_dist
    return closest_so_far 

def has_reached_goal(player, goal, reached_dist = 0):
    return Point.Distance(player.Position, goal) == reached_dist

def find_next_pos(player, goal):
    weights = global_map.get_weights()
    # print 'Weights: ' + str(weights)

    if player.Position == goal:
        return goal

    start = (player.Position.X, player.Position.Y)
    goal = (goal.X, goal.Y)

    path = a_star(weights, start, goal)
    # print 'Path: ' + str(path)

    # No path found
    if not path:
        return player.Position

    # Already there
    if len(path) == 0:
        return goal

    next_pos = Point(path[-1][0], path[-1][1])
    return next_pos

def needs_resource(player):
    return player.CarriedRessources != player.CarryingCapacity


def _heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

def a_star(array, start, goal):
    array = numpy.array(array)
    neighbors = [(0,1),(0,-1),(1,0),(-1,0)]

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:_heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + _heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + _heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))
                
    return False


    
