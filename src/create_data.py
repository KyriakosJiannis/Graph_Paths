import numpy as np
import pandas as pd
import src.confiq


class CreateInputs:
    """
    Generate data with started point always zeros and returns as numpy array and dataframe as
    """

    def __init__(self, N, space, min_max, random_seed):
        self.N = N
        self.space = space
        self.min_max = min_max
        self.random_seed = random_seed

    def generate(self):
        """
        :param N: set the total number of stations
        :param space: 2d or 3d space
        :param min_max: set the max and min coordinate
        :param random_seed: default 1
        :return: numpy array and pandas dataframe
        :param
        """
        np.random.seed(seed=self.random_seed)

        if self.space == "3d":
            coordinates = np.vstack(
                [[0, 0, 0], np.random.randint(-self.min_max, self.min_max, size=(self.N - 1, 3))]
            )

            coordinates_pd = pd.DataFrame(
                {
                    "x": coordinates[:, 0],
                    "y": coordinates[:, 1],
                    "z": coordinates[:, 2],
                    "label": np.repeat(
                        np.array(["Started Point", "Med Point", "Final Point"]),
                        [1, self.N - 2, 1],
                        axis=0,
                    ),
                }
            )

        elif self.space == "2d":

            coordinates = np.vstack(
                [[0, 0], np.random.randint(-self.min_max, self.min_max, size=(self.N - 1, 2))]
            )

            coordinates_pd = pd.DataFrame(
                {
                    "x": coordinates[:, 0],
                    "y": coordinates[:, 1],
                    "label": np.repeat(
                        np.array(["Started Points", "Med Points", "Final Points"]),
                        [1, self.N - 2, 1],
                        axis=0,
                    ),
                }
            )

        return coordinates, coordinates_pd
