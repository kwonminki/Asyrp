#%%
import cv2
import os
import shutil
from PIL import Image

#%%
def listdirs(rootdir, _files=[]):
    for it in os.scandir(rootdir):
        if it.is_dir():
            listdirs(it, _files)
        else:
            _files.append(it.path)

dir_name = "video_ddim"

# Get all files in the directory
files = []
# listdirs("video_quality", files)
listdirs(dir_name, files)


#%%
# Convert mp4 to png



for file_name in files:
    if file_name.split(".")[-1] != "mp4":
        continue
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

#%%

# Get all files in the directory
files = []
# listdirs("video_quality", files)
listdirs(dir_name, files)

for file_name in files:
    
    # check if the file is png
    if file_name.split(".")[-1] != "png":
        continue

    image = cv2.imread(file_name)

    # get image size
    height, width, channels = image.shape

    # make new image with height+50, width, channels
    new_image = cv2.copyMakeBorder(image, 0, 50, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    # get file name as number
    processed_percent = int(file_name.split("/")[-1].split(".")[0]) / 29

    # write red arrowedLine on bottom of new_image which of length is width * processed_percent
    cv2.arrowedLine(new_image, (25, height+32), (int((width-50) * processed_percent)+25, height+32), (0, 0, 255), 5)
    
    # write text on bottom of new_image
    # text : real , position : left, color : white
    cv2.putText(new_image, f"real", (5, height+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    # text : edited , position : right, color : white
    cv2.putText(new_image, f"edited", (width-50, height+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # new_image to PIL image
    new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    new_image = Image.fromarray(new_image)
    
    # save image
    new_image.save(file_name)
    
#%%
# Convert png to mp4

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

        os.system(f"ffmpeg -f image2 -framerate 10 -i {image_dir}/%d.png -c:v libx264 -crf 18 -preset veryslow -pix_fmt yuv420p {filename} -y")

        shutil.rmtree(image_dir)

