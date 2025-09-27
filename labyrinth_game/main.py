#!/usr/bin/env python3

from .player_actions import get_input
from .utils import describe_current_room

game_state = {
    "player_inventory": [],  # Инвентарь игрока
    "current_room": "entrance",  # Текущая комната
    "game_over": False,  # Значения окончания игры
    "steps_taken": 0,  # Количество шагов
}


def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while (_ := get_input()) != "quit":
        pass


if __name__ == "__main__":
    main()
