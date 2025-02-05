'''
 # @ : test_io.py
 # @ Created by: Julien Zouein
 # @ Create Time: 2025-02-05
 # @ Copyright: © 2024 Sigmedia.tv. All rights reserved.
 # @          : © 2024 Julien Zouein (zoueinj@tcd.ie).
 # @ Modified by: Julien Zouein
 # @ Modified time: 2025-02-05
 # @  :----------------------------------------------------------------------------:
 # @ Description: Test the io module.
 '''

import os
import shutil
import pytest

from ..modules.io import check_ivf_file
from ..modules.io import copy_images
from ..modules.io import get_image_paths
from .config.io_test_config import IoTestConfig


@pytest.mark.parametrize(
    "input_path, expected_result", 
    IoTestConfig.check_ivf_file
)
def test_ivf_file(input_path, expected_result):
    result = check_ivf_file(input_path)
    assert result == expected_result


@pytest.mark.parametrize(
    "input_path, expected_result",
    IoTestConfig.copy_images
)
def test_copy_images(input_path, expected_result):

    # Create a temporary folder.
    os.makedirs("src/test/data/images/test_dir", exist_ok=True)

    image_paths = get_image_paths(input_path)

    copy_images(image_paths, "src/test/data/images/test_dir")

    # Get the paths of the images in the temporary folder.
    image_paths = get_image_paths("src/test/data/images/test_dir")

    assert image_paths == expected_result

    # Remove the temporary folder.
    shutil.rmtree("src/test/data/images/test_dir")


@pytest.mark.parametrize(
    "input_path, expected_result",
    IoTestConfig.get_image_paths
)
def test_get_image_paths(input_path, expected_result):
    result = get_image_paths(input_path)

    assert result == expected_result