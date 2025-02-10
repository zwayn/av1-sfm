'''
 # @ : json_processing_test_config.py
 # @ Created by: Julien Zouein
 # @ Create Time: 2025-02-05
 # @ Copyright: © 2024 Sigmedia.tv. All rights reserved.
 # @          : © 2024 Julien Zouein (zoueinj@tcd.ie).
 # @ Modified by: Julien Zouein
 # @ Modified time: 2025-02-05
 # @  :----------------------------------------------------------------------------:
 # @ Description: File used to define the configuration for the json_processing test.
 '''


class JsonProcessingTestConfig(object):

    get_frame_ref_index = [
        (
            "src/test/data/",
            [
                '0, 0, 0, 0, 0, 0, 0, 0', 
                '0, 0, 0, 0, 0, 0, 0, 0', 
                '0, 1, 0, 0, 0, 0, 0, 0', 
                '0, 2, 1, 0, 0, 0, 0, 0', 
                '0, 3, 2, 1, 0, 0, 0, 0', 
                '0, 3, 2, 1, 4, 0, 0, 0', 
                '0, 5, 3, 2, 4, 0, 1, 0', 
                '0, 6, 5, 3, 4, 0, 2, 1', 
                '0, 7, 6, 5, 4, 0, 3, 2', 
                '0, 7, 6, 5, 8, 0, 4, 3'
            ]
        )
    ]

    _compute_angle = [
        (
            "src/test/data/images/orientation/0_5.png",
            0
        ),
        (
            "src/test/data/images/orientation/45_5.png",
            45
        ),
        (
            "src/test/data/images/orientation/90_5.png",
            90
        ),
        (
            "src/test/data/images/orientation/135_5.png",
            135
        ),
        (
            "src/test/data/images/orientation/0_9.png",
            0
        ),
        (
            "src/test/data/images/orientation/45_9.png",
            45
        ),
        (
            "src/test/data/images/orientation/90_9.png",
            90
        ),
        (
            "src/test/data/images/orientation/135_9.png",
            135
        ),
        (
            "src/test/data/images/orientation/0_12.png",
            0
        ),
        (
            "src/test/data/images/orientation/45_12.png",
            45
        ),
        (
            "src/test/data/images/orientation/90_12.png",
            90
        ),
        (
            "src/test/data/images/orientation/135_12.png",
            135
        ),
    ]
