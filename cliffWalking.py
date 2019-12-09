import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
WIDTH = 9
HEIGHT = 9
'''IMPORTANT'''
"""The x y of this problem is according to the 2-dimension list index, not the graph index"""
#0      1      2    3
#LEFT   RIGHT  UP   DOWN
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
        self.q_table=[0 for i in range(4)]

    def set_q_value(self,value,direction):
        self.q_table[direction]=value

    def get_q_value(self):
        return self.q_table

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
    map = [[Square(j, i) for i in range(WIDTH)] for j in range(HEIGHT)]
    for y in range((WIDTH)):
        for x in range((HEIGHT)):
            if x + 1 == 9 and y + 1 == 9:
                map[x][y].set_treasure()
            elif x + 1 == 7 and y + 1 == 6:
                map[x][y].set_snakepit()
            elif x + 1 == 2 and y + 1 >= 3 and y + 1 <= 7:
                map[x][y].set_wall()
            elif x + 1 == 8 and y + 1 >= 2 and y + 1 <= 5:
                map[x][y].set_wall()
            elif y + 1 == 7 and x + 1 >= 3 and x + 1 <= 6:
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
        current_reward=graph[x][y].get_reward()
        for square in nearbySquares:
            updated_value+=1.0/l*(current_reward+square.get_value())
        #print(updated_value)

        graph[x][y].set_value(updated_value)

    def equiprobable_policy(self, graph):
        '''equiproble policy with the same possability'''
        num = random.randint(0, 3)
        self.move(graph,ACTIONS[num])

    def optimal_value_function(self,graph):
        x, y = self.get_position()
        # print(x,y)
        # print("#######")
        next_states=self.nextStates(graph)
        max_value=-1000000
        for s in next_states:
            a,b=s.get_position()
            # print(a,b)
            value=s.get_value()
            if value>max_value:
                max_value=value
                max_pos=[s.x,s.y]
        action=[max_pos[0]-x,max_pos[1]-y]
        return action

    def dp_policy(self,graph):
        '''optimal policy with the highest value'''
        action=self.optimal_value_function(graph)
        self.move(graph,action)

    def q_learning(self,graph):
        #1 current position
        x, y = self.get_position()
        #print(x,y)
        #2 random pick next position
        next_states = self.nextStates(graph)
        num=len(next_states)-1
        n=random.randint(0,num)
        #3 calculate the movement between current and next state, get the direction tag
        x_next,y_next=next_states[n].get_position()
        x_diff,y_diff=x_next-x,y_next-y
        #print(x_diff,y_diff)
        for i in range(len(ACTIONS)):
            if [x_diff,y_diff]==ACTIONS[i]:
                direction_tag=i # the action of next move
        #print(direnction_tag,graph[x][y].q_table)
        #4 calculate q value according to the value
        updated_q_value=graph[x_next][y_next].get_reward()+max(graph[x_next][y_next].q_table)
        #5 update q value
        graph[x][y].set_q_value(updated_q_value,direction_tag)
        #6 move according to the direction tag to next state
        self.move(graph,ACTIONS[direction_tag])
        #print(graph[x][y].get_q_value())

    def q_learning_policy(self,graph):
        '''q_learning choosing the action with the highest value in with the q table of each square'''
        x, y = self.get_position()
        #print(x,y)
        max_q_value=max(graph[x][y].q_table)
        for i in range(len(graph[x][y].q_table)):
            if graph[x][y].q_table[i]==max_q_value:
                direction_tag=i
        self.move(graph, ACTIONS[direction_tag])





        

def Episode(graph,snake):
    '''
    Episode represent a game from the given start position and map until the terminal situation
    '''
    move_path = []
    while (snake.state != 'TERMINAL'):
        #snake.dp_policy(graph)
        snake.equiprobable_policy(graph)
        snake.value_update(graph)
        #snake.q_learning(graph)
        move_path.append([snake.x, snake.y])
    snake.value_update(graph)

    valueMatrix=[[0]*WIDTH for i in range(HEIGHT)]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # print(x,y)
            valueMatrix[x][y]=graph[x][y].get_value()

    global policy_evaluation
    policy_evaluation=valueMatrix
    return snake.reward, move_path,policy_evaluation

def Episode_q_learning(graph,snake):
    move_path = []
    while (snake.state != 'TERMINAL'):
        snake.q_learning_policy(graph)
        move_path.append([snake.x, snake.y])
    return snake.reward, move_path

def output_auxilary(policy_evaluation):
    for line in policy_evaluation:
        for i in range(len(line)):
            print('{0:>6.1f}'.format(line[i]),end = " ")
        print("")


if __name__ == '__main__':
    reward_table=[]
    graph = Map()
    # for i in range(9):
    """Iteration of 100 times can be adjust"""
    for i in range(100):
        #random start location
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        snake = Snake(x, y, 0)
        #Drop on the wall, skip this round
        if graph[x][y].moveable==False:
            continue
        reward,move_path,matrix=Episode(graph,snake)
        print(reward,move_path)
        #reward_table.append(reward)
    for i in range(9):
        for j in range(9):
            print(graph[i][j].q_table,end=" ")
        print('\n')
    output_auxilary(matrix)
    sns.set()
    np.random.seed(0)
    uniform_data = matrix
    ax = sns.heatmap(matrix)
    plt.show()

    # for i in range(100):
    #     x = random.randint(0, 8)
    #     y = random.randint(0, 8)
    #     if graph[x][y].moveable==False:
    #         continue
    #     snake = Snake(x, y, 0)
    #     reward, move_path = Episode_q_learning(graph, snake)
    #     reward_table.append(reward)
    #     #print(reward, move_path)

    #print(reward_table)