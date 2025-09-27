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


def get_input(prompt="> ") -> str:
    """
    Запрашивает у пользователя данные (команду, название, ответ) и возвращает их.

    Args:
        prompt (object): приглашение пользователя к вводу
    """

    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
