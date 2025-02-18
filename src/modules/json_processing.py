'''
 # @ : json_processing.py
 # @ Created by: Julien Zouein
 # @ Create Time: 2025-02-04
 # @ Copyright: © 2024 Sigmedia.tv. All rights reserved.
 # @          : © 2024 Julien Zouein (zoueinj@tcd.ie).
 # @ Modified by: Julien Zouein
 # @ Modified time: 2025-02-04
 # @  :----------------------------------------------------------------------------:
 # @ Description: File used to define all the functions to process the AV1 JSON.

 AOM inspect tool is used to retrieve metadata out of AV1 files. This tool save 
 the matadata in a JSON file.
 In this file, we define all the functions to process the JSON file.
 '''


import os
import subprocess

import cv2
import numpy as np
import re


block_size = {
    0: [4, 4],
    1: [4, 8],
    2: [8, 4],
    3: [8, 8],
    4: [8, 16],
    5: [16, 8],
    6: [16, 16],
    7: [16, 32],
    8: [32, 16],
    9: [32, 32],
    10: [32, 64],
    11: [64, 32],
    12: [64, 64],
    13: [64, 128],
    14: [128, 64],
    15: [128, 128],
    16: [4, 16],
    17: [16, 4],
    18: [8, 32],
    19: [32, 8],
    20: [16, 64],
    21: [64, 16],
}


def get_block_map(frame_metadata: dict, temp_folder: str) -> np.ndarray:
    """ This function is used to get the block map out of AV1 bitstream.

    Args:
        frame_metadata: Metadata of the frame.
        temp_folder: Path to the temporary folder.
    Returns:
        A numpy array of the block map.
    """

    block_size_data = np.array(frame_metadata["blockSize"])

    height, width = block_size_data.shape

    coord_block = []
    frame_number = frame_metadata["frame"]
    
    result = np.zeros((4*height, 4*width), dtype=int)

    block_index = 1

    image_path = f"{temp_folder}/images/frame_{frame_number}.png"
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    for i in range(height):
        for j in range(width):

            if result[i*4, j*4] == 0:

                block_identifier = block_size_data[i, j]

                block_width, block_height = block_size[block_identifier]

                result[i*4:i*4+block_height, j*4:j*4+block_width] = block_index
                block_index += 1

                block_center_x = (j*4) + ((block_width-1) / 2)
                block_center_y = (i*4) + ((block_height-1) / 2)

                minimal_block_size = min(block_width, block_height)

                x_patch = int(block_center_x - minimal_block_size//2)
                y_patch = int(block_center_y - minimal_block_size//2)

                coord_block.append([block_center_x, block_center_y])

                block_patch = image[y_patch:y_patch+minimal_block_size, x_patch:x_patch+minimal_block_size]

                angle = _compute_angle(block_patch, minimal_block_size)

                with open(f"{temp_folder}/frame_{frame_number}.feat", mode="a", encoding="utf-8") as feat_file:
                    feat_file.write(f"{block_center_x} {block_center_y} {minimal_block_size} {angle}\n")

    result = result - 1

    return result, coord_block

def get_frame_ref_index(temp_folder: str) -> list[list[int]]:
    """ This function is used to get the order hints out of AV1 bitstream.

    When processing the metadata, if we check from reference frame index, we have
    a number representing the type of frame (last, golden, etc). However, in our
    case we would rather have the frame number.
    The conversion array between frame type and frame number is the order hints.

    Args:
        temp_folder: Path to the temporary folder.

    Returns:
        A list of all the order hints (list of integers).
    """

    # Call av1parser tool to analyze the bitstrean and save this analysis in a txt file.
    command = f"cd src/third_parties/av1parser && cargo run ../../../{temp_folder}/video.ivf -vv"
    command += f" > ../../../{temp_folder}/output_bitstream.txt && cd ../../.."
    
    subprocess.run(command, shell=True)

    # Define a RegEx pattern to find the order hints in the txt file.
    pattern = re.compile("order_hints: \[(.*?)\]")

    # Read the txt file and find the order hints.
    with open(f"{temp_folder}/output_bitstream.txt", mode="rt", encoding="utf-8") as docFile:
        doc = docFile.read()
        refs_frame_index = re.findall(pattern, doc)

    # Remove the txt file.
    os.remove(f"{temp_folder}/output_bitstream.txt")

    return refs_frame_index


def get_motion_vectors(frame_metadata: dict) -> np.ndarray:
    """ This function is used to get the motion vectors out of AV1 bitstream.

    Args:
        frame_metadata: Metadata of the frame.

    Returns:
        A numpy array of motion vectors with 4 channels. first two are backward motion
        and the last two are forward motion.
    """

    # AV1 has 1/* pixel precision. Therefore motion vectors are divided by 8.
    motion_vectors = np.array(frame_metadata["motionVectors"]) / 8

    motion_vectors = _inverse_motion(motion_vectors)

    # the array is 1/16 of the size of the frame. we upsample it by giving the same value to all the new pixels.
    height, width, _ = motion_vectors.shape
    motion_vectors = cv2.resize(motion_vectors, (width * 4, height * 4), interpolation=cv2.INTER_NEAREST)

    return motion_vectors


def get_reference_frame(frame_metadata: dict, order_hint: list[int]) -> np.ndarray:
    """ This function is used to get the reference frame out of AV1 bitstream.

    Args:
        frame_metadata: Metadata of the frame.
        order_hint: Order hint of the frame.

    Returns:
        A numpy array of the reference frame.
    """

    reference_frame = np.array(frame_metadata["referenceFrame"])

    mapping = np.array(order_hint)
    # Use the references as indices into the mapping array
    reference_frame_index =  mapping[reference_frame]

    height, width, _ = reference_frame_index.shape

    reference_frame_index = cv2.resize(reference_frame_index, (width * 4, height * 4), interpolation=cv2.INTER_NEAREST)

    return reference_frame_index


def _compute_angle(block_patch: np.array, size: int) -> float:
    """ This function is used to compute the main orientation of the gradient of the block.

    Implementation is similar to the one used for RAISR paper.

    Args:
        block_patch: Patch of the block.
        size: Size of the block.

    Returns:
        The main angle of the block.
    """

    weighting = _gaussian2d([size, size], 2)
    weighting = np.diag(weighting.ravel())

    block_patch = block_patch.astype(np.float32)

    block_patch = cv2.resize(block_patch, (size, size))

    gy, gx = np.gradient(block_patch)

    gx = gx.ravel()
    gy = gy.ravel()

    g = np.vstack((gx,gy)).T
    gtwg = g.T.dot(weighting).dot(g)
    w, v = np.linalg.eig(gtwg)

    nonzerow = np.count_nonzero(np.isreal(w))
    nonzerov = np.count_nonzero(np.isreal(v))
    if nonzerow != 0:
        w = np.real(w)
    if nonzerov != 0:
        v = np.real(v)

    # Sort w and v according to the descending order of w
    idx = w.argsort()[::-1]
    w = w[idx]
    v = v[:,idx]

    # Get the angle
    angle = np.arctan2(v[1,0], v[0,0])

    if angle < 0:
        angle = angle + np.pi

    return angle


def _gaussian2d(shape=(3,3),sigma=0.5):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h


def _inverse_motion(motion_vectors:np.array) -> np.array:
    """ This function is used to fill missing motion vectors.

    In some cases, the encoder does not compute a motion for a specific block.
    It will, therefore, give us a (0, 0) motion vector even though the motion
    is not zero.
    Each block has a backward and forward motion vector. To fill the missing
    motion vector (for example forward), we take the inverse backward motion
    vector.

    Args:
        motion_vectors: The motion vector array.

    Returns:
        motion_vectors: The filled motion vector array.
    """

    result = motion_vectors.copy()
    
    # Create masks for zero vectors
    backward_zero = (result[..., 0] == 0) & (result[..., 1] == 0)
    forward_zero = (result[..., 2] == 0) & (result[..., 3] == 0)
    
    # Update where backward is zero
    result[backward_zero, 0] = -result[backward_zero, 2]
    result[backward_zero, 1] = -result[backward_zero, 3]
    
    # Update where forward is zero
    result[forward_zero, 2] = -result[forward_zero, 0]
    result[forward_zero, 3] = -result[forward_zero, 1]

    return result


def _get_reference_frame_number(reference_frame: np.array, order_hint: list[int]) -> np.array:
    """ This function is used to get the reference frame number out of AV1 bitstream.

    Args:
        reference_frame: The reference frame.
        order_hint: The order hint.

    Returns:
        The reference frame number.
    """

    result = order_hint[int(reference_frame)]

    return result
