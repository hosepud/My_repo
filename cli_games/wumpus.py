from random import randint

class Room(object):
    def __init__(self, num):
        self.neighbors = [None, None, None]
        self.id = num

def connect(r1, r2):
    for i in range(3):
        if r1.neighbors[i] is None:
            for j in range(3):
                if r2.neighbors[j] is None:
                    r1.neighbors[i] = r2
                    r2.neighbors[j] = r1
                    return
rooms = [Room(0)]
chars = []

def make_labyrinth(room):
    if all(room.neighbors):
        return
    if len(rooms) == 20:
        return
    else:        
        for i in room.neighbors:
            if i is None:
                r = Room(len(rooms))
                rooms.append(r)
                connect(room, r)
                if len(rooms) == 20:                    
                    return                
        for r in room.neighbors:            
            make_labyrinth(r)    

def finalize_labyrinth():
    leafs = []
    for i in rooms:
        nb = list(filter(lambda x: x, i.neighbors))
        if len(nb) == 1:
            leafs.append(i)
    ctr = 0
    while True:        
        connect(leafs[ctr], leafs[ctr+1])
        ctr += 1 
        if ctr == len(leafs)-1:
            connect(leafs[0], leafs[-1])
            break      
    return

def get_random_room():
    clear = False
    while not clear:
        clear = True
        r = randint(0, 19)
        for c in chars:
            if c.room == r:
                clear = False        
    return r    

def init_chars():
    char_names = ["Player", "Bat", "Bat", "Wumpus", "Pit", "Pit"]    
    for n in char_names:
        chars.append(Character(get_random_room(), n))
    return 

class Character(object):
     def __init__(self, r, identity):
        self.room = r
        self.name = identity

     def move(self, index):
        self.room = rooms[self.room].neighbors[index-1].id

        return
    
def next_round(index, batted = False):          
    p = chars[0]
    if not batted: 
        p.move(index)
    for c in chars[1:]:
        if p.room == c.room:
            if c.name in ["Wumpus", "Pit"]:
                return False
            elif c.name == "Bat":
                tmp = randint(0, 19)
                print("Bat encountered, new room is %d " % tmp)
                p.room = tmp
                return next_round(-1, True)
    return 1

def print_20_graph():
    def have_edge(r1, r2):
        for i in r1.neighbors:
            if i == r2:
                return True
        return False
    graph = []
    for i in range(20):
        graph.append([0]*20)
    for i in range(20):
        r1 = rooms[i]
        for j in range(20):
            r2 = rooms[j]
            if have_edge(r1, r2):
                graph[i][j] = 1 
    print("  ", end = " ")
    for i in range(20):
        print("%2d"%i, end = " ")
    print('\n', end = " ")
    for i in range(20):
        print("%2d"%i, end = " ") 
        print(graph[i])

def print_info():
    p = chars[0]
    ctr = 0
    nb = []
    for r in rooms[p.room].neighbors:
        ctr +=1
        print("(Door %d to Room %d)" %(ctr, r.id))
        nb.append(r.id)
    
    for char in chars[1:]:
        if char.room in nb:
            if char.name == "Wumpus":
                print("I smell a wumpus")
            if char.name == "Bat":
                print("Bats nearby")
            if char.name == "Pit":
                print("I feel a draft")
    print('\n')

def get_input():
    m = -2
    tmp = ""
    while m not in [-1,1,2,3]:
        tmp = input(">")
        try:
            m = int(tmp)
        except:
            if(tmp.strip().lower() in "shootshotshoootshoots"):
                m = -1
    return m

def shoot():
    m = -1
    while m == -1:
        print("Room to shoot in")
        m = get_input()
    w = chars[3]
    p = chars[0]
    if w.room == rooms[p.room].neighbors[m-1].id:
        return 1
    else:
        if randint(0,2) == 0:
            print("Wumpus gets startled and moves..")
            n = randint(0, 19)
            if n == p.room:
                return 0
            else:
                w.room = n
                print(w.room)
                return 2
        return 2

def main():
    make_labyrinth(rooms[0])
    finalize_labyrinth()
    init_chars() 
    p = chars[0]
    print("In room %d " %p.room)
    #for i in chars:
    #    print i.name, " IN ", i.room
    while True:
        print_info()         
        m = get_input()
        if m == -1:
            outcome = shoot()
            if outcome == 2:               
                continue
            elif outcome == 1:
                print("You killed the wumpus")
                break
            else:
                print("You died")
                break
        outcome = next_round(m)
        if outcome:
            print("In room %d " %p.room)
        else:
            print("You died.")
            break
    return
            
main()


