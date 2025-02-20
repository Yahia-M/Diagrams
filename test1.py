from graphviz import Digraph

dot = Digraph(comment='Architecture Contrôle de Gestion')

# Ajouter des nœuds
dot.node('A', 'S3 (Data Lake)')
dot.node('B', 'Glue (ETL)')
dot.node('C', 'PySpark')

# Ajouter des arêtes
dot.edge('A', 'B')
dot.edge('B', 'C')

# Générer et afficher le diagramme
dot.render('architecture.gv', view=True)