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
