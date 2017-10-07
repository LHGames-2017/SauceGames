from flask import Flask, request
from structs import *
from map_utils import GlobalMap
from ai_utils import a_star
import json
import numpy

app = Flask(__name__)

def create_action(action_type, target):
    actionContent = ActionContent(action_type, target.__dict__)
    return json.dumps(actionContent.__dict__)

def create_move_action(target):
    return create_action("MoveAction", target)

def create_attack_action(target):
    return create_action("AttackAction", target)

def create_collect_action(target):
    return create_action("CollectAction", target)

def create_steal_action(target):
    return create_action("StealAction", target)

def create_heal_action():
    return create_action("HealAction", "")

def create_purchase_action(item):
    return create_action("PurchaseAction", item)

def deserialize_map(serialized_map):
    """
    Fonction utilitaire pour comprendre la map
    """
    serialized_map = serialized_map[1:]
    rows = serialized_map.split('[')
    column = rows[0].split('{')
    deserialized_map = [[Tile() for x in range(20)] for y in range(20)]
    for i in range(len(rows) - 1):
        column = rows[i + 1].split('{')

        for j in range(len(column) - 1):
            infos = column[j + 1].split(',')
            end_index = infos[2].find('}')
            content = int(infos[0])
            x = int(infos[1])
            y = int(infos[2][:end_index])
            deserialized_map[i][j] = Tile(content, x, y)

    return deserialized_map

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

def bot():
    """
    Main de votre bot.
    """
    map_json = request.form["map"]

    # Player info

    encoded_map = map_json.encode()
    map_json_dict = json.loads(encoded_map)

    p = map_json_dict["Player"]
    pos = p["Position"]
    x = pos["X"]
    y = pos["Y"]
    house = p["HouseLocation"]
    player = Player(p["Health"], p["MaxHealth"], Point(x,y),
                    Point(house["X"], house["Y"]), p["Score"],
                    p["CarriedResources"], p["CarryingCapacity"],
                    p["AttackPower"], p["Defence"], p["TotalResources"])

    # Map
    serialized_map = map_json_dict["CustomSerializedMap"]
    deserialized_map = deserialize_map(serialized_map)

    otherPlayers = []

    for players in map_json_dict["OtherPlayers"]:
        player_info = players["Value"]
        p_pos = player_info["Position"]
        player_info = PlayerInfo(player_info["Health"],
                                    player_info["MaxHealth"],
                                    Point(p_pos["X"], p_pos["Y"]))

        otherPlayers.append(player_info)

    global_map.update_grid(deserialized_map)
    # print str(global_map)

    # print str(player)

    action = None
    if needs_resource(player):
        goal = find_closest_resource(deserialized_map, player)
        # print 'Target: ' + str(goal)
        if not has_reached_goal(player, goal, 1):
            next_pos = find_next_pos(player, goal)
            # print 'Next pos: ' + str(next_pos) 
            action = create_move_action(next_pos)
        else:
            action = create_collect_action(goal)
    else:    
        next_pos = find_next_pos(player, player.HouseLocation)
        action = create_move_action(next_pos)
            
    # return decision
    return action

@app.route("/", methods=["POST"])
def reponse():
    """
    Point d'entree appelle par le GameServer
    """
    resp = bot()
    # print resp
    return resp

if __name__ == "__main__":
    global global_map
    global_map = GlobalMap()
    app.run(host="0.0.0.0", port=8080, debug=True)
