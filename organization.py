import math
import string
import random
from typing import Optional, Type, Any, Literal
from dataclasses import dataclass, asdict

def generate_name():
    return "".join([random.choice(string.ascii_letters) for i in range(10)])

@dataclass
class ResourceBill:
    """ A class for showing a resource bill for a task force"""
    community: Optional[int]
    infrastructure: Optional[int]
    materials: Optional[int]
    force: Optional[int]
    agriculture: Optional[int]
    industry: Optional[int]
    
@dataclass
class OrganizationRelation:
    """A class for showing an opinion of ONE organization to an entity"""
    relation: Optional[int] = 50 # 0 == hates, 100 == loves
    organization: Optional[Any] = None

class Character:

    def __init__(self):
        self.name = f"CHAR-{generate_name()}"
        self.risk = random.randrange(0,101)
        self.determination = random.randrange(0,101)
        self.aggression = random.randrange(0,101)
        self.health = 100
        self.hunger = 100
        self.agenda = None # a mission statement not created with one
        
    def calculate_destroyed(self):
        print(self.name," calculate_destroyed ", sorted([self.health, self.hunger])[0])
        "Return 0 (destroyed) - 100 (perfect) based off lowest trait health/hunger"
        return sorted([self.health, self.hunger])[0]

    def reflect(self, organization: Any = None):
        "Here is where a character will reflect on a their status and make/keep an agenda"
        # if org and a resource is low, make a missionStatment to increase that resource
        # if org, check relations. maybe make a missionStatment based off aggression/risk and org relations
        # compare your current agenda to the ones made above, pick one
        pass
    
    def make_desision(self, options, organization: Any = None):
        "Here is where a character will be given a choice and have to pick a winner based off traits and exterior things they own."
        if not options:
            return None
        selected_option = options[0]
        for option in options:
            if isinstance(option, PassiveTaskForce):
                # weigh the options, see if it aligns with the leaders opinions and needs of their organization
                pass
            elif isinstance(option, TaskForce):
                # weigh the options, see if it aligns with the leaders opinions and needs of their organization
                pass
        print(self.name, " make_desision ", selected_option)
        return selected_option
    
        
class Organization:

    resource_start_multiplier = 10
    
    def __init__(self, size=1):
        self.owner = self
        self.name = f"ORG-{generate_name()}"
        self.population = self.resource_start_multiplier * size
        self.community = self.resource_start_multiplier * size
        self.infrastructure = self.resource_start_multiplier * size # doesnt seem necessary
        self.materials = self.resource_start_multiplier * size
        self.force = self.resource_start_multiplier * size
        self.agriculture = self.resource_start_multiplier * size
        self.industry = self.resource_start_multiplier * size
        self.leader = Character()
        self.passive_task_forces = []
        self.task_forces = []
        self.relations = []
        
    def calculate_destroyed(self):
        "return 0 (destroyed) - x (doing well) based off lowest trait?"
        print(self.name, " calculate_destroyed ", sorted([self.community, self.agriculture, self.agriculture])[0])
        return sorted([self.community, self.agriculture, self.agriculture])[0]


    def pick_possible_task_forces(self):
        available_resources = ("community", "infrastructure", "materials", "force", "agriculture", "industry")
        if self.passive_task_forces:
            used_resources = set([ptf.resource_type for ptf in self.passive_task_forces])
            available_resources = list(set(["community", "infrastructure", "materials", "force", "agriculture", "industry"]) - used_resources)
        passives = [PassiveTaskForce(random.choice(available_resources), self, random.randrange(1,self.resource_start_multiplier)) for i in available_resources]
        #TODO: org needs to know all entities, then we can make 2 random TaskForces related to them
        print(self.name, " pick_possible_task_forces ", passives)
        return passives
    
    def make_task_force(self):
        "use leader/leader attr + organization resources to determine if a task force/passive task force wants to be made."
        print("make_task_forces")
        possible_task_forces = self.pick_possible_task_forces()
        new_task_force = self.leader.make_desision(possible_task_forces)
        if new_task_force:
            if isinstance(new_task_force, PassiveTaskForce):
                self.passive_task_forces.append(new_task_force)
            self.task_forces.append(new_task_force)
            

    def degrade_resources(self):
        print(self.name, " degrade_resources ")
        "Degrade all resources based off population existing"
        self.community = self.community - round(self.leader.aggression / 100)
        self.infrastructure = self.infrastructure - (self.population / 100)
        self.agriculture = self.agriculture - (self.population / 100)
        self.population = self.population + (((self.population + self.community)* 2) / 100) 
        self.materials = self.materials - (self.industry / 100)
        

    def move(self):
        print(self.name, " move")
        "A simulated year for an Org."
        [ptf.move() for ptf in self.passive_task_forces]
        [tf.move() for tf in self.task_forces]
        self.make_task_force() # maybe make a task force
        self.degrade_resources() # degrade resources
        self.leader.reflect()
        alive = self.calculate_destroyed()
        if not alive:
            print("Oh no ", self.name, " was destroyed!")
            del self

class MissionStatement:
    
    def __init__(self, actee: Any, mission_type: Literal["Steal industry", "Steal agriculture", "Steal material", "Force", "Destroy"], acquisition_req: int = 30):
        self.actee = actee # thing its happening to
        self.acquisition = 0 # a sum of materials that gained, stolen
        self.mission_type = mission_type
        self.acquisition_req = acquisition_req

    def calc_progression(self):
        print("mission statement calc_progression")
        if self.actee:
            if isinstance(self.actee, Organization):
                if "Steal" in self.mission_type:
                    return (self.acquisition/self.acquisition_req) * 100
                elif self.mission_type == "Force":
                    return 100 if self.actee.owner == self else 0
                elif self.mission_type == "Destroy":
                    return abs(self.actee.calculate_destroyed() - 100)
            if isinstance(self.actee, Character):
                if self.mission_type == "Destroy":
                    return abs(self.actee.calculate_destroyed() - 100)
        return 0


class TaskForce:
    
    def __init__(self,
                 previous_leader: Optional[Type[Character]] = None,
                 determination: int = 50,
                 organization: Any = None,
                 aggression: int = 50,
                 mission_statement: Optional[Type[MissionStatement]] = None):
        self.leader = previous_leader or Character()
        self.resource_bill = self.generate_resource_bill()
        self.failure_bill = self.generate_resource_bill()
        self.organization = organization
        self.mission_statement = mission_statement
        self.determination = determination # how desperate they want this taskForce to finish (priority)
        self.aggression = aggression # How likely they are to use force (results in loss of community and higher loss of resources for higher progression)
        self.progress = 0
        self.resource_map = {
            "community": self.organization.community,
            "infrastructure": self.organization.infrastructure,
            "materials": self.organization.materials,
            "force": self.organization.force,
            "agriculture": self.organization.agriculture,
            "industry": self.organization.industry
        }

    def generate_resource_bill(self):
        "Create a resource bill for the task force depending on type."
        print("task force generate_resource_bill")
        return ResourceBill(None,10,10,10,10,10)
        
    def has_no_resources(self):
        "return Bool if the TF is out of a resource."
        print("task force has_no_resources")
        for res in asdict(self.resource_bill).values():
            if type(res) == int and not res:
                return True
        return False
        
        
    def move(self):
        print("task force move")
        leader_destroyed = self.leader.calculate_destroyed() # calculate leader health, if dead elect a new one or organization can obsorb back resources
        if leader_destroyed: 
           self.dissolve() # TODO: the organization MAY be able to ellect a new leader?
        mission_progress = self.mission_statement.calc_progression()
        if mission_progress == 100: # Check_progress in mission statement, if done call it off
            return # give the reward back
        if self.has_no_resources(): # Check if more resources, if not disolve
            self.dissolve()
        # calculate next task to complete taskForce (using char attrs and taskforce attrs)
        # do task, costing resources
        # impliment task side effects, update missionstatment progression
        pass

    def dissolve(self):
        "The org will eat up left over resources, paying the price for the Task Force"
        print("task force dissolve")
        for res_key, res_val in asdict(self.resource_bill).items():
            self.resource_map[res_key] += res_val
        self.organization.leader.make_desision([TaskForce(None, 50, self.organization, 50, MissionStatement(self.leader, "Destroy"))]) # TODO: allow PTF to have a "fire" function, basically a freebe
        self.organization.task_forces.remove(self)
        # TODO: calculate loss and subject organization to it
    
        
        
class PassiveTaskForce:
    
    def __init__(self, resource_type: Literal["community", "infrastructure", "materials", "force", "agriculture", "industry"], organization, resource_amount = 1):
        self.organization = organization
        self.resource_type = resource_type
        self.resource_amount = resource_amount
        self.resource_cost_map = {
            "community": [self.organization.agriculture],
            "infrastructure": [self.organization.materials, self.organization.agriculture],
            "materials": [self.organization.community],
            "force": [self.organization.community, self.organization.materials, self.organization.agriculture],
            "agriculture": [self.organization.materials],
            "industry": [self.organization.materials, self.organization.agriculture]
        }
        self.resource_map = {
            "community": self.organization.community,
            "infrastructure": self.organization.infrastructure,
            "materials": self.organization.materials,
            "force": self.organization.force,
            "agriculture": self.organization.agriculture,
            "industry": self.organization.industry
        }
        

    def move(self):
        print("PassiveTaskForce move")
        for resource in self.resource_cost_map[self.resource_type]:
            resource = resource - random.randrange(0,math.ceil(self.resource_amount/len(self.resource_cost_map[self.resource_type])))
        self.resource_map[self.resource_type] += random.randrange(0,self.resource_amount)
        
    def dissolve(self):
        " Organization abandons for reward in inital payment"
        print("PassiveTaskForce dissolve")
        for resource in self.resource_cost_map[self.resource_type]:
            resource = resource + random.randrange(0,math.ceil(self.resource_amount/len(self.resource_cost_map[self.resource_type])))
        self.organization.passive_task_forces.remove(self)
        
        
org = Organization(1)
org2 = Organization(1)
for i in range(10):
    print("YEAR ",i)
    org.move()
    org2.move()
