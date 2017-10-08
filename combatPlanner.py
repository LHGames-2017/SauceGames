from goapy import World, Planner, Action_List
def get_combat_brain(Global_map, Player, Other_players):		
	
	_can_finish_combat = False;
	_is_ennemis_dead = False;
	_is_heavy_damaged = False;
	_run_away = False;
	_is_close_to_ennemis = False;
	_do_nothing = False

	_combat_brain = Planner('can_finish_combat', 'is_ennemis_dead', 'is_heavy_damaged', 'run_away', 'is_close_to_ennemis', 'do_nothing')
	_combat_brain.set_start_state(can_finish_combat=_can_finish_combat, is_ennemis_dead=_is_ennemis_dead, is_heavy_damaged=_is_heavy_damaged, run_away=_run_away, is_close_to_ennemis=_is_close_to_ennemis, do_nothing=_do_nothing)

	_combat_actions = Action_List()
	_combat_actions.add_condition('attack', is_heavy_damaged=False, is_ennemis_dead=False, is_close_to_ennemis=True)
	_combat_actions.add_reaction('attack', is_ennemis_dead=True)

	_combat_actions.add_condition('run_away', can_finish_combat=False, is_heavy_damaged=True, is_close_to_ennemis=True)
	_combat_actions.add_reaction('run_away', is_close_to_ennemis=False)

	_combat_actions.add_condition('heal', is_heavy_damaged=True, is_close_to_ennemis=False)
	_combat_actions.add_reaction('heal', is_heavy_damaged=False)

	_combat_actions.add_condition('do_nothing', do_nothing=False)
	_combat_actions.add_reaction('do_nothing', do_nothing=True)

	_combat_actions.add_condition('go_to_ennemis', is_close_to_ennemis=False)
	_combat_actions.add_reaction('go_to_ennemis',  is_close_to_ennemis=True)

	_combat_actions.set_weight('attack', 30)
	_combat_actions.set_weight('do_nothing', 1000)

	_combat_brain.set_action_list(_combat_actions)


	_combat_brain.set_goal_state(is_ennemis_dead=True)

	return _combat_brain