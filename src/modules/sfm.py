'''
 # @ : sfm.py
 # @ Created by: Julien Zouein
 # @ Create Time: 2025-02-06
 # @ Copyright: © 2024 Sigmedia.tv. All rights reserved.
 # @          : © 2024 Julien Zouein (zoueinj@tcd.ie).
 # @ Modified by: Julien Zouein
 # @ Modified time: 2025-02-06
 # @  :----------------------------------------------------------------------------:
 # @ Description:
 '''

import itertools
import os

import numpy as np
import pandas as pd


def image_adjacency_matrix(matches: list[pd.DataFrame], threshold: int = 25, temp_folder: str = "temp") -> np.ndarray:
    """ Create the adjacency matrix of the image.

    The adjacency matrix is a matrix that represents the connections between
    the frames.

    Args:
        matches: The matches between the frames.
        threshold: The threshold for the matches (%).
        temp_folder: The folder to save the block maps.
    Returns:
        The adjacency matrix.
    """

    number_frame = len([name for name in os.listdir(f"{temp_folder}/images") if os.path.isfile(name)])

    adjacency_matrix = np.zeros((number_frame, number_frame))
    result_pairs = []

    frames_numbers = list(range(0, number_frame + 1))

    pairs = list(itertools.combinations(frames_numbers, 2))

    for pair in pairs:

        dataframe = matches[pair[0]]

        dataframe_filtered = dataframe[dataframe['target_frame'] == pair[1]]

        dataframe_filtered["coverage"] = _compute_coverage(index=dataframe_filtered["feature_id"], block_map=f"{temp_folder}/block_maps/frame_{pair[0]}.npy")
        coverage = dataframe_filtered["coverage"].sum()

        if coverage >= threshold:
            adjacency_matrix[pair[0], pair[1]] = 1
            result_pairs.append(pair)

    return adjacency_matrix, result_pairs


def _compute_coverage(index: pd.Index, block_map: str) -> float:
    """ Compute the coverage of matches.

    We compute the block coverage of the frame between two matches.

    Args:
        index: The index of the matches.
        block_map: The block map.
    Returns:
        The coverage of the matches (%).
    """

    block = np.load(block_map)

    coverage = np.mean(block == index) * 100

    return coverage