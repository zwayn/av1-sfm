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
