State = tuple[int, list[str | int]]  # Tuple of player (whose turn it is),
                                     # and the buckets (as str)
                                     # or the number in a bucket
Action = str | int  # Bucket choice (as str) or choice of number


class Game:
    def initial_state(self) -> State:
        return 0, ['A', 'B', 'C']

    def to_move(self, state: State) -> int:
        player, _ = state
        return player

    def actions(self, state: State) -> list[Action]:
        _, actions = state
        return actions

    def result(self, state: State, action: Action) -> State:
        if action == 'A':
            return (self.to_move(state) + 1) % 2, [-50, 50]
        elif action == 'B':
            return (self.to_move(state) + 1) % 2, [3, 1]
        elif action == 'C':
            return (self.to_move(state) + 1) % 2, [-5, 15]
        assert type(action) is int
        return (self.to_move(state) + 1) % 2, [action]

    def is_terminal(self, state: State) -> bool:
        _, actions = state
        return len(actions) == 1

    def utility(self, state: State, player: int) -> float:
        assert self.is_terminal(state)
        _, actions = state
        assert type(actions[0]) is int
        return actions[0] if player == self.to_move(state) else -actions[0]

    def print(self, state):
        print(f'The state is {state} and ', end='')
        if self.is_terminal(state):
            print(f'P1\'s utility is {self.utility(state, 0)}')
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

game = Game()

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