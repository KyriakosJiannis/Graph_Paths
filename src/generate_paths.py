import pandas as pd
import numpy as np
from scipy.spatial import distance


def nearest_neighbor_triangle_route(coords, k=None):
    """
    Nearest Nearest neighbor search based on triange distance
    source is the first row 0 and target is the last

    Parameters
    ----------------
    @param: coords the coordinate array
    @param: k the nearest neighbor search step
    @return:
    """

    # Calculate and store the distance
    distances = distance.cdist(coords, coords, 'euclidean')
    dist = distances.copy()

    # Set the first step, our source is the 0
    ix = 0  # refers to station index
    routes = [0]  # indexes for the path
    edge_distance = [0]  # will append each edge distance

    # Set position and edge distances
    end_station = len(distances) - 1  # index for target
    start2end_dist = distances[0, end_station]  # source target distance
    all2end_dist = distances[0:end_station, end_station]  # all node distances

    # We will mask with zeros nodes that we do not need to select, saving computations
    # Zeros where the distances are higher than started - ended
    distances = np.where(distances > start2end_dist, 0, distances)
    to_exclude = distances[:, end_station] == 0
    to_exclude[end_station] = False  # keep end station
    distances[:, to_exclude] = 0
    distances[to_exclude, :] = 0
    # exclude nodes where
    to_exclude = distances[:, 0] == 0
    to_exclude[0] = False
    distances[:, to_exclude] = 0
    distances[to_exclude, :] = 0

    while ix < end_station:  # ix current node, n the next node, loop ending when ix=n=end station

        # mask with zeros, not taking part in calculations
        dd_mask = np.ma.masked_equal(distances, 0.0, copy=False)
        # for each selected node find the Nearest Distance
        min_edge = dd_mask[ix, :].min()

        if ix == 0 and start2end_dist == min(all2end_dist):
            # if [started-ended] distance is the smaller there is not route
            # the only path to go to final destination is started ---> ended
            print("There is not any path, the only path is start-ended")
            routes = [0, end_station]
            edge_distance.append(start2end_dist)
            # data frame where store each step results
            out_df = pd.DataFrame(list(zip(routes, edge_distance)), columns=['routes', 'edge_distance'])
            out_df["distance_to_end"] = distances[out_df["routes"], end_station]
            # total distance
            total_distance = sum(edge_distance)
            break
        else:
            # mask steps, not to get into the loop, next step is nearest to ended point
            triangle_dis = dd_mask[end_station, :] + distances[:, ix]
            triangle_dis = np.ma.masked_where(triangle_dis == triangle_dis[ix], triangle_dis)

            if k is not None:
                triangle_edge_dis = dd_mask[ix, :len(dd_mask[ix])]  # k=len if none
                anti_mask = triangle_edge_dis.argsort()[:k]  # find the k mim dis to search
                falsies = np.full(len(dd_mask[ix]), True)  # create the mask
                falsies[anti_mask] = False  # create the mask
                triangle_edge_dis.mask = falsies  # populate the mask
                triangle_dis.mask = triangle_edge_dis.mask  # update triangle dis

            if np.min(np.ma.masked_equal(distances[ix], 0.0, copy=False)) == distances[ix, end_station]:
                # if the ix records the min distance to end, then n is the last station
                n = end_station
            else:
                n = np.where(triangle_dis == np.min(triangle_dis))
                # finds the next which has the min distance to end
                n = n[0][0]
                if distances[ix, end_station] < distances[n, end_station] and k is None:
                    # if the next node records larger distance, don't select and go end
                    n = end_station
                elif distances[ix, end_station] < distances[n, end_station] and k is not None:
                    # if the next node records larger distance, don't select and go next
                    distances[:, n] = 0
                    distances[n, :] = 0
                    continue
                elif distances[ix, n] > distances[ix, end_station]:
                    # if the distance to end is smaller on current node than next go to end
                    n = end_station
                else:
                    pass

            routes.append(n)  # update routes
            edge_distance.append(dist[ix, n])  # populate edge distance
            distances[:, ix] = 0
            distances[ix, :] = 0  # set zero the whole node not be selected again!
            ix = n
            print("selected node:", ix)

        # data frame where store each step results
        out_df = pd.DataFrame(list(zip(routes, edge_distance)), columns=['routes', 'edge_distance'])
        out_df["distance_to_end"] = dist[out_df["routes"], end_station]
        # total distance
        total_distance = sum(edge_distance)

    return dist, routes, edge_distance, total_distance, out_df
