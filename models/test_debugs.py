import pandas as pd
import numpy as np
import os
import plotly.express as px
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
# import ffmpeg

from scipy.spatial import distance
from scipy.sparse.csgraph import shortest_path, dijkstra
from sklearn.utils.graph_shortest_path import graph_shortest_path
import networkx as nx

import src.confiq
from src.create_data import CreateInputs
from src.create_charts import plot_2d_network, plot_3d_network
from src.generate_paths import nearest_neighbor_triangle_route

import networkx as nx
from scipy.spatial import distance

# coords, coords_df = CreateInputs(N=500, space='2d', min_max=100, random_seed=50).generate()
# coords = np.vstack([coords, [70, -100]])
# plot_2d_network(coords)

# plot_3d_network(coords_df)
# d = distance.cdist(coords, coords, 'euclidean')
# G = nx.from_numpy_matrix(d)
# G = nx.DiGraph(G)

# Add position
# for ix in range(len(coords)):
#    G.add_node(ix, pos=(coords[ix, 0], coords[ix, 1]))

# pos = nx.get_node_attributes(G, 'pos')

# plot_2d_network(coords)

# plt.figure()
# nx.draw_networkx(G, pos)

# d, routes, edge_distance, Total_distance, df = generates_nearest_neighbor_triangle_route(coords, k=3)
# plot_2d_network(coords, routes)

# plot_3d_network(coords_df, routes=routes)


coords, coords_df = CreateInputs(N=100, space='3d', min_max=100, random_seed=1).generate()
d, routes, edge_distance, total_distance, df = nearest_neighbor_triangle_route(coords, k=1)
plot_3d_network(coords_df, routes, output_name='example221', path_to_save=True)
