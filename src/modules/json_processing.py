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

import re


def get_frame_ref_index(logger,input_path: str, output_path: str) -> list[int]:
    """ This function is used to get the order hints out of AV1 bitstream.

    When processing the metadata, if we check from reference frame index, we have
    a number representing the type of frame (last, golden, etc). However, in our
    case we would rather have the frame number.
    The conversion array between frame type and frame number is the order hints.

    Args:
        logger: Loguru logger.
        input_path: Path to the input AV1 ivf file.
        output_path: Path where to generate the txt file to query the order hints.

    Returns:
        A list of integers representing the frame reference indices.
    """

    # Call av1parser tool to analyze the bitstrean and save this analysis in a txt file.
    logger.debug("Generating the command to retrieve order hints from the bitstream.")
    command = f"cd src/third_parties/av1parser && cargo run ../../../{input_path} -vv"
    command += f" > ../../../{output_path}/output_bitstream.txt && cd ../../.."
    
    logger.debug(f"Running the command: {command}")
    subprocess.run(command, shell=True)

    # Define a RegEx pattern to find the order hints in the txt file.
    pattern = re.compile("order_hints: \[(.*?)\]")
    logger.debug(f"Pattern to find the order hints: {pattern}")

    # Read the txt file and find the order hints.
    try:
        with open(f"{output_path}/output_bitstream.txt", mode="rt", encoding="utf-8") as docFile:
            doc = docFile.read()
            refs_frame_index = re.findall(pattern, doc)

    except Exception as e:
        logger.error(f"Error reading the txt file: {e}")
        raise e

    # Remove the txt file.
    os.remove(f"{output_path}/output_bitstream.txt")

    return refs_frame_index
