from classes import Verb, Story, Noun, Adjective

narrator = Noun("Brandon Brodrick", False, "none", None, "male")
bobalina = Noun("Bobalina", False, "none", None, "female")
subject = Noun("cat", True, "specific", bobalina, "none")
jump = Verb("jump")
adj = Adjective("high")
sty = Story(narrator, [narrator, subject, bobalina])
print(sty.generate_indepentant_clause(narrator, jump, "present", adj))
print(sty.generate_indepentant_clause(bobalina, jump, "future", adj))
print(sty.generate_indepentant_clause(subject, jump, "past", adj))
# print(sty.show_story())

