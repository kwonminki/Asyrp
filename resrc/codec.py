import cv2
import os


def listdirs(rootdir, _files=[]):
    for it in os.scandir(rootdir):
        if it.is_dir():
            listdirs(it, _files)
        else:
            _files.append(it.path)

# Get all files in the directory
files = []
listdirs("video_quality", files)


for file_name in files:
    os.system(f"ffmpeg -i {file_name} -vcodec libx264 {file_name} -y")

