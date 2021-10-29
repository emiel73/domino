from itertools import combinations_with_replacement
from random import shuffle


class Domino:
    def __init__(self):
        self.full_set = [list(el) for el in (combinations_with_replacement(range(7), 2))]
        self.stock = []
        self.comp = []
        self.player = []
        self.snake = []
        self.status = ''
        self.split_set()

    def split_set(self):
        shuffle(self.full_set)
        self.player = self.full_set[:7]
        self.comp = self.full_set[7:14]
        self.stock = self.full_set[14:]

    def determine_first(self):
        max_double_comp = self.max_double(self.comp)
        max_double_player = self.max_double(self.player)
        if max_double_comp > max_double_player:
            self.snake.append(max_double_comp)
            self.status = 'player'
            self.comp.remove(max_double_comp)
        elif max_double_comp < max_double_player:
            self.snake.append(max_double_player)
            self.status = 'computer'
            self.player.remove(max_double_player)
        else:
            self.split_set()
            self.determine_first()

    @staticmethod
    def max_double(_set):
        try:
            return max(el for el in _set if el[0] == el[1])
        except ValueError:
            return []

    def print_menu(self):
        print('=' * 70, f'Stock size: {len(self.stock)}',
              f'Computer pieces: {len(self.comp)}\n', *self.snake,
              '\nYour pieces:', sep='\n')
        for idx, piece in enumerate(self.player, start=1):
            print(f'{idx}:{piece}')
        input("\nStatus: It's your turn to make a move. Enter your command."
              if self.status == 'player' else
              "\nStatus: Computer is about to make a move. Press Enter to continue...")


def main():
    game = Domino()
    game.determine_first()
    game.print_menu()


if __name__ == '__main__':
    main()
