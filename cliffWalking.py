import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
MAX_STEPS=100
WIDTH = 12
HEIGHT = 4
NEGATIVE=-100000
epsilon = 0.5
iteration = 2000
'''IMPORTANT'''
"""The x y setting is according to the 2-dimension list index, not the graph index"""
# 0      1      2    3
# LEFT   RIGHT  UP   DOWN
ACTIONS = [[0, -1], [0, 1], [-1, 0], [1, 0]]


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
        self.q_table = [0 for i in range(4)]

    def set_q_value(self, value, action):
        self.q_table[action] = value

    def get_q_value(self, action):
        return self.q_table[action]

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return (self.x, self.y)

    def get_state(self):
        return self.state

    def get_reward(self):
        return self.reward

    def set_cliff(self):
        self.state = 'TERMINAL'
        self.reward = -100

    def set_goal(self):
        self.reward = +20
        self.state = 'TERMINAL'


def set_cliff_map():
    '''
       map is a 2-dimension list which contained square class to build the given map.
       '''
    map = [[Square(j, i) for i in range(WIDTH)] for j in range(HEIGHT)]
    for y in range((WIDTH)):
        for x in range((HEIGHT)):
            if y + 1 == 12 and x + 1 == 4:
                map[x][y].set_goal()
            elif x + 1 == 4 and y > 0 and y < 11:
                map[x][y].set_cliff()
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
        if x < 0 or x > 3 or y < 0 or y > 11:
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
            print(1)
            self.set_position(x + action[0], y + action[1])
            return graph[x + action[0]][y + action[1]]
        else:
            print(2)
            return graph[x][y]

    def epsilon_greedy_policy(self, current_state, epsilon, use_epsilon):
        x, y = current_state.get_position()
        num = random.random()
        # 1.1exp[oitation
        if num > epsilon and use_epsilon:
            #greedy return the max q value action
            max_q_value = max(graph[x][y].q_table)
            for i in range(len(graph[x][y].q_table)):
                if graph[x][y].q_table[i] == max_q_value:
                    direction_tag = i
            print("greedy",current_state.get_position(), direction_tag)
        # 1.2exploration: epsilon-greedy
        else:
            j = random.randint(0, 3)
            for i in range(len(ACTIONS)):
                if i==j:
                    direction_tag = i  # the action of next move
            print("epsilon", direction_tag)
        return direction_tag

    def q_learning(self, graph, alpha=0.1, discount_factor=0.95):
        # 1 initial location
        x, y = 3, 0
        t = 0
        self.set_position(x, y)
        state0 = graph[x][y]
        while state0.state != "TERMINAL" and t < MAX_STEPS:
            # 2 calculate Action and S' according to the policy
            action0 = self.epsilon_greedy_policy(state0, epsilon, True)
            # 3 calculate Action' a according to the policy
            self.move(graph, ACTIONS[action0])
            x, y = self.get_position()
            state1 = graph[x][y]
            updated_q_value = state0.get_q_value(action0) + alpha * (
                    state1.get_reward() + (discount_factor * max(state1.q_table))-state0.get_q_value(action0))
            print(state0.get_q_value(action0), updated_q_value,max(state1.q_table))
            state0.set_q_value(updated_q_value,action0)
            state0 = state1
            t += 1
        print("@@@@@@@@END@@@@@@@@")

    def SARSA(self, graph, alpha=0.1, discount_factor=0.95):
        # 1 initial location
        #x,y=random.randint(0,3),random.randint(0,11)
        x,y=3,0
        t=0
        self.set_position(x,y)
        state0 = graph[x][y]
        # 2 calculate Action and S' according to the policy
        action0= self.epsilon_greedy_policy(state0, epsilon, True)
        # 3 calculate Action' a according to the policy
        while state0.state != "TERMINAL" and t<MAX_STEPS:
            self.move(graph, ACTIONS[action0])
            x,y=self.get_position()
            state1=graph[x][y]
            reward=state1.get_reward()
            action1 = self.epsilon_greedy_policy(state1, epsilon, True)
            # 4 update Q-value according to SARSA
            print("S",state0.get_position(),"A",action0,"R",reward,"S'",state1.get_position(),"A'",action1)

            updated_q_value = (state0.get_q_value(action0) + alpha * (
                     state1.get_reward() + (discount_factor*state1.q_table[action1]) - state0.q_table[action0]))
            print(state0.get_q_value(action0),updated_q_value)
            # 5 update q value
            state0.set_q_value(updated_q_value, action0)
            # 6 move according to the direction tag to next state
            state0 = state1
            action0 = action1
            t+=1
        print("@@@@@@@@END@@@@@@@@")


def Episode(graph, snake, times,onPolicy):
    '''
    Episode represent a game from the given start position and map until the terminal situation
    '''
    move_path = []
    for i in range(times):
        if onPolicy==True:
            snake.SARSA(graph)
        else:
            snake.q_learning(graph)
        move_path.append([snake.x, snake.y])
    # snake.value_update(graph)
    return snake.reward, move_path

if __name__ == '__main__':
    reward_table = []
    graph = set_cliff_map()
    for row in graph:
        for s in row:
            print(s.state, end="   ")
        print("\n")
    x, y = 3, 0
    snake = Snake(x, y, 0)
    # set episode, the last parameter determine whether use SARSA(True) or Q_learning(False)
    reward, move_path = Episode(graph, snake,iteration,False)
    # output Q table
    for i in range(HEIGHT):
        for j in range(WIDTH):
            print(graph[i][j].q_table, end=" ")
        print('\n')
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if i == 3 and j != 0 and j != 11:
                print("C", end=" ")
                continue
            elif i == 3 and j == 11:
                print("G", end=" ")
                continue
            max = -10000
            for x in range(len(graph[i][j].q_table)):
                if graph[i][j].q_table[x] != 0 and graph[i][j].q_table[x] > max:
                    index = x
                    max = graph[i][j].q_table[x]
            if index == 0:
                print("←", end=" ")
            elif index == 1:
                print("→", end=" ")
            elif index == 2:
                print("↑", end=" ")
            elif index == 3:
                print("↓", end=" ")
        print('\n')