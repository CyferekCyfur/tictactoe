from enum import Flag
import random


BLANK = 0
PL_X = 1
PL_O = -1


class Board:
    def __init__(self):
        self.board = [[BLANK for _ in range(3)] for _ in range(3)]
        #self.whose_turn = 1

    def print_board(self):
        print("-------------")
        for row in self.board:
            for elem in row:
                if elem == BLANK:
                    print(f'|   ', end='')
                elif elem == PL_X:
                    print(f'| X ', end='')
                else:
                    print(f'| O ', end='')
            print('|')
            print("-------------")

    def get_current_state(self):
        return self.board

    def available_moves(self):  # mozliwe ruchy do wykonania w obecnym ukladzie
        av_moves = [(x, y) for x in range(3)
                    for y in range(3) if self.get_current_state()[x][y] == BLANK]
        return av_moves

    def is_board_full(self):  # sprawdza czy pelna plansza, wtedy najprawdopodobniej remis
        av_moves = self.available_moves()
        if len(av_moves) == 0:
            return True
        return False

    def make_move(self, move, player):  # wykonuje ruch (X -> 1, O -> -1, spacja -> 0)
        self.get_current_state()[move[0]][move[1]] = player

    def winner_result(self):  # sprawdza kto wygral gre
        for row in range(3):  # poziomo
            if self.get_current_state()[row] == [PL_X for _ in range(3)]:
                return True, PL_X
            elif self.get_current_state()[row] == [PL_O for _ in range(3)]:
                return True, PL_O

        for col in range(3):  # pionowo
            if self.get_current_state()[0][col] != BLANK and self.get_current_state()[0][col] == self.get_current_state()[1][col] == self.get_current_state()[2][col]:
                return True, self.get_current_state()[0][col]

        # skos od lewy gorny do prawy dolny
        if self.get_current_state()[0][0] != BLANK and self.get_current_state()[0][0] == self.get_current_state()[1][1] == self.get_current_state()[2][2]:
            return True, self.get_current_state()[1][1]

        # skos od prawy gorny do lewy dolny
        if self.get_current_state()[0][2] != BLANK and self.get_current_state()[0][2] == self.get_current_state()[1][1] == self.get_current_state()[2][0]:
            return True, self.get_current_state()[1][1]
        # jesli nikt nie wygral
        return False, BLANK

    def print_results(self):    # printuje kto wygral
        if self.winner_result()[0]:
            if self.winner_result()[1] == PL_X:
                print('X won')
            else:
                print('O won')
        elif self.is_board_full():
            print('Draw')

    def rating(self):   # ocenia, czy dany ruch jest optymalny
        if self.winner_result()[0] and self.winner_result()[1] == PL_X:
            return 10
        elif self.winner_result()[0] and self.winner_result()[1] == PL_O:
            return -10
        else:
            return 0

    def alphabeta(self, depth, player, alpha, beta):
        x = -1  # sometimes x and y are not changing in recursion, causing
        y = -1  # the remove of the last element of the last row (2, 2)
        # for x = none and y = none there will be nonetype error, shit like that
        if self.winner_result()[0] or depth == 0:
            return x, y, self.rating()
        # weird things happening with depth, not sure if it's working properly
        print(depth)

        av_moves = self.available_moves()
        for move in av_moves:
            self.make_move(move, player)
            best_move = self.alphabeta(
                depth-1, -player, alpha, beta)   # recursion
            if PL_X == player and best_move[2] > alpha:
                alpha = best_move[2]
                x = move[0]
                y = move[1]
            elif PL_O == player and best_move[2] < beta:
                beta = best_move[2]
                # problem probably there
                x = move[0]
                y = move[1]
            # sign is not removed from the board (sometimes)
            self.make_move((x, y), BLANK)
            # self.print_board()
            if beta <= alpha:
                break

        if PL_O == player:
            return x, y, beta
        else:
            return x, y, alpha

    def ai(self, depth, player):    # ruch sztucznej inteligencji
        if len(self.available_moves()) == 9:  # randomowo losuje miejsce z ktorego zaczynamy rozgrywke
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            self.make_move((x, y), -player)
            self.print_board()

        else:
            x, y, _ = self.alphabeta(
                depth-1, -player, -float('inf'), float('inf'))
            move = (x, y)
            self.make_move(move, -player)

    def play(self):  # petla gry
        player = PL_X

        while not self.is_board_full() or not self.winner_result()[0]:
            self.gameplay(player)
            player = -player

        self.print_results()

    def gameplay(self, player):  # wybor gracza do podania dla sztucznej i
        if player == PL_O:
            # we want depth to determine how effective is the algorithm (eg. for depth = 9 always draw, not so effective for d=3 or 4)

            self.ai(9, player)
        else:
            self.ai(9, -player)


if __name__ == "__main__":
    board = Board()
    board.play()


# nie wiemy jak napisac heurystyke, ktora jest raczej potrzebna, zeby glebokosc mniejsza niz maksymalna (9) dzialala optymalnie i wyznaczala najlepszy ruch
