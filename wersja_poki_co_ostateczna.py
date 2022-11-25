from random import randint
from ast import literal_eval

BLANK = 0
PL_X = 1
PL_O = -1


class Board:
    def __init__(self):
        self.board = [[BLANK for _ in range(3)] for _ in range(3)]

    def print_board(self): #printuje plansze
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

    def is_board_full(self):  # sprawdza czy pelna plansza, wtedy remis
        av_moves = self.available_moves()
        if len(av_moves) == 0:
            return True
        return False

    def is_winning(self, player): #sprawdza czy ktos wygral
        for row in range(3):  # poziomo
            if self.get_current_state()[row][0] != BLANK and self.get_current_state()[row][0] == self.get_current_state()[row][1] == self.get_current_state()[row][2] and self.get_current_state()[row][0] == player:
                return True

        for col in range(3):  # pionowo
            if self.get_current_state()[0][col] != BLANK and self.get_current_state()[0][col] == self.get_current_state()[1][col] == self.get_current_state()[2][col] and self.get_current_state()[0][col] == player:
                return True

        # skos od lewy gorny do prawy dolny
        if self.get_current_state()[0][0] != BLANK and self.get_current_state()[0][0] == self.get_current_state()[1][1] == self.get_current_state()[2][2] and self.get_current_state()[0][0] == player:
            return True

        # skos od prawy gorny do lewy dolny
        if self.get_current_state()[0][2] != BLANK and self.get_current_state()[0][2] == self.get_current_state()[1][1] == self.get_current_state()[2][0] and self.get_current_state()[0][2] == player:
            return True
        # jesli nikt nie wygral
        return False

    def heuristic_function(self): #heura
        if self.is_winning(PL_X):
            value = 1
        elif self.is_winning(PL_O):
            value = -1
        else:
            value = 0

        return value

    def somebody_won(self): #sprawdza czy istnieje zwyciezca
        if self.is_winning(PL_X) or self.is_winning(PL_O):
            return True
        return False

    def available_moves(self): #zwraca liste mozliwych ruchow
        av_moves = [(x, y) for x in range(3)
                    for y in range(3) if self.get_current_state()[x][y] == BLANK]
        return av_moves

    def make_move(self, move, player): #wykonanie ruchu
        self.get_current_state()[move[0]][move[1]] = player

    
    def minimax(self, depth, player):
        if player == PL_X:
            best_move = [-1, -1, -float('inf')]
        elif player == PL_O:
            best_move = [-1, -1, float('inf')]

        if self.somebody_won() or depth == 0:
            best_score = self.heuristic_function()  # prawdopodobnie do wyjebania
            return [-1, -1, best_score]

        av_moves = self.available_moves()

        for move in av_moves:
            self.get_current_state()[move[0]][move[1]] = player
            best_score = self.minimax(depth - 1, -player)
            self.get_current_state()[move[0]][move[1]] = 0
            best_score[0], best_score[1] = move[0], move[1]

            if player == PL_X and best_score[2] > best_move[2]:
                best_move = best_score
            elif player == PL_O and best_score[2] < best_move[2]:
                best_move = best_score

        return best_move

    def ai_move(self, player): #wykonuje ruch komputera

        depth = len(self.available_moves())
        if depth == 9:
            move = (randint(0, 2), randint(0, 2))
        else:
            move = self.minimax(depth, player)
            move = (move[0], move[1])

        self.make_move(move, player)


def main():
    board = Board()
    player = PL_X

    while True:

        board.ai_move(PL_O)
        board.print_board()
        board.ai_move(PL_X)
        board.print_board()
        if board.is_winning(PL_O):
            print("Wygralo O")
            return
        elif board.is_winning(PL_X):
            print("Wygral X")
            return
        elif board.is_board_full():
            print("Remis")
            return
        # your_move = literal_eval(input())
        # board.make_move(your_move, player)


if __name__ == "__main__":
    main()
