from goapy import World, Planner, Action_List

def get_purchase_brain(Global_map, Player):

	_has_sword=False
	_has_shield=False
	_has_bag=False
	_has_enough_potion=False
	_has_40000=False
	_has_enough_ressource=False
	_is_close_to_shop=False
	_do_nothing=False

	_purchase_brain = Planner('has_sword', 'has_shield', 'has_bag', 'has_enough_potion', 'has_40000', 'has_enough_ressource', 'is_close_to_shop', 'do_nothing')
	_purchase_brain.set_start_state(has_sword=_has_sword, has_shield=_has_shield, has_bag=_has_bag, has_enough_potion=_has_enough_potion, has_40000=_has_40000, has_enough_ressource=_has_enough_ressource, is_close_to_shop=_is_close_to_shop, do_nothing=_do_nothing)

	_purchase_action = Action_List()

	_purchase_action.add_condition('purchase_sword', has_sword=False, has_40000=True, is_close_to_shop=True)
	_purchase_action.add_reaction('purchase_sword', has_sword=True, has_40000=False)

	_purchase_action.add_condition('purchase_shield', has_shield=False, has_40000=True, is_close_to_shop=True)
	_purchase_action.add_reaction('purchase_shield', has_shield=True, has_40000=False)

	_purchase_action.add_condition('purchase_bag', has_bag=False, has_40000=True, is_close_to_shop=True)
	_purchase_action.add_reaction('purchase_bag', has_bag=True, has_40000=False)

	_purchase_action.add_condition('do_nothing', do_nothing=False)
	_purchase_action.add_reaction('do_nothing', do_nothing=True)

	_purchase_action.add_condition('purchase_heal_potion', has_enough_potion=False, has_enough_ressource=True, is_close_to_shop=True)
	_purchase_action.add_reaction('purchase_heal_potion', has_enough_potion=True, has_enough_ressource=False)

	_purchase_action.add_condition('go_to_shop', is_close_to_shop=False)
	_purchase_action.add_reaction('go_to_shop', is_close_to_shop=True)

	_purchase_action.set_weight('do_nothing', 1000)

	_purchase_brain.set_action_list(_purchase_action)

	#Current goal for purchase is set to nothing
	_purchase_brain.set_goal_state(do_nothing=True)

	return _purchase_brain