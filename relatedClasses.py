import random

WIDTH = 9
HEIGHT = 9

class Square(object):
    '''
    Squre Class represent each square that consist the map.
    Three variaties of class are wall, treasure and snakepit, which have different moveable varaibles, reward value and end state
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.moveable = True
        self.reward = -1
        self.state = 'NULL'

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def get_state(self):
        return self.state

    def get_reward(self):
        return self.reward

    def set_wall(self):
        self.moveable = False

    def set_treasure(self):
        self.reward = 50
        self.state = 'TERMINAL'

    def set_snakepit(self):
        self.reward = -50
        self.state = 'TERMINAL'


def Map():
    '''
       map is a 2-dimension list which contained square class to build the given map.
       '''
    map = [[Square(i + 1, j + 1) for i in range(WIDTH)] for j in range(HEIGHT)]
    for y in range((WIDTH)):
        for x in range((HEIGHT)):
            if x + 1 == 9 and y + 1 == 9:
                map[x][y].set_treasure()
            elif x + 1 == 6 and y + 1 == 7:
                map[x][y].set_snakepit()
            elif y + 1 == 2 and x + 1 >= 3 and x + 1 <= 7:
                map[x][y].set_wall()
            elif y + 1 == 8 and x + 1 >= 2 and x + 1 <= 5:
                map[x][y].set_wall()
            elif x + 1 == 7 and y + 1 >= 3 and y + 1 <= 6:
                map[x][y].set_wall()
    return map


class Snake(object):
    '''
    Snake Class represent our agent which can move across the map.
    It has the ability to move towards 4 direction, but constrained to the game rule.
    '''
    def __init__(self, x, y, reward):
        self.x = x
        self.y = y
        self.reward = reward
        self.state = ''

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return (self.x, self.y)

    def reward_update(self, x, y, graph):
        if self.boundary_judgement(x,y):
            self.reward += graph[x][y].get_reward()
        else:
            self.reward-=1
        return self.reward

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def state_update(self, x, y, graph):
        self.state = graph[x][y].get_state()
        return self.state

    def boundary_judgement(self,x,y):
        if x < 0 or x > 8 or y < 0 or y > 8:
            return False
        else:
            return True

    def move_judgement(self, x, y,graph):
        self.boundary_judgement(x,y)
        if not graph[x][y].moveable:
            return False
        else:
            return True

    def move_left(self, graph):
        x, y = self.get_position()
        self.reward_update(x - 1, y, graph)
        if self.move_judgement(x - 1, y,graph):
            self.state_update(x - 1, y, graph)
            return self.set_position(x - 1, y)
        else:
            return self.get_position()

    def move_right(self, graph):
        x, y = self.get_position()
        self.reward_update(x + 1, y, graph)
        if self.move_judgement(x + 1, y,graph):
            self.state_update(x + 1, y, graph)
            return self.set_position(x + 1, y)
        else:
            return self.get_position()

    def move_down(self, graph):
        x, y = self.get_position()
        self.reward_update(x, y-1, graph)
        if self.move_judgement(x, y-1,graph):
            self.state_update(x, y-1, graph)
            return self.set_position(x, y-1)
        else:
            return self.get_position()

    def move_up(self, graph):
        x, y = self.get_position()
        self.reward_update(x, y+1, graph)
        if self.move_judgement(x, y+1,graph):
            self.state_update(x, y+1, graph)
            return self.set_position(x, y+1)
        else:
            return self.get_position()

####current policy: move towards 4 direnction with same possibality###
    def equiprobable_policy(self, graph):
        num = random.randint(1, 4)
        if num == 1:
            self.move_left(graph)
        elif num == 2:
            self.move_right(graph)
        elif num == 3:
            self.move_down(graph)
        else:
            self.move_up(graph)

def Episode():
    '''
    Episode represent a game from the given start position and map until the terminal situation
    '''
    graph = Map()
    move_path = []
    snake = Snake(0, 0, 100)
    while (snake.state != 'TERMINAL'):
        snake.equiprobable_policy(graph)
        move_path.append([snake.x,snake.y])
    return snake.reward,move_path


if __name__ == '__main__':
    reward,move_path=Episode()
    print(reward,move_path)

