'''
 # @ : test_json_processing.py
 # @ Created by: Julien Zouein
 # @ Create Time: 2025-02-05
 # @ Copyright: © 2024 Sigmedia.tv. All rights reserved.
 # @          : © 2024 Julien Zouein (zoueinj@tcd.ie).
 # @ Modified by: Julien Zouein
 # @ Modified time: 2025-02-05
 # @  :----------------------------------------------------------------------------:
 # @ Description: File used to test the json_processing module.
 '''

import os

import cv2
import numpy as np
import pytest

from ..modules.json_processing import _compute_angle
from ..modules.json_processing import get_block_map
from ..modules.json_processing import get_frame_ref_index
from ..modules.json_processing import get_motion_vectors
from ..modules.json_processing import get_reference_frame

from .config.json_processing_test_config import JsonProcessingTestConfig


@pytest.mark.parametrize(
    "input_path, expected_output", 
    JsonProcessingTestConfig.get_frame_ref_index
)
def test_get_frame_ref_index(input_path, expected_output):
    assert get_frame_ref_index(input_path) == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    JsonProcessingTestConfig.get_motion_vectors
)
def test_get_motion_vectors(input, expected_output):
    input = np.array(input)
    expected_output = np.array(expected_output)
    frame_data = {"motionVectors": input}
    assert np.array_equal(get_motion_vectors(frame_data), expected_output)


@pytest.mark.parametrize(
    "input, order_hint, expected_output",
    JsonProcessingTestConfig.get_reference_frame
)
def test_get_reference_frame(input, order_hint, expected_output):
    input = np.array(input)
    expected_output = np.array(expected_output)
    frame_data = {"referenceFrame": input}
    assert np.array_equal(get_reference_frame(frame_data, order_hint), expected_output)


@pytest.mark.parametrize(
    "input_path, expected_output",
    JsonProcessingTestConfig._compute_angle
)
def test__compute_angle(input_path, expected_output):

    image = cv2.imread(input_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    angle = np.rad2deg(_compute_angle(image, 9))
    
    interval_result = expected_output - 0.1 < angle < expected_output + 0.1
    assert interval_result


@pytest.mark.parametrize(
    "blockSize, temp_folder, frame_number, feat_path, block_map_path, coord_ref",
    JsonProcessingTestConfig.get_block_map
)
def test_get_block_map(blockSize, temp_folder, frame_number, feat_path, block_map_path, coord_ref):
    
    metadata = {
        "frame": frame_number,
        "blockSize": blockSize
    }

    block_map, coord_test = get_block_map(metadata, temp_folder)
    
    block_map_ref = np.load(block_map_path)

    assert np.array_equal(block_map, block_map_ref)
    assert np.array_equal(coord_test, coord_ref)

    # check that both feat files are identical
    with open(feat_path, "r") as feat_file:
        feat_ref = feat_file.readlines()

    with open(feat_path, "r") as feat_file:
        feat_test = feat_file.readlines()

    assert feat_ref == feat_test

    os.remove("src/test/data/get_block_map/frame_0.feat")
