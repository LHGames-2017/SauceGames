from flask import Flask, request
from structs import *
from map_utils import GlobalMap
from ai_utils import *
from planner import *
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
                    p["CarriedResources"], p["CarryingCapacity"])

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

    print str(player)

    best_plan = get_best_plan(deserialized_map, player, otherPlayers)
    print best_plan
    
    closest_resource = find_closest_resource(global_map, player)
    action = None
    if best_plan == 'go_to_ressources':
            next_pos = find_next_pos(player, closest_resource)
            # print 'Next pos: ' + str(next_pos) 
            action = create_move_action(next_pos)
    
    elif best_plan == 'collect':
            action = create_collect_action(closest_resource)

    elif best_plan == 'go_to_house':    
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
