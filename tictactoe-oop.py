# Repo: https://github.com/ziaroque/game-tic-tac-toe

from dataclasses import dataclass
from termcolor import colored
import random
import time
import re
import os

GAME_COLOR = 'light_blue'
PLAYER1_COLOR = 'light_green'
PLAYER2_COLOR = 'light_magenta'

class Game:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.player1 = None
        self.player2 = None
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self.winner = None
        self.round = 1
        self.scores = {'player1': 0, 'player2': 0, 'draw': 0}

    def reset_board(self):
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

    def start(self):
        os.system('clear')
        self.show_title()
        self.set_players()
        print('The game will begin in 3.. 2.. 1..')
        time.sleep(3)
        
    @staticmethod
    def show_title():
        title = '''
    █████ █ ████    █████  ███  ████   █████ █████ █████
      █   █ █         █   █   █ █        █   █   █ █
      █   █ █    █    █   █████ █    █   █   █   █ ███
      █   █ █         █   █   █ █        █   █   █ █
      █   █ ████      █   █   █ ████     █   █████ █████
                '''
        print(colored(title, GAME_COLOR))

    def set_players(self):
        player1_name = self.ask_player_name(True)
        player1_marker = None
        player1_is_first_turn = random.randint(1, 2) == 1
        player2_name = None
        player2_marker = None
        player2_is_first_turn = not player1_is_first_turn
        player2_is_computer = False
        while True:
            input_value = input('\nHey ' + colored(f'{player1_name}', PLAYER1_COLOR) + ', choose between the markers [' + colored('X', GAME_COLOR) + '] or [' + colored('O',GAME_COLOR) + ']: ')
            marker = str(input_value).upper()
            if marker in ['X', 'O']:
                player1_marker = marker
                player2_marker = 'O' if player1_marker == 'X' else 'X'
                break
            print('Try again!\n')
        print('\nYour chosen marker is ' + colored(f'{player1_marker}', PLAYER1_COLOR) + '. This will not affect who gets the first turn in the game.')
        print('The first player to make a move will be chosen randomly!\n')
        while True:
            input_value = input(f'Do you want to play vs a [' + colored('C', GAME_COLOR) + ']omputer or another [' + colored('H',GAME_COLOR) + ']uman? ')
            opponent = str(input_value).upper()
            if opponent == 'C':
                player2_name = 'Computer'
                player2_is_computer = True
                break
            elif opponent == 'H':
                while player1_name == player2_name or player2_name is None:
                    player2_name = self.ask_player_name()
                    if player1_name == player2_name:
                        print('Sorry! Please try a different name.')
                break
            else:
                print('Try again!\n')
        print('\nIt\'s ' + colored(player1_name, PLAYER1_COLOR) + ' vs ' + colored(player2_name, PLAYER2_COLOR) + '. Let\'s play Tic-Tac-Toe!!\n')
        if player1_is_first_turn:
            print(colored(f'{player1_name}', PLAYER1_COLOR) + ' will play first!\n')
        else:
            print(colored(f'{player2_name}', PLAYER2_COLOR) + ' will play first!\n')
        self.player1 = Player(player1_name, player1_marker, player1_is_first_turn, False, PLAYER1_COLOR)
        self.player2 = Player(player2_name, player2_marker, player2_is_first_turn, player2_is_computer, PLAYER2_COLOR)
    
    def ask_player_name(self, is_player1=False):
        while True:
            input_value = input('\nHello there! What\'s your first name? ' if is_player1 else '\nWhat\'s your opponent\'s first name? ')
            regex = r'^[A-Za-z\-\'\. ]+$'
            if re.match(regex, input_value) and len(input_value) <= 15:
                name = str(input_value).capitalize()
                return name
            print('Try again!\n')

    def repaint_screen(self):
        os.system('clear')
        self.show_title()
        self.print_scores()
        self.print_board()

    def print_scores(self):
        print('\n')
        print(colored('SCORES', GAME_COLOR))
        print(f'{self.player1.name} (' + colored(self.player1.marker, self.player1.color) + ') = {}'.format(self.scores['player1']))
        print(f'{self.player2.name} (' + colored(self.player2.marker, self.player2.color) + ') = {}'.format(self.scores['player2']))
        print('Draw = {}'.format(self.scores['draw']))
        print('\n')

    def print_board(self):
        print('     0   1   2 ')
        print('    -----------')
        for i, row in enumerate(self.board):
            if i > 0:
                print('    ---+---+---')
            print(f' {i} | ' + ' | '.join(' ' if marker is None else colored(marker, self.player1.color if marker == self.player1.marker else self.player2.color) for marker in row) + ' |')
        print('    -----------')
        print(colored('     ROUND', GAME_COLOR) + ' #{}'.format(self.round))
        print('\n')
    
    def play(self):
        current_player = self.player1 if self.player1.is_first_turn else self.player2
        while len(self.check_available_moves()) > 0:
            coor = current_player.get_move(self.check_available_moves())
            self.make_move(coor, current_player.marker)
            self.repaint_screen()
            self.check_winner()
            if self.winner is not None:
                if self.winner == self.player1.marker:
                    self.scores['player1'] += 1
                    self.repaint_screen()
                    print('!!! ' + colored(f'{self.player1.name}', self.player1.color) + ' WON !!!')
                else:
                    self.scores['player2'] += 1
                    self.repaint_screen()
                    print('!!! ' + colored(f'{self.player2.name}', self.player2.color) + 'WON !!!')
                break
            if len(self.check_available_moves()) == 0:
                self.scores['draw'] += 1
                self.repaint_screen()
                print('\nIT\'S A DRAW!!!')
            current_player = self.player2 if current_player == self.player1 else self.player1
    
    def check_available_moves(self):
        available_moves = []
        for x, row in enumerate(self.board):
            for y, coor in enumerate(row):
                if coor is None:
                    available_moves.append([x, y])
        return available_moves
    
    def make_move(self, coor, marker):
        self.board[coor[0]][coor[1]] = marker

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                self.winner = self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i]:
                self.winner = self.board[0][i]
        if (self.board[0][0] == self.board[1][1] == self.board[2][2]) or (self.board[0][2] == self.board[1][1] == self.board[2][0]):
            self.winner = self.board[1][1]

    def check_status(self):
        while True:
            input_value = input('\n[' + colored('C', GAME_COLOR) + ']ontinue Game / [' + colored('R', GAME_COLOR) + ']eset Game / [' + colored('Q', GAME_COLOR) + ']uit Game ? ')
            status = str(input_value).upper()
            if status in ['C', 'R', 'Q']:
                if status == 'C':
                    return 'continue'
                elif status == 'R':
                    return 'reset'
                return 'quit'
            print('Try again!')

@dataclass
class Player:
    name: str = None
    marker: str = None
    is_first_turn: bool = False
    is_computer: bool = False
    color: str = None

    def get_move(self, available_moves):
        if self.is_computer:
            return self.computer_move(available_moves)
        return self.ask_move(available_moves)
    
    def computer_move(self, available_moves):
        time.sleep(0.5)
        return random.choice(available_moves)

    def ask_move(self, available_moves):
        while True:
            input_value = input(f'\n{self.name} (' + colored(f'{self.marker}', self.color) + '), it\'s your turn. Input move [' + colored('row', GAME_COLOR) + ',' + colored('col', GAME_COLOR) + ']: ')
            regex = r'^[0-2]\,[0-2]$'
            if re.match(regex, input_value):
                x = int(input_value.split(',')[0])
                y = int(input_value.split(',')[1])
                coor = [x, y]
                if coor in available_moves:
                    return coor
            print('Try again!\n')

def main():
    game = Game()
    game.start()
    while True:
        game.repaint_screen()
        game.play()
        status = game.check_status()
        if status == 'quit':
            break
        elif status == 'continue':
            game.reset_board()
            game.round += 1
        else:
            game.reset()
            game.start()
    print('\nX X  ' + colored('GAME OVER!', GAME_COLOR) + '  X X')
    print('\nThanks for playing!')

if __name__ == "__main__":
    main()
