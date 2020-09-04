"""
Chad Fischer AI proj 3
"""
import numpy as np

def util(u_mat, r_mat, action, x, y):
    _util = 0
    size = len(u_mat)
    n,e,s,w = .1,.1,.1,.1
    if action == '^': w = .7
    elif action == '>': n = .7
    elif action == 'v': e = .7
    elif action == '<': s = .7

    if x in range(1, size - 1) and y in range(1, size - 1):
        _util = n * u_mat[x][y + 1] + e * u_mat[x + 1][y] + s * u_mat[x][y - 1] + w * u_mat[x - 1][y]
    elif y == 0 and x == 0:
        _util = n * u_mat[x][y + 1] + e * u_mat[x + 1][y] + s * u_mat[x][y] + w * u_mat[x][y]
    elif x == size - 1 and y in range(1,size-1):
        _util = n * u_mat[x][y + 1] + e * u_mat[x][y] + s * u_mat[x][y - 1] + w * u_mat[x-1][y]
    elif y == size - 1 and x in range(1,size-1):
        _util = n * u_mat[x][y] + e * u_mat[x + 1][y] + s * u_mat[x][y - 1] + w * u_mat[x-1][y]
    elif x == 0 and y in range(1, size - 1):
        _util = n * u_mat[x][y + 1] + e * u_mat[x + 1][y] + s * u_mat[x][y - 1] + w * u_mat[x][y]
    elif y == 0 and x in range(1, size - 1):
        _util = n * u_mat[x][y + 1] + e * u_mat[x + 1][y] + s * u_mat[x][y] + w * u_mat[x - 1][y]
    elif y == size - 1 and x == size - 1:
        _util = n * u_mat[x][y] + e * u_mat[x][y] + s * u_mat[x][y - 1] + w * u_mat[x - 1][y]
    elif x == 0 and y == size - 1:
        _util = n * u_mat[x][y] + e * u_mat[x + 1][y] + s * u_mat[x][y - 1] + w * u_mat[x][y]
    elif x == size - 1 and y == 0:
        _util = n * u_mat[x][y + 1] + e * u_mat[x][y] + s * u_mat[x][y] + w * u_mat[x - 1][y]

    reward = r_mat[x][y]
    return _util,reward

def value_it(u, r):
    u_mat = list(u)
    r_mat = list(r)
    policy = [[0 for x in range(len(u_mat))] for y in range(len(u_mat))]
    
    while True:
        delta = 0
        epsilon = 0.01
        action_list = ['^', '>', 'v', '<']
        # loop over state space
        for rownum, row in enumerate(u_mat):
            for colnum, col in enumerate(row):
                if(r_mat[rownum][colnum] == 99):continue
                action_vals = []
                reward_vals = []
                # loop over actions
                for a in range(0,4):
                    _u,_r = util(u_mat, r_mat, action_list[a], rownum, colnum)
                    action_vals.append(_u)
                    reward_vals.append(_r)
                optimized_action = max(action_vals)
                action_in = action_vals.index(optimized_action)
                reward = reward_vals[action_in]
                action_token = action_list[action_in]
                bellman = reward + .9 * optimized_action
                delta = max(delta, abs(bellman - u_mat[rownum][colnum]))
                u_mat[rownum][colnum] = bellman
                policy[rownum][colnum] = action_token
        if delta < epsilon:
            break
    return u_mat,policy


def read_in():
    file = open('input', 'r')
    size = int(file.readline())
    obstacle_num = int(file.readline())
    obs_list = []
    dest = []
    for i,line in enumerate(file):
        if i < obstacle_num: obs_list.append(line.strip().split(','))
        else: dest.append(line.strip().split(','))

    ew_mat = np.ones(shape=(size,size))
    # reward map with -1 values
    rew_mat = np.negative(ew_mat)
    util_mat = np.zeros(shape=(size, size))
    # add destination
    resx = int(dest[0][0])
    resy = int(dest[0][1])
    rew_mat[resy][resx] = 99
    util_mat[resy][resx] = 99
    for x in obs_list:
        rew_mat[int(x[1])][int(x[0])] = -100
    v,p = value_it(util_mat, rew_mat)
    p[resy][resx] = '.'
    for q in obs_list:
        p[int(q[1])][int(q[0])] = 'o'
    _f = open('output','w')
    for line in p:
        for element in line:
            _f.write(element)
        _f.write('\n')

read_in()

