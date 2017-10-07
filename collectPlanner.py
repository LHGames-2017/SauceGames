from goapy import World, Planner, Action_List
def get_collect_brain(Global_map, Player):	
	
	_is_full = (Player.CarriedRessources >= Player.CarryingCapacity)
	_has_enough_ressource=False
	_is_close_to_ressource=False
	_is_at_ennemis_house=False
	_is_in_house= (Player.Position == Player.HouseLocation)
	_do_nothing=False

	_collect_brain = Planner('is_full', 'has_enough_ressource', 'is_close_to_ressource', 'is_at_ennemis_house', 'is_in_house', 'do_nothing')
	_collect_brain.set_start_state(is_full=_is_full, has_enough_ressource=_has_enough_ressource, is_close_to_ressource=_is_close_to_ressource, is_at_ennemis_house=_is_at_ennemis_house, is_in_house=_is_in_house, do_nothing=_do_nothing)
	_collect_brain.set_goal_state(is_full=!_is_full)

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

	_collect_actions.add_condition('do_nothing', do_nothing=False)
	_collect_actions.add_reaction('do_nothing', do_nothing=True)

	_collect_actions.set_weight('collect', 10)
	_collect_actions.set_weight('steal', 15)
	_collect_actions.set_weight('do_nothing', 1000)

	_collect_brain.set_action_list(_collect_actions)

	return _collect_brain