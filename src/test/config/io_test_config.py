'''
 # @ : io_test_config.py
 # @ Created by: Julien Zouein
 # @ Create Time: 2025-02-05
 # @ Copyright: © 2024 Sigmedia.tv. All rights reserved.
 # @          : © 2024 Julien Zouein (zoueinj@tcd.ie).
 # @ Modified by: Julien Zouein
 # @ Modified time: 2025-02-05
 # @  :----------------------------------------------------------------------------:
 # @ Description: Config for the io test.
 '''


class IoTestConfig:
    check_ivf_file = [
        ("src/test/data/test_subdataset.ivf", True),
        ("src/test/data/000046.avi", False),
    ]
