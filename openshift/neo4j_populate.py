from sdifrontend.apps.mainpage.models import SysDataset
from sdifrontend.apps.mainpage.views.utils import unpack_dataset_json
from sdifrontend.apps.mainpage.models import SidebarMenu
from py2neo import Database
from py2neo import Graph
graph = Graph(host="neo4j", auth=('neo4j','1234'))

sb = SidebarMenu()


query = '''MATCH (n)
DETACH DELETE n;
'''
print(query)
graph.run(query)

query = '''CREATE INDEX ON :User(id);'''
print(query)
graph.run(query)
query = '''CREATE INDEX ON :Dataset(id);'''
print(query)
graph.run(query)
query = '''CREATE INDEX ON :Category(id);'''
print(query)
graph.run(query)
query = '''CREATE INDEX ON :Type(id);'''
print(query)
graph.run(query)
query = '''CREATE INDEX ON :Keyword(value);'''
print(query)
graph.run(query)

# Creating nodes

# Creating nodes
for ds in SysDataset.objects.all():
     ds = unpack_dataset_json(ds)
     query = "MERGE (n:User {{ id: '{0}', username: '{1}'}});"
     print(query.format(ds.owner.id, ds.owner.username))
     graph.run(query.format(ds.owner.id, ds.owner.username))
     query = "MERGE (n:Dataset {{ id: '{0}', title: '{1}'}});"
     print(query.format(ds.id, ds.attributes['title']))
     graph.run(query.format(ds.id, ds.attributes['title']))
     query = "MERGE (n:Category {{ id: '{0}', name: '{1}'}});"
     print(query.format(ds.category, sb.nav_elements[0]['items'][ds.category]['name']))   
     graph.run(query.format(ds.category, sb.nav_elements[0]['items'][ds.category]['name']))   
     query = "MERGE (n:Type {{ id: '{0}', name: '{1}'}});"
     print(query.format(ds.type, sb.nav_elements[1]['items'][ds.type]['name']))
     graph.run(query.format(ds.type, sb.nav_elements[1]['items'][ds.type]['name']))
     query = "MERGE (n:Keyword {{ value: '{0}'}});"
     for keyword in ds.attributes['keywords']:
          print(query.format(keyword))
          graph.run(query.format(keyword))
          

# Creating edges
for ds in SysDataset.objects.all():
     ds = unpack_dataset_json(ds)
     query = '''
     MATCH (a:User),(b:Dataset)
     WHERE a.id = '{0}' AND b.id = '{1}'
     CREATE (a)-[r:Owns]->(b);
     '''
     print(query.format(ds.owner.id, ds.id))
     graph.run(query.format(ds.owner.id, ds.id))

     query = '''
     MATCH (a:Dataset),(b:Category)
     WHERE a.id = '{0}' AND b.id = '{1}'
     CREATE (a)-[r:isInCategory]->(b);
     '''
     print(query.format(ds.id, ds.category))
     graph.run(query.format(ds.id, ds.category))

     query = '''
     MATCH (a:Dataset),(b:Type)
     WHERE a.id = '{0}' AND b.id = '{1}'
     CREATE (a)-[r:hasType]->(b);
     '''
     print(query.format(ds.id, ds.type))
     graph.run(query.format(ds.id, ds.type))

     for keyword in ds.attributes['keywords']:
          query = '''
     MATCH (a:Dataset),(b:Keyword)
     WHERE a.id = '{0}' AND b.value = '{1}'
     CREATE (a)-[r:hasKeyword]->(b);
          '''
          print(query.format(ds.id, keyword))
          graph.run(query.format(ds.id, keyword))


