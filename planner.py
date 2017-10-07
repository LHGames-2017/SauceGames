import time
from goapy import World, Planner, Action_List

def get_best_plan():
	
	_world = World()
	_collect_brain = Planner('is_full', 'has_enough_ressource', 'is_close_to_ressource', 'is_at_ennemis_house', 'is_in_house')
	_collect_brain.set_start_state(is_full=False, has_enough_ressource=False, is_close_to_ressource=False, is_at_ennemis_house=False, is_in_house=False)
	_collect_brain.set_goal_state(is_full=True)

	_collect_actions = Action_List()
	_collect_actions.add_condition('collect', is_full=False, is_close_to_ressource=True)
	_collect_actions.add_reaction('collect', is_full=True)

	_collect_actions.add_condition('steal', is_full=False, is_at_ennemis_house=True)
	_collect_actions.add_reaction('steal', is_full=True)

	_collect_actions.add_condition('upgrade', has_enough_ressource=True, is_in_house=True)
	_collect_actions.add_reaction('upgrade', has_enough_ressource=False)

	_collect_actions.add_condition('go_to_ressource', is_close_to_ressource=False)
	_collect_actions.add_reaction('go_to_ressource', is_close_to_ressource=True)

	_collect_actions.add_condition('go_to_ennemis_house', is_at_ennemis_house=False)
	_collect_actions.add_reaction('go_to_ennemis_house',  is_at_ennemis_house=True)

	_collect_actions.add_condition('go_to_house', is_full=True, is_in_house=False)
	_collect_actions.add_reaction('go_to_house', is_full=False, is_in_house=True)

	_collect_actions.set_weight('collect', 10)
	_collect_actions.set_weight('steal', 15)

	_collect_brain.set_action_list(_collect_actions)


	_purchase_brain = Planner('has_sword', 'has_shield', 'has_bag', 'has_enough_potion', 'has_40000', 'has_enough_ressource', 'is_close_to_shop')
	_purchase_brain.set_start_state(has_sword=False, has_shield=False, has_bag=False, has_enough_potion=False, has_40000=False, has_enough_ressource=False, is_close_to_shop=False)
	_purchase_brain.set_goal_state(has_sword=True)

	_purchase_action = Action_List()

	_purchase_action.add_condition('purchase_sword', has_sword=False, has_40000=True, is_close_to_shop=True)
	_purchase_action.add_reaction('purchase_sword', has_sword=True, has_40000=False)

	_purchase_action.add_condition('purchase_shield', has_shield=False, has_40000=True, is_close_to_shop=True)
	_purchase_action.add_reaction('purchase_shield', has_shield=True, has_40000=False)

	_purchase_action.add_condition('purchase_bag', has_bag=False, has_40000=True, is_close_to_shop=True)
	_purchase_action.add_reaction('purchase_bag', has_bag=True, has_40000=False)

	_purchase_action.add_condition('purchase_heal_potion', has_enough_potion=False, has_enough_ressource=True, is_close_to_shop=True)
	_purchase_action.add_reaction('purchase_heal_potion', has_enough_potion=True, has_enough_ressource=False)

	_purchase_action.add_condition('go_to_shop', is_close_to_shop=False)
	_purchase_action.add_reaction('go_to_shop', is_close_to_shop=True)

	_purchase_brain.set_action_list(_purchase_action)


	_combat_brain = Planner('can_finish_combat', 'is_ennemis_dead', 'is_heavy_damaged', 'run_away', 'is_close_to_ennemis')
	_combat_brain.set_start_state(can_finish_combat=False, is_ennemis_dead=False, is_heavy_damaged=False, run_away=False, is_close_to_ennemis=False)
	_combat_brain.set_goal_state(is_ennemis_dead=True)

	_combat_actions = Action_List()
	_combat_actions.add_condition('attack', is_heavy_damaged=False, is_ennemis_dead=False, is_close_to_ennemis=True)
	_combat_actions.add_reaction('attack', is_ennemis_dead=True)

	_combat_actions.add_condition('run_away', can_finish_combat=False, is_heavy_damaged=True, is_close_to_ennemis=True)
	_combat_actions.add_reaction('run_away', is_close_to_ennemis=False)

	_combat_actions.add_condition('heal', is_heavy_damaged=True, is_close_to_ennemis=False)
	_combat_actions.add_reaction('heal', is_heavy_damaged=False)

	_combat_actions.add_condition('go_to_ennemis', is_close_to_ennemis=False)
	_combat_actions.add_reaction('go_to_ennemis',  is_close_to_ennemis=True)

	_combat_brain.set_action_list(_combat_actions)

	_world.add_planner(_collect_brain)
	_world.add_planner(_purchase_brain)
	_world.add_planner(_combat_brain)
	
	_t = time.time()
	_path = _world.calculate()
	_took_time = time.time() - _t

	for path in _path:
		print _path.index(path)+1, path['name']

	_sorted_plans = _world.get_plan(debug=True)

	print '\nTook:', _took_time

	return _sorted_plans[0]

		