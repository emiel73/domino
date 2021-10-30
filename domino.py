from itertools import combinations_with_replacement, chain
from random import shuffle, choice


class Domino:
    def __init__(self):
        self.full_set = [list(el) for el in (combinations_with_replacement(range(7), 2))]
        self.stock = []
        self.comp = []
        self.human = []
        self.snake = []
        self.active_player = ''
        self.split_set()

    def split_set(self):
        shuffle(self.full_set)
        self.human = self.full_set[:7]
        self.comp = self.full_set[7:14]
        self.stock = self.full_set[14:]

    def determine_first(self):
        max_double_comp = self.max_double(self.comp)
        max_double_human = self.max_double(self.human)
        if max_double_comp > max_double_human:
            self.snake.append(max_double_comp)
            self.active_player = 'human'
            self.comp.remove(max_double_comp)
        elif max_double_comp < max_double_human:
            self.snake.append(max_double_human)
            self.active_player = 'computer'
            self.human.remove(max_double_human)
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
              f'Computer pieces: {len(self.comp)}\n', sep='\n')
        if len(self.snake) <= 6:
            print(*self.snake, sep='')
        else:
            print(*self.snake[:3], '...', *self.snake[-3:], sep='')
        print('\nYour pieces:')
        for idx, piece in enumerate(self.human, start=1):
            print(f'{idx}:{piece}')
        print("\nStatus: It's your turn to make a move. Enter your command."
              if self.active_player == 'human' else
              "\nStatus: Computer is about to make a move. Press Enter to continue...")

    def turn(self):
        if self.active_player == 'human':
            move = self.validate_move()
            self.make_move(move, self.human)
            self.active_player = 'computer'

        elif self.active_player == 'computer':
            input()
            move = choice(range(-(len(self.comp)), len(self.comp)))
            self.make_move(move, self.comp)
            self.active_player = 'human'

    def make_move(self, move, player):
        if move == 0:
            player.append(self.stock.pop())
        elif move > 0:
            self.snake.append(player[move - 1])
            del player[move - 1]
        elif move < 0:
            self.snake.insert(0, player[abs(move) - 1])
            del player[abs(move) - 1]

    def validate_move(self):
        while True:
            move = input()
            try:
                if abs(int(move)) > len(self.human):
                    raise ValueError
                return int(move)
            except ValueError:
                print('Invalid input. Please try again.')

    def end_game(self):
        if not self.human:
            print('Status: The game is over. You won!')
            return True
        elif not self.comp:
            print('Status: The game is over. The computer won!')
            return True
        elif len(self.snake) > 7 and self.snake[0][0] == self.snake[-1][-1]:
            if list(chain.from_iterable(self.snake[0][0])).count(5) == 8:
                print("Status: The game is over. It's a draw!")
                return True
        return False


def main():
    game = Domino()
    game.determine_first()
    game.print_menu()
    while True:
        game.turn()
        game.print_menu()
        if game.end_game():
            break


if __name__ == '__main__':
    main()
