import src.confiq
import os
from src.create_data import CreateInputs
from src.create_charts import plot_2d_network, plot_3d_network
from src.generate_paths import nearest_neighbor_triangle_route
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import imageio

# Graph example 1
coords, coords_df = CreateInputs(N=10, space='2d', min_max=100, random_seed=1).generate()
coords[9, [0, 1]] = [70, -100]

d, routes, edge_distance, total_distance, df = nearest_neighbor_triangle_route(coords, k=1)
plot_2d_network(coords, output_name='example111', path_to_save=True)
plot_2d_network(coords, routes, output_name='example112', path_to_save=True)

G = nx.from_numpy_matrix(d)
G = nx.DiGraph(G)
# Add position
for ix in range(len(coords)):
    G.add_node(ix, pos=(coords[ix, 0], coords[ix, 1]))
pos = nx.get_node_attributes(G, 'pos')

f = plt.figure()
nx.draw_networkx(G, pos)
plt.close(f)
f = f.savefig(os.path.join(src.confiq.OUTPUT_DIR_PIC, 'example113' + ".png"))

## Gif, example
for ix in range(50, 70, 5):
    for n in range(50, 300, 10):
        for k in [1, 2, 3, 5, 10, None]:
            coords, coords_pd = CreateInputs(N=n, space='2d', min_max=100, random_seed=ix).generate()
            coords = np.vstack([coords, [70, -100]])
            d, routes, edge_distance, total_distance, df = nearest_neighbor_triangle_route(coords, k=k)

            def k2str(i):
                if i is None:
                    return '0'
                else:
                    i
                return str(i)

            plot_2d_network(coords,
                            title='Number of neighbors:' + str(k),
                            routes=routes,
                            output_name=str("gif/") + str(ix).zfill(3) + str(n).zfill(3) + k2str(k).zfill(3),
                            path_to_save=True)

png_dir = './output/pictures/gif'
images = []
for file_name in sorted(os.listdir(png_dir)):
    if file_name.endswith('.png'):
        file_path = os.path.join(png_dir, file_name)
        images.append(imageio.imread(file_path))
imageio.mimsave('./output/pictures/gif_2d_routes.gif', images, duration = 0.8)


# snippet

coords, coords_df = CreateInputs(N=100, space='2d', min_max=100, random_seed=1).generate()
d, routes, edge_distance, total_distance, df = nearest_neighbor_triangle_route(coords, k=1)
plot_2d_network(coords, routes, output_name='example221', path_to_save=True)


coords, coords_df = CreateInputs(N=300, space='3d', min_max=100, random_seed=1).generate()
d, routes, edge_distance, total_distance, df = nearest_neighbor_triangle_route(coords, k=1)
plot_3d_network(coords_df, routes, output_name='example221', path_to_save=True)
plot_3d_network(coords_df, routes)