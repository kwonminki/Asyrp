import cv2
import os
import shutil


def listdirs(rootdir, _files=[]):
    for it in os.scandir(rootdir):
        if it.is_dir():
            listdirs(it, _files)
        else:
            _files.append(it.path)

# Get all files in the directory
files = []
listdirs("video_ddim", files)


for file_name in files:
    vidcap = cv2.VideoCapture(f'{file_name}')
    success,image = vidcap.read()
    count = 0
    dir_name = file_name.split(".")[0]
    os.makedirs(dir_name, exist_ok=True)
    while success:    
        cv2.imwrite(f"{dir_name}/{count}.png", image)     # save frame as JPEG file
        success,image = vidcap.read()
        # print('Read a new frame: ', success)
        count += 1
        # break # Only get the first frame

print("finish! convert video to frame")

# make grid images


for filename in files:
    img_array = []
    if filename.endswith(".mp4"):
        # get file directory
        dir = os.path.dirname(filename)
        # get file name
        name = os.path.basename(filename)
        # get file name without extension
        name = os.path.splitext(name)[0]
        # get directory which is the name of the video
        image_dir = os.path.join(dir, name)

        os.system(f"ffmpeg -f image2 -framerate 10 -i {image_dir}/%d.png -c:v libx264 -crf 18 -preset veryslow {filename} -pix_fmt yuv420p -y")

        shutil.rmtree(image_dir)

