from string import digits
from random import randint
class Game():
    POSITION = (3, 2, 1)
    combinations = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 4, 8), (2, 4, 6), (0, 3, 6), (1, 4, 7), (2, 5, 8))

    def __init__(self, player1, player2):
        self.state = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        modes = {"user": self.player_move, "easy": self.computer_easy, "medium": self.computer_medium, "hard": self.computer_hard}
        self.move = 0
        self.player1 = modes[player1]
        self.player2 = modes[player2]
        self.result = self.engine()

    def output(self):
        field = [[], [], []]
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                if self.state[index] == '_':
                    self.state[index] = ' '
                field[i].append(self.state[index])
        print('-' * 9)
        for i in range(3):
            print('|', *field[i], '|')
        print('-' * 9)

    def player_move(self):
        while True:
            s = input("Enter the coordinates: ").split()
            if len(s) == 2:
                x, y = s
            else:
                x = s[0]
            if x not in digits or y not in digits:
                print("You should enter numbers!")
                continue
            elif int(x) not in self.POSITION or int(y) not in self.POSITION:
                print("Coordinates should be from 1 to 3!")
                continue
            x, y = self.POSITION[int(y) - 1] - 1, int(x) - 1
            if self.state[x * 3 + y] != ' ':
                print("This cell is occupied! Choose another one!")
            else:
                return x, y

    def computer_easy(self):
        print('Making move level "easy"')
        while True:
            x, y = randint(1, 3), randint(1, 3)
            x, y = self.POSITION[int(y) - 1] - 1, int(x) - 1
            if self.state[x * 3 + y] != ' ':
                continue
            else:
                return x, y
    def computer_medium(self):
        print('Making move level "medium"')
        symbols = ('X', 'O') if self.move else ('O', 'X')
        # win // lose condition
        for symbol in symbols:
            for combo in self.combinations:
                count, ram = 0, 0
                for i in range(3):
                    if self.state[combo[i]] == symbol:
                        count += 1
                    if self.state[combo[i]] == ' ':
                        ram = i
                if count == 2 and ram != 0:
                    return combo[ram] // 3, combo[ram] % 3
        # random condition
        while True:
            x, y = randint(1, 3), randint(1, 3)
            x, y = self.POSITION[int(y) - 1] - 1, int(x) - 1
            if self.state[x * 3 + y] != ' ':
                continue
            else:
                return x, y

    def computer_hard(self):
        print('Making move level "hard"')
        best = -99999
        symbols = ('X', 'O') if self.move else ('O', 'X')
        for i in range(9):
            if self.state[i] == " ":
                self.state[i] = symbols[0]
                score = self.minimax(self.state, symbols, 0)
                self.state[i] = " "
                if score > best:
                    best = score
                    ans = i
        return ans // 3, ans % 3



    def minimax(self, board, symbols, depth):
        result = self.check_result()
        score = 0
        if result == f"{symbols[0]} wins":
            score = 1
        if result == f"{symbols[1]} wins":
            score = -1
        if result == "Draw":
            score = 0
        if result != "Game not finished":
            return score
        if depth % 2 == 0:
            best = -9999999
            for i in range(9):
                if self.state[i] == ' ':
                    self.state[i] = symbols[0]
                    score = self.minimax(self.state, symbols, depth + 1)
                    self.state[i] = ' '
                    if score > best:
                        best = score
            return best
        else:
            best = 999999
            for i in range(9):
                if self.state[i] == ' ':
                    self.state[i] = symbols[1]
                    score = self.minimax(self.state, symbols, depth + 1)
                    self.state[i] = ' '
                    if score < best:
                        best = score
            return best


    def engine(self):
        self.output()
        game = True
        time = 0
        while game:
            x, y = self.way()
            time += 1
            self.state[x * 3 + y] = 'X' if self.move else 'O'
            self.output()
            result = self.check_result()
            if result != "Game not finished":
                return result

    def way(self):
        self.move = (self.move + 1) % 2
        if self.move % 2:
            return self.player1()
        return self.player2()

    def check_result(self):
        flags = [False, False, False, False, True]
        conditions = ('Impossible', 'O wins', 'X wins', 'Draw', 'Game not finished')
        for combo in self.combinations:
            if self.state[combo[0]] == self.state[combo[1]] == self.state[combo[2]] == 'X':
                flags[2] = True
            if self.state[combo[0]] == self.state[combo[1]] == self.state[combo[2]] == 'O':
                flags[1] = True
        if (flags[1] == flags[2] == True) or (
                flags[1] == flags[2] == False and abs(self.state.count('X') - self.state.count('O')) > 1):
            flags[0] = True
        if flags[1] == flags[2] == False and self.state.count(' ') == 0:
            flags[3] = True
        for index in range(5):
            if flags[index]:
                return conditions[index]
modes = ('user', 'easy', 'medium', 'hard')

while True:
    commands = input("Input command: ").split()
    if commands[0] == "exit":
        break
    elif len(commands) != 3:
        print("Bad parameters!")
    elif commands[0] == 'start' and commands[1] in modes and commands[2] in modes:
        game = Game(commands[1], commands[2])
        print(game.result)
        print()
    else:
        print("Bad parameters!")
        print()
