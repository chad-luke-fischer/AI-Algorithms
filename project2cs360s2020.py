import copy

class chef:
    def __init__(self, id, capacity, happy_a,happy_b, pick_state):
        self.id = id
        self.capacity = capacity
        self.happy_a = happy_a
        self.happy_b = happy_b
        self.pick_state = pick_state

def read_in():
    file = open('input', 'r')
    num_chefs = file.readline()
    alg = file.readline()
    choose_wab = False
    team_a = []
    team_b = []
    available = []
    for line in file:
        params = line.strip().split(',')
        if params[4] == '0': available.append(chef(int(params[0]),float(params[1]),float(params[2]),float(params[3]),params[4]))
        elif params[4] == '1': team_a.append(chef(int(params[0]),float(params[1]),float(params[2]),float(params[3]),params[4]))
        elif params[4] == '2': team_b.append(chef(int(params[0]),float(params[1]),float(params[2]),float(params[3]),params[4]))
    available.sort(key=lambda x: x.id, reverse=False)
    if alg == 'ab': choose_wab = True
    ans = decide_minmax(available, team_a, team_b, choose_wab)
    output = open('output', 'w')
    output.write(str(ans))
    output.close()
    return

def find_power(team,num):
    diversity = 120
    diversity_list = []
    net = 0
    for member in team:
        if num == 1: net += member.happy_a * member.capacity
        elif num == 2: net += member.happy_b * member.capacity
        if member.id % 10 in diversity_list: diversity = 0
        diversity_list.append(member.id % 10)
    net += diversity
    return net

def find_advantage(team_a,team_b):
    return find_power(team_a,1) - find_power(team_b,2)

def decide_minmax(available, teama, teamb, ab):
    val = [(float('-inf')), '']
    for member in available:
        tempavail = list(available)
        tempa = list(teama)
        tempa.append(member)
        tempavail.remove(member)
        if ab:
            if val[0] < minval_wab(tempavail,tempa,teamb,float('-inf'),float('inf')): val = [minval_wab(tempavail,tempa,teamb,float('-inf'),float('inf')),member.id]
        else:
            if val[0] < minval(tempavail, tempa, teamb): val = [minval(tempavail, tempa, teamb), member.id]
        if val[0] < minval(tempavail,tempa,teamb): val = [minval(tempavail,tempa,teamb),member.id]
    return val[1]

def maxval(available, teama, teamb):
    if(len(teama) == 5 and len(teamb)== 5): return find_advantage(teama,teamb)
    else:
        val = float('-inf')
        for member in available:
            tempavail = list(available)
            tempa = list(teama)
            tempa.append(member)
            tempavail.remove(member)
            val = max(val, minval(tempavail,tempa,teamb))
        return val

def maxval_wab(available, teama, teamb, alpha, beta):
    if(len(teama) == 5 and len(teamb)== 5): return find_advantage(teama,teamb)
    else:
        val = float('-inf')
        for member in available:
            tempavail = list(available)
            tempa = list(teama)
            tempa.append(member)
            tempavail.remove(member)
            val = max(val, minval(tempavail,tempa,teamb))
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return val

def minval(available, teama, teamb):
    if (len(teama) == 5 and len(teamb) == 5): return find_advantage(teama,teamb)
    else:
        val = float('inf')
        for member in available:
            tempavail = list(available)
            tempb = list(teamb)
            tempb.append(member)
            tempavail.remove(member)
            val = min(val, maxval(tempavail,teama,tempb))
        return val

def minval_wab(available, teama, teamb, alpha, beta):
    if (len(teama) == 5 and len(teamb) == 5): return find_advantage(teama,teamb)
    else:
        val = float('inf')
        for member in available:
            tempavail = list(available)
            tempb = list(teamb)
            tempb.append(member)
            tempavail.remove(member)
            val = min(val, maxval(tempavail,teama,tempb))
            beta = min(beta,val)
            if beta <= alpha:
                break
        return val

team_list = read_in()