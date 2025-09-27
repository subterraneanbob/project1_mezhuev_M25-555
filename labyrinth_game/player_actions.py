def show_inventory(game_state: dict):
    """
    Выводит предметы в инвентаре или сообщение, что инвентарь пуст.

    Args:
        game_state (dict): Текущее состояние игры.
    """

    if inventory := game_state["player_inventory"]:
        print(f"Инвентарь: {', '.join(inventory)}")
    else:
        print("Инвентарь пуст.")
