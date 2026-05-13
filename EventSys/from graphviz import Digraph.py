import os
os.environ["PATH"] += os.pathsep + r"C:\Users\raine\miniconda3\Library\bin"
os.environ["GRAPHVIZ_PLUGIN_PATH"] = ""

from graphviz import Digraph

# Crear el objeto del grafo
dot = Digraph(comment='Mapa sinoptico de Administracion de Servidores')

# Nodo principal
dot.node('A', 'Administracion de los Servidores', shape='box', style='filled', color='#2E86C1', fontcolor='white')

# Subtemas
dot.node('B', 'Monitoreo de Red', shape='box', style='filled', color='#AED6F1')
dot.node('C', 'Monitoreo de Memoria', shape='box', style='filled', color='#AED6F1')
dot.node('D', 'Monitoreo de CPU', shape='box', style='filled', color='#AED6F1')
dot.node('E', 'Monitoreo de Procesos', shape='box', style='filled', color='#AED6F1')

# Conexiones
dot.edges(['AB', 'AC', 'AD', 'AE'])

# Exportar a archivo
dot.save('mapa_sinoptico.dot')

print("Archivo DOT generado en 'mapa_sinoptico.dot'")
