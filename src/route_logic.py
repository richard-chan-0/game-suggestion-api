from src.database.entity_factory import create_player, create_game, create_reference
from src.database.wrapper import database_wrapper


def ready_player(request):
    steam_id = request.form.get("steam_id")
    first_name = request.form.get("first_name").lower()
    last_name = request.form.get("last_name").lower()

    player = create_player(steam_id, first_name, last_name)
    database_wrapper.player_wrapper.add_player(player)
    return "player successfully added", 200


def refresh_shared_games():
    steam_ids = database_wrapper.player_wrapper.get_all_players()
    for id in steam_ids:
        pass
        # TODO: fix this
        # database_wrapper.player_wrapper.clean_player_games(id)
        # games = get_owned_games(id)
    #     for app_id, game_name in games:
    #         database_wrapper.game_wrapper.add_game(create_game(app_id, game_name))
    #         add_player_game_ref(create_reference(id, app_id))
    # return "table refreshed", 200


def get_shared_games(request):
    steam_ids = request.form.getlist("steam_ids")
    games = database_wrapper.get_shared_games(steam_ids), 200
    if games:
        return games, 200
    else:
        return "no shared games", 200
