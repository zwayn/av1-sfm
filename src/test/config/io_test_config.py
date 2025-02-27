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
        ("src/test/data/video.ivf", True),
        ("src/test/data/000046.avi", False),
    ]

    get_image_paths = [
        (
            "src/test/data/images/png/",
            [
                "src/test/data/images/png/frame_0001.png",
                "src/test/data/images/png/frame_0002.png",
                "src/test/data/images/png/frame_0003.png",
                "src/test/data/images/png/frame_0004.png",
                "src/test/data/images/png/frame_0005.png",
                "src/test/data/images/png/frame_0006.png",
                "src/test/data/images/png/frame_0007.png",
                "src/test/data/images/png/frame_0008.png",
                "src/test/data/images/png/frame_0009.png",
                "src/test/data/images/png/frame_0010.png",
                "src/test/data/images/png/frame_0011.png",
                "src/test/data/images/png/frame_0012.png",
                "src/test/data/images/png/frame_0013.png",
                "src/test/data/images/png/frame_0014.png",
                "src/test/data/images/png/frame_0015.png",
                "src/test/data/images/png/frame_0016.png",
                "src/test/data/images/png/frame_0017.png",
                "src/test/data/images/png/frame_0018.png",
                "src/test/data/images/png/frame_0019.png",
                "src/test/data/images/png/frame_0020.png",
                "src/test/data/images/png/frame_0021.png",
                "src/test/data/images/png/frame_0022.png",
                "src/test/data/images/png/frame_0023.png",
                "src/test/data/images/png/frame_0024.png",
                "src/test/data/images/png/frame_0025.png",
                "src/test/data/images/png/frame_0026.png",
                "src/test/data/images/png/frame_0027.png",
                "src/test/data/images/png/frame_0028.png",
                "src/test/data/images/png/frame_0029.png",
                "src/test/data/images/png/frame_0030.png",
                "src/test/data/images/png/frame_0031.png",
                "src/test/data/images/png/frame_0032.png",
                "src/test/data/images/png/frame_0033.png",
                "src/test/data/images/png/frame_0034.png",
                "src/test/data/images/png/frame_0035.png",
                "src/test/data/images/png/frame_0036.png",
                "src/test/data/images/png/frame_0037.png",
                "src/test/data/images/png/frame_0038.png",
                "src/test/data/images/png/frame_0039.png",
                "src/test/data/images/png/frame_0040.png",
                "src/test/data/images/png/frame_0041.png",
                "src/test/data/images/png/frame_0042.png",
                "src/test/data/images/png/frame_0043.png",
                "src/test/data/images/png/frame_0044.png",
                "src/test/data/images/png/frame_0045.png",
                "src/test/data/images/png/frame_0046.png",
                "src/test/data/images/png/frame_0047.png",
                "src/test/data/images/png/frame_0048.png",
                "src/test/data/images/png/frame_0049.png",
                "src/test/data/images/png/frame_0050.png",
            ]
        )
    ]


    copy_images = [
        (
            "src/test/data/images/png/",
            [   
                "src/test/data/images/test_dir/images/frame_0000.png",
                "src/test/data/images/test_dir/images/frame_0001.png",
                "src/test/data/images/test_dir/images/frame_0002.png",
                "src/test/data/images/test_dir/images/frame_0003.png",
                "src/test/data/images/test_dir/images/frame_0004.png",
                "src/test/data/images/test_dir/images/frame_0005.png",
                "src/test/data/images/test_dir/images/frame_0006.png",
                "src/test/data/images/test_dir/images/frame_0007.png",
                "src/test/data/images/test_dir/images/frame_0008.png",
                "src/test/data/images/test_dir/images/frame_0009.png",
                "src/test/data/images/test_dir/images/frame_0010.png",
                "src/test/data/images/test_dir/images/frame_0011.png",
                "src/test/data/images/test_dir/images/frame_0012.png",
                "src/test/data/images/test_dir/images/frame_0013.png",
                "src/test/data/images/test_dir/images/frame_0014.png",
                "src/test/data/images/test_dir/images/frame_0015.png",
                "src/test/data/images/test_dir/images/frame_0016.png",
                "src/test/data/images/test_dir/images/frame_0017.png",
                "src/test/data/images/test_dir/images/frame_0018.png",
                "src/test/data/images/test_dir/images/frame_0019.png",
                "src/test/data/images/test_dir/images/frame_0020.png",
                "src/test/data/images/test_dir/images/frame_0021.png",
                "src/test/data/images/test_dir/images/frame_0022.png",
                "src/test/data/images/test_dir/images/frame_0023.png",
                "src/test/data/images/test_dir/images/frame_0024.png",
                "src/test/data/images/test_dir/images/frame_0025.png",
                "src/test/data/images/test_dir/images/frame_0026.png",
                "src/test/data/images/test_dir/images/frame_0027.png",
                "src/test/data/images/test_dir/images/frame_0028.png",
                "src/test/data/images/test_dir/images/frame_0029.png",
                "src/test/data/images/test_dir/images/frame_0030.png",
                "src/test/data/images/test_dir/images/frame_0031.png",
                "src/test/data/images/test_dir/images/frame_0032.png",
                "src/test/data/images/test_dir/images/frame_0033.png",
                "src/test/data/images/test_dir/images/frame_0034.png",
                "src/test/data/images/test_dir/images/frame_0035.png",
                "src/test/data/images/test_dir/images/frame_0036.png",
                "src/test/data/images/test_dir/images/frame_0037.png",
                "src/test/data/images/test_dir/images/frame_0038.png",
                "src/test/data/images/test_dir/images/frame_0039.png",
                "src/test/data/images/test_dir/images/frame_0040.png",
                "src/test/data/images/test_dir/images/frame_0041.png",
                "src/test/data/images/test_dir/images/frame_0042.png",
                "src/test/data/images/test_dir/images/frame_0043.png",
                "src/test/data/images/test_dir/images/frame_0044.png",
                "src/test/data/images/test_dir/images/frame_0045.png",
                "src/test/data/images/test_dir/images/frame_0046.png",
                "src/test/data/images/test_dir/images/frame_0047.png",
                "src/test/data/images/test_dir/images/frame_0048.png",
                "src/test/data/images/test_dir/images/frame_0049.png",
            ],
        )
    ]
