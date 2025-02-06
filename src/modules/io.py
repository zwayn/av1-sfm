'''
 # @ : io.py
 # @ Created by: Julien Zouein
 # @ Create Time: 2025-02-05
 # @ Copyright: © 2024 Sigmedia.tv. All rights reserved.
 # @          : © 2024 Julien Zouein (zoueinj@tcd.ie).
 # @ Modified by: Julien Zouein
 # @ Modified time: 2025-02-05
 # @  :----------------------------------------------------------------------------:
 # @ Description: All the function related to input and output.
 '''


import os
import shutil
import subprocess


IVF_SIGNATURE = b"DKIF"
IVF_HEADER_SIZE = 32
CODEC = b"AV01"


def check_ivf_file(file_path: str) -> bool:
    with open(file_path, "rb") as file:
        header = file.read(IVF_HEADER_SIZE)

        signature = header[:4]
        codec = header[8:12]

        if signature != IVF_SIGNATURE or codec != CODEC:
            return False
        return True


def copy_images(image_paths: list[str], output_folder: str):
    """ Copy the images to the output folder.

    The images copied name is being normalized to be in the right format.

    Args:
        image_paths (list[str]): The paths to the images.
        output_folder (str): The path to the output folder.
    """

    os.makedirs(f"{output_folder}/images", exist_ok=True)

    for idx, image_path in enumerate(image_paths):
        # Get the extension of the image.
        image_path_extension = image_path.split(".")[-1]
        
        new_filename = f"frame_{idx:04d}.{image_path_extension}"
        dest_path = os.path.join(output_folder, "images", new_filename)
        shutil.copy2(image_path, dest_path)

def copy_video(video_path: str, output_folder: str):
    """ Copy the video to the output folder.

    Args:
        video_path (str): The path to the video.
        output_folder (str): The path to the output folder.
    """

    shutil.copy2(video_path, os.path.join(output_folder, "video.ivf"))


def generate_json(input_path: str):
    """ Generate json file using AOM inspect tool.

    To get the metadata of an ivf file, we use AOM inspect tool. This tool
    generate a json file.
    
    Args:
        input_path (str): The path to the folder containing the images.
    """

    command = f"./src/third_parties/aom_build/examples/inspect {input_path}/video.ivf "
    command += f" -mv -r -bs > {input_path}/video.json"
    subprocess.run(command, shell=True)


def generate_video(input_path: str):
    """ Generate a video from the images.

    Args:
        input_path (str): The path to the folder containing the images.
    """

    command = f"ffmpeg -framerate {60} -pattern_type glob -i './{input_path}/images/frame_*.png' -pix_fmt yuv444p " \
                    f"{input_path}/video.y4m"
    
    subprocess.run(command, shell=True)


def generate_ivf_file(input_path: str, encoding_preset: str):
    """ Generate an ivf file from the video.

    Args:
        input_path (str): The path to the video.
        encoding_preset (str): The encoding preset.
    """

    command = f"./src/encoding/{encoding_preset}.sh {input_path}/video.y4m {input_path}/video.ivf"
    subprocess.run(command, shell=True)


def get_image_paths(folder_path: str) -> list[str]:
    """ Get the paths of all the images in the folder.

    The input of the process can be a folder full of images that we will have to
    encode.

    Args:
        folder_path (str): The path to the folder containing the images.

    Returns:
        list[str]: A list of paths to the images.
    """

    image_paths = []
    extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", "webp", ".npy"]
    for directory_path, _, filenames in os.walk(folder_path):
        file_paths = [
            file for file in filenames if any(file.lower().endswith(extension) for extension in extensions)
        ]

        for filename in file_paths:
            image_paths.append(os.path.join(directory_path, filename))
    image_paths.sort()

    return image_paths


def process_images(input_path: str, output_path: str, encoding_preset: str):
    """ Process the images.

    Args:
        input_path (str): The path to the folder containing the images.
        output_path (str): The path to the output folder.
        encoding_preset (str): The encoding preset.
    """

    image_paths = get_image_paths(input_path)
    copy_images(image_paths, output_path)
    generate_video(output_path)
    generate_ivf_file(output_path, encoding_preset)