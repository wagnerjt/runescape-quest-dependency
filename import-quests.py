
import json

from py2neo import Node, Relationship, Graph, NodeMatcher

def match_quest(quest_id, matcher):
    return matcher.match('Quest', questId=quest_id).first()
def match_skill(skill_name, matcher):
    return matcher.match('Skill', name=skill_name).first()

class DEPENDS_ON(Relationship): pass

# Load json from file
quest_path = 'quests.json'

with open(quest_path, 'r') as fp:
    raw_quest_json = json.load(fp)

# Configuring our graph
graph = Graph(bolt=True, bolt_port=7687, user='neo4j', password='neo')
graph_matcher = NodeMatcher(graph)

# Ensuring we have all quests added
tx = graph.begin()
for row in raw_quest_json:
    quest_node = Node('Quest', questId=row['id'], name=row['title'], members=row['members'])
    tx.merge(quest_node, primary_label='Quest', primary_key='questId')
tx.commit()
if tx.finished():
    print('All Quest Nodes have been merged successfully')
else:
    print('There was an issue merging quest nodes.')

tx = graph.begin()
# Start building relationships for dependencies
for row in raw_quest_json:
    if 'requirements' in row:
        quest = match_quest(row['id'], graph_matcher)
        if quest is None:
            print('quest is none', requirement)
            continue
        for requirement in row['requirements']:

            # Handle quest array
            if requirement is 'quests':
                pass
            elif requirement is 'qp':
                pass # Handle qp
            else:
                skill = match_skill(requirement, graph_matcher) # Handle Skill
                if skill is not None:
                    # Create the required relationship between quest and skill
                    q_depends_s = DEPENDS_ON(quest, skill, level=row['requirements'][requirement])
                    tx.merge(q_depends_s)
                    print(q_depends_s)
tx.commit()


# Setup connection

# get transaction
# tx = graph.begin()
# print(graph)

# # TODO: Create constraint.


# # Create nodes
# for index, row in df.iterrows():
#     name = row['name']
#     # if(row.isCombat):
#     #     n = Node('Skill:Combat')
#     # else:
#     n = Node('Skill')

#     # add name property
#     n['name'] = name
    

#     # Save nodes with transaction
#     tx.merge(n, primary_label='Skill', primary_key='name')
# tx.commit()
# print(tx.finished())