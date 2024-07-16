import string
import random


outcomes = [
    "death",
    "wealth",
    "famine",
    "peace"
]

mtypes = [
    "war",
    "fight",
    "dialog"
]

motives = {
    

}


def generate_name():
    return "".join([random.choice(string.ascii_letters) for i in range(10)])

class Memory:

    def __init__(self, actor):
        # check nearby locations for things (actees, items, locations, factions, civils etc)
        # calculate/ get random encounter type
        # calculate/get random result
        # propigate to actee's (person, places or things)
        pass


class Civilization:

    def __init__(self, x, y, motive):
        self.location = (x, y)
        self.size = 10
        # self.motive = motive
        # self.characteristics = 
        self.encountered = []
        self.name = generate_name()
        self.memory = []

class Character:

    def __init__(self, civil):
        self.speed = 1
        self.name = generate_name()
        self.aligience = civil
        self.location = civil.location
        self.memory = []

    def __str__(self):
        return self.name
        
class generator:

    def __init__(self):
        self.x_range = 100
        self.y_range = 100
        self.civilizations = [Civilization(random.randrange(1,self.x_range), random.randrange(1,self.y_range)) for i in range(4)]
        self.main_char = Character(self.civilizations[0])
        self.chars = [Character(random.choice(self.civilizations)) for i in range(4)]
        self.total = ""


    def make_move(self, actor):
        actor_move = random.choice([True,False])
        if actor_move:
            move = random.randrange(0,actor.speed + 1)
            actor.location = (actor.location[0] + move  , actor.location[1] + move)
        make_memory = random.choice([True,False])
        if make_memory:
            mem = Memory(actor)
            
        # actor.memory.append(mem) # need to remove char after death
        # self.total += f"{actor} {mem.mtype} {actee} RESULTS: {actor} {mem.actor_outcome} and {actee} {mem.actee_outcome}\n"
        # return f"{actor} {mem.mtype} {actee} RESULTS: {actor} {mem.actor_outcome} and {actee} {mem.actee_outcome}"
        
    def run_sim(self):
        
        for i in range(10):
            self.make_move(self.main_char, random.choice(self.chars), random.choice(self.civilizations)) # need to keep track of char location, and them moving
            for char in self.chars:
                self.make_move(char, random.choice(self.chars), random.choice(self.civilizations)) # dont have actee be self??
        
        print(self.total)

gen = generator()
gen.run_sim()  
    
