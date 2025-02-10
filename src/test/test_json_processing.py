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


import cv2
import numpy as np
import pytest

from ..modules.json_processing import _compute_angle
from ..modules.json_processing import get_frame_ref_index

from .config.json_processing_test_config import JsonProcessingTestConfig


@pytest.mark.parametrize(
    "input_path, expected_output", 
    JsonProcessingTestConfig.get_frame_ref_index
)
def test_get_frame_ref_index(input_path, expected_output):
    assert get_frame_ref_index(input_path) == expected_output


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
