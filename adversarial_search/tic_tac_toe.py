from copy import deepcopy
import time

State = tuple[int, list[list[int | None]]]  # Tuple of player (whose turn it is),
                                            # and board
Action = tuple[int, int]  # Where to place the player's piece

class Game:
    def initial_state(self) -> State:
        return (0, [[None, None, None], [None, None, None], [None, None, None]])

    def to_move(self, state: State) -> int:
        player_index, _ = state
        return player_index

    def actions(self, state: State) -> list[Action]:
        _, board = state
        actions = []
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    actions.append((row, col))
        return actions

    def result(self, state: State, action: Action) -> State:
        _, board = state
        row, col = action
        next_board = deepcopy(board)
        next_board[row][col] = self.to_move(state)
        return (self.to_move(state) + 1) % 2, next_board

    def is_winner(self, state: State, player: int) -> bool:
        _, board = state
        for row in range(3):
            if all(board[row][col] == player for col in range(3)):
                return True
        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        return all(board[i][2 - i] == player for i in range(3))

    def is_terminal(self, state: State) -> bool:
        _, board = state
        if self.is_winner(state, (self.to_move(state) + 1) % 2):
            return True
        return all(board[row][col] is not None for row in range(3) for col in range(3))

    def utility(self, state, player):
        assert self.is_terminal(state)
        if self.is_winner(state, player):
            return 1
        if self.is_winner(state, (player + 1) % 2):
            return -1
        return 0

    def print(self, state: State):
        _, board = state
        print()
        for row in range(3):
            cells = [
                ' ' if board[row][col] is None else 'x' if board[row][col] == 0 else 'o'
                for col in range(3)
            ]
            print(f' {cells[0]} | {cells[1]} | {cells[2]}')
            if row < 2:
                print('---+---+---')
        print()
        if self.is_terminal(state):
            if self.utility(state, 0) > 0:
                print(f'P1 won')
            elif self.utility(state, 1) > 0:
                print(f'P2 won')
            else:
                print('The game is a draw')
        else:
            print(f'It is P{self.to_move(state)+1}\'s turn to move')

def minimax_search(game: Game, state: State) -> Action | None:
    player = game.to_move(state)                                # Get the current player whose turn it is
    value, move = max_value(game, state)                        # Start the minimax algorithm by finding the maximum value move for the current player
    return move                                                 # Return the best action (move) found by the minimax search

def max_value(game: Game, state: State) -> tuple[float, float | None]:
    if (game.is_terminal(state)): return game.utility(state, player), None  # Check if the game is in a terminal state (i.e., if the game has ended), return the utility of the current state for the player
    v, move = float('-inf'), float('-inf')                                  # Initialize v as negative infinity because we are looking for the maximum value and initialize 'move' as negative infinity, will be updated with the best action
    for a in game.actions(state):                                           # Loop over all possible actions that can be taken from the current state
        v2, a2 = min_value(game, game.result(state, a))                     # Get the value of the resulting state after Player 2 (minimizer) takes their action
        if (v2 > v):                                                        # If the value found (v2) is better than the current best (v), update v and the move
            v, move = v2, a                                                 # Keep track of the best value and associated action
    return v, move                                                          # Return the highest value found (v) and the corresponding best action (move)

def min_value(game: Game, state: State) -> tuple[float, float | None]:
    if (game.is_terminal(state)): return game.utility(state, player), None  # Check if the game is in a terminal state (i.e., if the game has ended), return the utility of the current state for the player
    v, move = float('inf'), float('inf')                                    # Initialize v as negative infinity because we are looking for the maximum value and initialize 'move' as negative infinity, will be updated with the best action
    for a in game.actions(state):                                           # Loop over all possible actions that can be taken from the current state
        v2, a2 = max_value(game, game.result(state, a))                     # Get the value of the resulting state after Player 1 (maximizer) takes their action
        if (v2 < v):                                                        # If the value found (v2) is better (lower) than the current best (v), update v and the move
            v, move = v2, a                                                 # Keep track of the best (smallest) value and associated action
    return v, move                                                          # Return the lowest value found (v) and the corresponding best action (move)

def alpha_beta_search(game: Game, state: State) -> Action | None:
    player = game.to_move(state)                                            # Get the current player whose turn it is
    value, move = max_value_ab(game, state, float('-inf'), float('inf'))    # Start alpha-beta pruning search with initial alpha and beta values (-inf and +inf)
    return move                                                             # Return the best action (move) found by the alpha-beta search

def max_value_ab(game: Game, state: State, alpha, beta) -> tuple[float, float]:
    if (game.is_terminal(state)): return game.utility(state, player), None  # If the game has ended, return the utility of the current state for the player
    v = float('-inf')                                                       # Initialize v as negative infinity because we are looking for the maximum value
    for a in game.actions(state):                                           # Loop over all possible actions that can be taken from the current state
        v2, a2 = min_value_ab(game, game.result(state, a), alpha, beta)     # Get the value of the resulting state after Player 2 (minimizer) takes their action
        if (v2 > v):                                                        # If the value found (v2) is better than the current best (v), update v and the move
            v, move = v2, a                                                 # Keep track of the best value and associated action
            alpha = max(alpha, v)                                           # Update alpha to reflect the best value found so far by the maximizer
        if (v >= beta): return v, move                                      # Beta cutoff: f v is greater than or equal to beta, we can prune the remaining branches. Return immediately because further exploration is unnecessary (pruning occurs)
    return v, move                                                          # Return the highest value found (v) and the corresponding best action (move)

def min_value_ab(game: Game, state: State, alpha, beta) -> tuple[float, float | None]:
    if (game.is_terminal(state)): return game.utility(state, player), None  # If the game has ended, return the utility of the current state for the player
    v, move = float('inf'), float('inf')                                    # Initialize v as positive infinity because we are looking for the minimum value
    for a in game.actions(state):                                           # Loop over all possible actions that can be taken from the current state
        v2, a2 = max_value_ab(game, game.result(state, a), alpha, beta)     # Get the value of the resulting state after Player 1 (maximizer) takes their action
        if (v2 < v):                                                        # If the value found (v2) is better (lower) than the current best (v), update v and the move
            v, move = v2, a                                                 # Keep track of the best (smallest) value and associated action
            beta = min(beta, v)                                             # Update beta to reflect the best value found so far by the minimizer
        if (v <= alpha): return v, move                                     # Alpha cutoff: if v is less than or equal to alpha, we can prune the remaining branches. Return immediately because further exploration is unnecessary (pruning occurs)
    return v, move                                                          # Return the lowest value found (v) and the corresponding best action (move)

game = Game()

state = game.initial_state()
game.print(state)
while not game.is_terminal(state):
    player = game.to_move(state)

    start_time = time.time()
    #action = minimax_search(game, state) # The player whose turn it is
                                         # is the MAX player
    action = alpha_beta_search(game, state)
    end_time = time.time()
    print(f'Move runtime: {end_time-start_time} s')
    
    print(f'P{player+1}\'s action: {action}')
    assert action is not None
    state = game.result(state, action)
    game.print(state)
