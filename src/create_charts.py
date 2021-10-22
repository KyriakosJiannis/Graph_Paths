import src.confiq

import sys
import os
import pandas as pd
import numpy as np
import plotly.express as px
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
# import ffmpeg

from scipy.spatial import distance
from scipy.sparse.csgraph import shortest_path, dijkstra
from sklearn.utils.graph_shortest_path import graph_shortest_path
import networkx as nx


def plot_2d_network(coordinates,  routes=None,  output_name='out', path_to_save=None, title=None, **kwargs):
    """
    function which returns on matplotlib the coordinates and flag
    the started point and destination

    Parameters
    ----------

    :param coordinates: numpy array with coordinates
    :param routes:
    :param output_name:
    :param path_to_save:
    :param kwargs: matplotlib plt.figure kwargs
    :return: matplotlib plot or png images on pictures
    """
    fig = plt.figure(**kwargs)
    plt.title(label=title)
    plt.scatter(coordinates[:, 0], coordinates[:, 1], c='Orange')

    # TODO PLOTLY

    if routes is not None:
        plt.plot(coordinates[routes, 0], coordinates[routes, 1], c="r")

    plt.scatter(0, 0, marker="X", c='b')
    plt.scatter(coordinates[len(coordinates) - 1, 0], coordinates[len(coordinates) - 1, 1], marker="D", c='g')

    if path_to_save is not None:
        #plt.savefig(os.path.join(src.confiq.OUTPUT_DIR_PIC, output_name + ".png").replace("\\", "/"), format="PNG")
        plt.savefig(os.path.join(src.confiq.OUTPUT_DIR_PIC, output_name + ".png"), format="PNG")
        plt.close(fig)
    else:
        plt.show()


def plot_3d_network(coordinates_df,  routes=None, output_name='out3d', path_to_save=None, title=None,
                    **kwargs):
    """
    import the dataframe with 3D positions

    Parameters
    ----------
    :param output_name:
    :param path_to_save:
    :param routes:
    :param coordinates_df: dataframe with 3D positions
    :param title: Give a title in the chart
    :param routes: rows selections
    :returns plotly and matplotlib 3D

    """

    # add in dataframe the colors
    coordinates_df['colors'] = coordinates_df['label'].replace(
        {'Started Point': 'b',
         'Med Point': 'orange',
         'Final Point': 'g'}
    )

    # create a plotly
    fig = px.scatter_3d(
        coordinates_df,
        x='x', y='y', z='z',
        size_max=18,
        color='label',
        symbol='label',
        opacity=0.7
    )

    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        title={'text': title,
               'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'}
    )

    fig.write_html("temp.html", auto_open=True)

    # TODO route is not None for plotly

    # matplotlib
    fig = plt.figure(**kwargs)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(coordinates_df['x'], coordinates_df['y'], coordinates_df['z'], c=coordinates_df['colors'], s=100)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(title)
    # TODO legends with mpatches

    if routes is not None:
        routes = coordinates_df.iloc[routes]
        ax.plot(routes['x'], routes['y'], routes['z'], color='r')

    if path_to_save is not None:
        #plt.savefig(os.path.join(src.confiq.OUTPUT_DIR_PIC, output_name + ".png").replace("\\", "/"), format="PNG")
        plt.savefig(os.path.join(src.confiq.OUTPUT_DIR_PIC, output_name + ".png"), format="PNG")
        plt.close(fig)
    else:
        plt.show()
