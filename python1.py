from copy import deepcopy
from colorama import Fore, Back, Style

#Ma trận hướng đi
DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
#Ma trận đích 
END = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]

#bảng màu
bar = Style.BRIGHT + Fore.BLACK + '\u2502' + Fore.RESET + Style.RESET_ALL
dash='\u2500'
right_junction = '\u2524'
left_junction = '\u251C'

#hàm vẽ puzlle
def print_puzzle(array):
    for a in range(len(array)):
        for i in array[a]:
            if i == 0:
                print(bar, Back.WHITE + ' ' + Back.RESET, end=' ')
            else:
                print(bar, i, end=' ')
        print(bar)

#nó là nút lưu trữ từng trạng thái câu đố
class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h

#trả về vị trí 
def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))

#Tính khoảng cách giữa các nút
def Distance(current_state):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = get_pos(END, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost

#nhận các nút liền kề
def getAdjNode(node):
    listNode = []
    emptyPos = get_pos(node.current_node, 0)

    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
            newState = deepcopy(node.current_node)
            newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            # listNode += [Node(newState, node.current_node, node.g + 1, Distance(newState), dir)]
            listNode.append(Node(newState, node.current_node, node.g + 1, Distance(newState), dir))
    return listNode

#lấy nút tốt nhất trong các nút có sẵn
def getBestNode(openSet):
    firstIter = True

    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode

#Hàm này tạo ra đường đi ngắn nhất
def buildPath(closedSet):
    node = closedSet[str(END)]
    branch = list()

    while node.dir:
        branch.append({
            'dir': node.dir,
            'node': node.current_node
        })
        node = closedSet[str(node.previous_node)]
    branch.append({
        'dir': '',
        'node': node.current_node
    })
    branch.reverse()
    return branch

#hàm chính (thuật toán A*)
def main(puzzle):
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, Distance(puzzle), "")}
    closed_set = {}

    while True:
        test_node = getBestNode(open_set)
        closed_set[str(test_node.current_node)] = test_node

        if test_node.current_node == END:
            return buildPath(closed_set)

        adj_node = getAdjNode(test_node)
        for node in adj_node:
            if str(node.current_node) in closed_set.keys() or str(node.current_node) in open_set.keys() and open_set[str(node.current_node)].f() < node.f():
                continue
            open_set[str(node.current_node)] = node

        del open_set[str(test_node.current_node)]

#hàm main để chạy chương trình và không sử dụng khi gọi.
if __name__ == '__main__':
    #it is start matrix
    br = main([[1,2,3,4],[5,6,7,8],[9,0,10,12],[13,14,11,15]])

    print('total steps : ', len(br) - 1)
    print()
    print(dash + dash + right_junction, "INPUT", left_junction + dash + dash)
    for b in br:
        if b['dir'] != '':
            letter = ''
            if b['dir'] == 'U':
                letter = 'UP'
            elif b['dir'] == 'R':
                letter = "RIGHT"
            elif b['dir'] == 'L':
                letter = 'LEFT'
            elif b['dir'] == 'D':
                letter = 'DOWN'
            print(dash + dash + right_junction, letter, left_junction + dash + dash)
        print_puzzle(b['node'])
        print()

    print(dash + dash + right_junction, 'ABOVE IS THE OUTPUT', left_junction + dash + dash)