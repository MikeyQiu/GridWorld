import random

WIDTH = 9
HEIGHT = 9
ACTIONS = [[-1, 0], [1, 0], [0, 1], [0, -1]]#left right up down


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
        self.value = 0

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

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
        if self.boundary_judgement(x, y):
            self.reward += graph[x][y].get_reward()
        else:
            self.reward -= 1
        return self.reward

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def state_update(self, x, y, graph):
        self.state = graph[x][y].get_state()
        return self.state

    def boundary_judgement(self, x, y):
        '''judge boundary according to the rule '''
        if x < 0 or x > 8 or y < 0 or y > 8:
            return False
        else:
            return True

    def move_judgement(self, x, y, graph):
        '''judge whether the move fits the game rules'''
        if self.boundary_judgement(x, y):
            if not graph[x][y].moveable:
                return False
            else:
                return True
        else:
            return False

    def move(self, graph, action):
        '''agent move according to certain action'''
        x, y = self.get_position()
        self.reward_update(x + action[0], y + action[1], graph)
        if self.move_judgement(x + action[0], y + action[1], graph):
            self.state_update(x + action[0], y + action[1], graph)
            return self.set_position(x + action[0], y + action[1])
        else:
            return self.get_position()

    def nextStates(self,graph):
        '''judge the next possible states from the nearby squares'''
        nextStates=[]
        x, y = self.get_position()
        for action in ACTIONS:
            if self.move_judgement(x+action[0],y+action[1],graph):
                nextStates.append(graph[x+action[0]][y+action[1]])
        return nextStates

    def value_update(self,graph):
        updated_value=0.0
        x, y = self.get_position()
        '''update current square value through the nearby value'''
        nearbySquares=self.nextStates(graph)
        l=len(nearbySquares)
        current_value=graph[x][y].get_reward()
        for square in nearbySquares:
            updated_value+=1.0/l*(current_value+square.get_reward())
        graph[x][y].set_value(updated_value)

    ####current policy: move towards 4 direnction with same possibality###
    def equiprobable_policy(self, graph):
        num = random.randint(0, 3)
        self.move(graph,ACTIONS[num])

def Episode():
    '''
    Episode represent a game from the given start position and map until the terminal situation
    '''
    graph = Map()
    move_path = []
    snake = Snake(7, 8, 0)
    while (snake.state != 'TERMINAL'):
        snake.equiprobable_policy(graph)
        snake.value_update(graph)
        move_path.append([snake.x, snake.y])
    snake.value_update(graph)

    valueMatrix=[[0]*WIDTH for i in range(HEIGHT)]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            valueMatrix[x][y]=graph[x][y].get_value()

    global policy_evaluation
    policy_evaluation=valueMatrix
    return snake.reward, move_path,policy_evaluation

def output_auxilary(policy_evaluation):
    for line in policy_evaluation:
        for i in range(len(line)):
            print('{0:>6.2f}'.format(line[i]),end = " ")
        print("")


if __name__ == '__main__':
    # graph = Map()
    # snake=Snake(0,0,0)
    # for i in range(10):
    #     snake.equiprobable_policy(graph)
    #     print(snake.x,snake.y,snake.value_update(graph))
    reward,move_path,matrix=Episode()
    print(reward,move_path)
    output_auxilary(matrix)
