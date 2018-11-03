import cv2
import os
import argparse
from skimage.measure import compare_ssim

parser = argparse.ArgumentParser()
parser.add_argument("--file")
args = parser.parse_args()

# tolerance defines to save or not
tolerance = 0.4

# with opencv2, Open video
video = cv2.VideoCapture(args.file)
count = 0

ret = None
image = None
grayOrigin = None
length = None

if video.isOpened():
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    print("Filename: ", args.file)
    print("Video size: " + str(width) + "x" + str(height))
    print("frame size: ", length)
    print("fps: ", fps)
    print("tolerance: ", tolerance)
    ret, image = video.read()
    grayOrigin = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

while(video.isOpened()):
    # os.makedirs(os.path.join("./", "temp"))
    if ret != False:
        count += 1
        aaa = os.path.join("./", "temp", "frame" + str(count) + ".jpg")
        compare_ret, compare_image = video.read()
        grayCompare = cv2.cvtColor(compare_image, cv2.COLOR_BGR2GRAY)
        (ssim, diff) = compare_ssim(grayOrigin, grayCompare, full=True)
        print("SSIM: {}".format(ssim))
        if ssim <= tolerance:
            print("The origin is changed to frame " + str(count) + "/" + str(length));
            image = compare_image
            grayOrigin = grayCompare

        # cv2.imwrite(os.path.join("./", "temp", "frame" + count + ".jpg"), image)
        # print("Saved frame ", count)

video.release()