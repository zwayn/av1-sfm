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


import pytest

from ..modules.io import check_ivf_file
from .config.io_test_config import IoTestConfig


@pytest.mark.parametrize(
    "input_path, expected_result", 
    IoTestConfig.check_ivf_file
)
def test_ivf_file(input_path, expected_result):
    result = check_ivf_file(input_path)
    assert result == expected_result
