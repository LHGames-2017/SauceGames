import time
from goapy import World, Planner, Action_List
from collectPlanner import *
from purchasePlanner import *
from combatPlanner import *

def get_best_plan(Global_map, Player, Other_players):
#if __name__ == '__main__':
	_world = World()
	
	_collect_brain = get_collect_brain(Global_map, Player)
	_purchase_brain = get_purchase_brain(Global_map, Player)
	_combat_brain = get_combat_brain(Global_map, Player, Other_players)

	_world.add_planner(_collect_brain)
	_world.add_planner(_purchase_brain)
	_world.add_planner(_combat_brain)
	
	_world.calculate()
	_sorted_plans = _world.get_plan(debug=True)

	return _sorted_plans[0]

		