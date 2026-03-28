import time
import math
import random
from collections import deque

def get_move(state, player_id):
    bot = LearningBot1D(player_id)
    return bot.get_move(state)

class LearningBot1D:

    ROWS = 12
    COLS = 8
    SIZE = 96

    def __init__(self, player_id, time_limit=0.9):
        self.player_id = player_id
        self.enemy_id = 1 - player_id
        self.time_limit = time_limit
        self.start_time = 0

    def get_move(self, state):
        self.start_time = time.time()
        flat_board = self.flatten_state(state)
        best_move = self.iterative_deepening(flat_board)
        if best_move is None:
            best_move = self.get_random_valid_move(flat_board)
        return (best_move // self.COLS, best_move % self.COLS)

    def flatten_state(self, state):
        flat = [(-1, 0)] * self.SIZE
        for r in range(self.ROWS):
            base = r * self.COLS
            for c in range(self.COLS):
                owner, count = state[r][c]
                flat[base + c] = (
                    owner if owner is not None else -1,
                    count
                )
        return flat

    def iterative_deepening(self, board):
        best_move = None
        depth = 1
        while True:
            if self.time_exceeded():
                break
            move = self.minimax_root(board, depth)
            if move is not None:
                best_move = move
            depth += 1
        return best_move

    def minimax_root(self, board, depth):
        best_score = -math.inf
        best_moves = []
        moves = self.get_valid_moves(board, self.player_id)
        moves = self.order_moves(moves)
        for move in moves:
            if self.time_exceeded():
                break
            new_board = board[:]
            self.apply_move(new_board, move, self.player_id)
            score = self.minimax(
                new_board,
                depth - 1,
                -math.inf,
                math.inf,
                False
            )
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        if not best_moves:
            return None
        return random.choice(best_moves)

    def minimax(self, board, depth, alpha, beta, maximizing):
        if self.time_exceeded():
            return self.evaluate(board)
        winner = self.check_winner(board)
        if winner == self.player_id:
            return 100000
        if winner == self.enemy_id:
            return -100000
        if depth == 0:
            return self.evaluate(board)
        if maximizing:
            value = -math.inf
            moves = self.get_valid_moves(board, self.player_id)
            moves = self.order_moves(moves)
            for move in moves:
                new_board = board[:]
                self.apply_move(new_board, move, self.player_id)
                value = max(
                    value,
                    self.minimax(
                        new_board,
                        depth - 1,
                        alpha,
                        beta,
                        False
                    )
                )
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
                if self.time_exceeded():
                    break
            return value
        else:
            value = math.inf
            moves = self.get_valid_moves(board, self.enemy_id)
            moves = self.order_moves(moves)
            for move in moves:
                new_board = board[:]
                self.apply_move(new_board, move, self.enemy_id)
                value = min(
                    value,
                    self.minimax(
                        new_board,
                        depth - 1,
                        alpha,
                        beta,
                        True
                    )
                )
                beta = min(beta, value)
                if beta <= alpha:
                    break
                if self.time_exceeded():
                    break
            return value

    def order_moves(self, moves):
        return sorted(moves, key=self.move_priority, reverse=True)

    def move_priority(self, idx):
        cap = self.get_capacity(idx)
        if cap == 2:
            return 3
        if cap == 3:
            return 2
        return 1

    def apply_move(self, board, idx, player):
        owner, count = board[idx]
        board[idx] = (player, count + 1)
        self.resolve_explosions(board)

    def resolve_explosions(self, board):
        queue = deque()
        in_queue = set()
        for i in range(self.SIZE):
            if board[i][1] >= self.get_capacity(i):
                queue.append(i)
                in_queue.add(i)
        safety = 0
        while queue and safety < 500:
            safety += 1
            curr = queue.popleft()
            in_queue.discard(curr)
            owner, count = board[curr]
            cap = self.get_capacity(curr)
            if count < cap:
                continue
            leftover = count - cap
            board[curr] = (
                owner if leftover > 0 else -1,
                leftover
            )
            for nb in self.get_neighbors(curr):
                n_owner, n_count = board[nb]
                board[nb] = (
                    owner,
                    n_count + 1
                )
                if (
                    board[nb][1] >= self.get_capacity(nb)
                    and nb not in in_queue
                ):
                    queue.append(nb)
                    in_queue.add(nb)

    def get_capacity(self, idx):
        r = idx // self.COLS
        c = idx % self.COLS
        cap = 4
        if r == 0 or r == self.ROWS - 1:
            cap -= 1
        if c == 0 or c == self.COLS - 1:
            cap -= 1
        return cap

    def get_neighbors(self, idx):
        r = idx // self.COLS
        c = idx % self.COLS
        neighbors = []
        if r > 0:
            neighbors.append(idx - self.COLS)
        if r < self.ROWS - 1:
            neighbors.append(idx + self.COLS)
        if c > 0:
            neighbors.append(idx - 1)
        if c < self.COLS - 1:
            neighbors.append(idx + 1)
        return neighbors

    def get_valid_moves(self, board, player):
        moves = []
        for i in range(self.SIZE):
            owner, _ = board[i]
            if owner == -1 or owner == player:
                moves.append(i)
        return moves

    def get_random_valid_move(self, board):
        moves = self.get_valid_moves(
            board,
            self.player_id
        )
        if not moves:
            return 0
        return random.choice(moves)

    def check_winner(self, board):
        owners = set()
        total_orbs = 0
        for owner, count in board:
            if owner != -1:
                owners.add(owner)
                total_orbs += count
        if len(owners) == 1 and total_orbs > 1:
            return next(iter(owners))
        return None

    def evaluate(self, board):
        score = 0
        for idx in range(self.SIZE):
            owner, count = board[idx]
            if owner == -1:
                continue
            cap = self.get_capacity(idx)
            value = 10
            if count == cap - 1:
                value += 40
            if cap == 2:
                value += 25
            elif cap == 3:
                value += 10
            for nb in self.get_neighbors(idx):
                n_owner, n_count = board[nb]
                if (
                    owner == self.player_id
                    and n_owner == self.enemy_id
                    and n_count
                    == self.get_capacity(nb) - 1
                ):
                    value -= 30
            if owner == self.player_id:
                score += value
            else:
                score -= value
        return score

    def time_exceeded(self):
        return (
            time.time() - self.start_time
            > self.time_limit
        )
