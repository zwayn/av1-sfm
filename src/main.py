'''
 # @ : main.py
 # @ Created by: Julien Zouein
 # @ Create Time: 2025-02-04
 # @ Copyright: © 2024 Sigmedia.tv. All rights reserved.
 # @          : © 2024 Julien Zouein (zoueinj@tcd.ie).
 # @ Modified by: Julien Zouein
 # @ Modified time: 2025-02-04
 # @  :----------------------------------------------------------------------------:
 # @ Description: Main file to run the application.
 '''


import os
import tempfile

from datetime import datetime
from tqdm import tqdm

from .modules.io import check_ivf_file
from .modules.io import copy_video
from .modules.io import generate_json
from .modules.io import process_images
from .modules.json_processing import get_frame_ref_index
from .modules.logger import start_logger


def main(
    encoding_preset: str = "preset_1",
    image_path: str = None,
    video_path: str = None,
    logger_level: str = "INFO",
):

    # Start logger.
    logger = start_logger(
        path="output",
        level=logger_level
    )

    logger.info("Starting processing...")

    logger.info("Generating temporary folder.")
    # Generate a temporary folder.
    temp_folder = tempfile.mkdtemp()


    if image_path:
        logger.info(f"Images as input.")

        process_images(image_path, temp_folder, encoding_preset=encoding_preset)

    else:
        logger.info("No images as input.")
        logger.info("Copying video to temporary folder.")
        copy_video(video_path, temp_folder)

    logger.info("Checking if the video is an ivf file.")
    if check_ivf_file(os.path.join(temp_folder, "video.ivf")):
        logger.info("Video is an ivf file.")
    else:
        logger.info("Video is not an ivf file.")
        exit(1)
    
    logger.info("Processing the video.")
    generate_json(temp_folder)
