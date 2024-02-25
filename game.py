import random
from timer_decorator import measure_time
# TODO: Add comments
class Game:

    def __init__(self, size) -> None:
        self.size = size
        self.game_field = [[0] * self.size for _ in range(self.size)]

    def clear_field(self):
        self.game_field = [[0] * self.size for _ in range(self.size)]

    def init_random_field(self):
        self.clear_field()
        
        for row in range(self.size):
            for col in range(self.size):
                self.game_field[row][col] = random.randint(0,1)

    def _check_rules(self, neighbor_count, current_state):
        # TODO: Maybe change to match ?
        if current_state == 0 and neighbor_count == 3:
            return 1
        elif current_state == 1 and neighbor_count < 2:
            return 0
        elif current_state == 1 and neighbor_count > 3:
            return 0
        elif current_state == 1 and neighbor_count == 2 or neighbor_count == 3:
            return 1
        else: 
            return 0

    def _get_alive_neighbors(self, x, y):
        sum_alive = 0

        for i in [(self.size - 1), 0, 1]:
            for j in [(self.size - 1), 0, 1]:

                if i == 0 and j == 0:
                    continue

                sum_alive += self.game_field[(y + i) % self.size][(x + j) % self.size]

        return sum_alive

    def step(self):
        next_field = [[0] * self.size for _ in range(self.size)]

        for row in range(len(self.game_field)):
            for column in range(len(self.game_field[row])):
                neighbor_count = self._get_alive_neighbors(x=column, y=row)
                current_state = self.game_field[row][column]

                next_field[row][column] = self._check_rules(neighbor_count, current_state)

        self.game_field = next_field

if __name__ == "__main__":
    game = init_random_field(5)
    n = game._get_alive_neighbors(4, 4)
    print(n)
