import sys, os

import pandas as pd
from py2neo import Node, Graph

# Read from csv
df = pd.read_csv('skills.csv')

# // Setup connection
graph = Graph(bolt=True, bolt_port=7687, user='neo4j', password='neo')

# get transaction
tx = graph.begin()
print(graph)

# TODO: Create constraint.


# Create nodes
for index, row in df.iterrows():
    name = row['name']
    # if(row.isCombat):
    #     n = Node('Skill:Combat')
    # else:
    n = Node('Skill')

    # add name property
    n['name'] = name
    

    # Save nodes with transaction
    tx.merge(n, primary_label='Skill', primary_key='name')
tx.commit()
print(tx.finished())