import math

State = tuple[int, int] # Tuple of player (whose turn it is),
                        # and the number to be decreased
Action = str  # Decrement (number <- number-1) or halve (number <- number / 2)

class Game:
    def __init__(self, N: int):
        self.N = N

    def initial_state(self) -> State:
        return 0, self.N

    def to_move(self, state: State) -> int:
        player, _ = state
        return player

    def actions(self, state: State) -> list[Action]:
        return ['--', '/2']

    def result(self, state: State, action: Action) -> State:
        _, number = state
        if action == '--':
            return (self.to_move(state) + 1) % 2, number - 1
        else:
            return (self.to_move(state) + 1) % 2, number // 2  # Floored division

    def is_terminal(self, state: State) -> bool:
        _, number = state
        return number == 0

    def utility(self, state: State, player: int) -> float:
        assert self.is_terminal(state)
        return 1 if self.to_move(state) == player else -1

    def print(self, state: State):
        _, number = state
        print(f'The number is {number} and ', end='')
        if self.is_terminal(state):
            if self.utility(state, 0) > 0:
                print(f'P1 won')
            else:
                print(f'P2 won')
        else:
            print(f'it is P{self.to_move(state)+1}\'s turn')

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

game = Game(5)

state = game.initial_state()
game.print(state)
while not game.is_terminal(state):
    player = game.to_move(state)
    action = minimax_search(game, state) # The player whose turn it is
                                         # is the MAX player
    print(f'P{player+1}\'s action: {action}')
    assert action is not None
    state = game.result(state, action)
    game.print(state)

# Expected output:
# The number is 5 and it is P1's turn
# P1's action: --
# The number is 4 and it is P2's turn
# P2's action: --
# The number is 3 and it is P1's turn
# P1's action: /2
# The number is 1 and it is P2's turn
# P2's action: --
# The number is 0 and P1 won