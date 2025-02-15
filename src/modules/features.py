'''
 # @ : features.py
 # @ Created by: Julien Zouein
 # @ Create Time: 2025-02-06
 # @ Copyright: © 2024 Sigmedia.tv. All rights reserved.
 # @          : © 2024 Julien Zouein (zoueinj@tcd.ie).
 # @ Modified by: Julien Zouein
 # @ Modified time: 2025-02-06
 # @  :----------------------------------------------------------------------------:
 # @ Description: All the functions to extract features and do the matching.

 This file contains all the functions we use to extract features and do the matching.
 Whether it is traditional methods (SIFT, etc) or experimental methods (AV1 related).
 '''

import itertools
import os

import ijson
import loguru
import numpy as np
import pandas as pd
from tqdm import tqdm

from .json_processing import get_block_map
from .json_processing import get_frame_ref_index
from .json_processing import get_motion_vectors
from .json_processing import get_reference_frame

def av1_features_and_matching(temp_folder: str, logger: loguru.Logger) -> None:
    """ Extract features and do the matching.

    Usually, to perform structure from motion, we used algorithms like SIFT to
    extract features and descriptors from an image and then we match those features
    between images. In our case we want to do the same but using AV1 features.

    The steps are the following:
        1. Extract block information from the image and use them as features.
        2. Extract motion vectors from the encoded video.
        3. Use motion vectors to do block matching.
    """

    logger.info("Getting the frame reference index.")
    frames_ref_index = get_frame_ref_index(temp_folder)

    logger.debug(f"Frame reference index: {frames_ref_index}")

    json_file_path = f"{temp_folder}/video.json"

    os.makedirs(f"{temp_folder}/block_maps", exist_ok=True)

    number_frame = len([name for name in os.listdir(f"{temp_folder}/images") if os.path.isfile(name)])

    # List of pandas dataframes to store the matches for each frame.
    matches = [pd.DataFrame(columns=["feature_coord", "feature_id", "target_frame", "coord_target", "feature_id_target"]) for _ in range(number_frame-1)]

    with open(json_file_path, "rb") as json_file:
        for frame_data in tqdm(ijson.items(json_file, "frame"), desc="Processing frames"):

            frame_number = frame_data["frame"]

            logger.debug(f"Frame number: {frame_number}")
            
            frame_ref_index = eval(frames_ref_index[frame_number])
            logger.debug(f"Frame reference index: {frame_ref_index}")

            current_block_map, coord_block = get_block_map(frame_data, temp_folder)
            np.save(f"{temp_folder}/block_maps/frame_{frame_number}.npy", current_block_map)

            if frame_number == 0:
                continue

            motion_vectors = get_motion_vectors(frame_data)
            reference_frame = get_reference_frame(frame_data, frame_ref_index)

            matches = _av1_match(coord_block, motion_vectors, reference_frame, matches, frame_number)

    matches = _av1_convert_matches(temp_folder, matches, current_block_map)

    for match in matches:
        match.drop(columns=['feature_coord', 'coord_target'], inplace=True)

    matches = _av1_propagate_matches(matches)


def _av1_convert_matches(temp_folder: str, matches: list[pd.DataFrame], current_block_map: np.ndarray) -> list[pd.DataFrame]:
    """ Convert the coordinates to the block index.

    Args:
        temp_folder: The temporary folder.
        matches: The matches updated.
    Returns:
        matches: The updated matches with feature IDs populated.
    """

    for i in range(len(matches)):
            
        for idx, row in matches[i].iterrows():

            current_coord = row['feature_coord']
            target_coord = row['coord_target']
            target_frame = row['target_frame']
            
            # Get feature IDs from block maps
            feature_id = current_block_map[current_coord[1], current_coord[0]]
            
            # Load target frame block map
            target_block_map = np.load(f"{temp_folder}/block_maps/frame_{target_frame}.npy")
            feature_id_target = target_block_map[target_coord[1], target_coord[0]]
            
            # Update the dataframe
            matches[i].at[idx, 'feature_id'] = feature_id
            matches[i].at[idx, 'feature_id_target'] = feature_id_target
    
    return matches


def _av1_propagate_matches(matches: list[pd.DataFrame]) -> list[pd.DataFrame]:
    """ Propagate the matches to other frames.

    We have matches between certain frames. the idea is to propagate those matches
    to other frames that are not directly connected.

    We have a block in frame A connected by a motion vector to a block in frame B.
    That same block is connected to another block in frame C. So we can create a
    new match between frame A and C.

    Args:
        matches: The matches to propagate.
    Returns:
        matches: The updated matches with feature IDs populated.
    """

    for i in range(1, len(matches)):

        index = len(matches) - i - 1

        dataframe = matches[index]

        for idx, row in dataframe.iterrows():

            target_frame = row['target_frame']
            id_target = row['feature_id_target']

            matches_target = matches[target_frame]

            # Get all rows matching id_target
            matches_target = matches_target[matches_target['feature_id_target'] == id_target]

            # Modify feature_id for all the rows
            matches_target['feature_id'] = id_target

            # Concatenate the current dataframe with the matches_target dataframe
            dataframe = pd.concat([dataframe, matches_target], ignore_index=True)

        matches[index] = dataframe
        matches[index].drop_duplicates(inplace=True)

    return matches



def _av1_match(
    coord_block: list[list[int]], 
    motion_vectors: np.ndarray, 
    reference_frame: np.ndarray, 
    matches: list[pd.DataFrame],
    frame_number: int
) -> list[pd.DataFrame]:
    """ Do the matching between the current frame and its references.

    The matching is done by using the motion vectors and the reference frame.
    The motion vectors are pointing towards a reference frame. AV1 uses a 
    buffer of 7 frames that can be used as a reference frame for a block.

    Moreover based on how the motion vectors are computed during the encoding
    process, we can interpolate the motion vectors to get matches with in-between
    frames.

    This function retrieves the matches using the motion vectors and the reference
    and compute the interpolated matches.

    Args:
        coord_block: The list of the center coordinates of the blocks.
        motion_vectors: The motion vectors.
        reference_frame: The reference frame.
        matches: Pandas dataframe to store the matches.
        frame_number: The current frame number.
    Returns:
        matches: The updated matches.
    """

    frames = [frame_number]

    for i in range(len(coord_block)):

        current_block_x, current_block_y = coord_block[i]

        motion_vectors = motion_vectors[current_block_y, current_block_x]
        references_frame = reference_frame[current_block_y, current_block_x]

        target_coord_1 = [int(current_block_x + motion_vectors[0]), int(current_block_y + motion_vectors[1])]
        target_coord_2 = [int(current_block_x + motion_vectors[2]), int(current_block_y + motion_vectors[3])]
        
        target_frame_1 = references_frame[target_coord_1[0]][target_coord_1[1]][0]
        target_frame_2 = references_frame[target_coord_2[0]][target_coord_2[1]][1]

        coords_motion = {}

        if (motion_vectors[0] != 0 or motion_vectors[1] != 0) and target_frame_1 != -1:

            frames.append(target_frame_1)

            coords_motion[frame_number] = coord_block[i]
            coords_motion[target_frame_1] = target_coord_1

            if target_frame_1 > frame_number:
                distance = target_frame_1 - frame_number
                next = -1
            
            else:
                distance = frame_number - target_frame_1
                next = 1

            unitary_motion = [motion_vectors[0] / distance, motion_vectors[1] / distance]
            
            for j in range(distance):

                interpolate_coord = [int(current_block_x + unitary_motion[0] * j), int(current_block_y + unitary_motion[1] * j)]
                next_frame = target_frame_1 + (j * next)
                coords_motion[next_frame] = interpolate_coord

        if (motion_vectors[2] != 0 or motion_vectors[3] != 0) and target_frame_2 != -1:

            frames.append(target_frame_2)

            if target_frame_2 > frame_number:
                distance = target_frame_2 - frame_number
                next = -1

            else:
                distance = frame_number - target_frame_2
                next = 1

            for j in range(distance):

                next_frame = target_frame_2 + (j * next)
                current_coord = [int(current_block_x + unitary_motion[0] * j), int(current_block_y + unitary_motion[1] * j)]
                coords_motion[next_frame] = current_coord

        min_frame = min(frames)
        max_frame = max(frames)

        # Get all frames numbers between min and max.
        frames_numbers = list(range(min_frame, max_frame + 1))

        pairs = list(itertools.combinations(frames_numbers, 2))

        for pair in pairs:

            frame_1, frame_2 = pair

            coord_1 = coords_motion[frame_1]
            coord_2 = coords_motion[frame_2]

            matches[frame_1].loc[-1] = [coord_1, None, frame_2, coord_2, None]

    return matches
