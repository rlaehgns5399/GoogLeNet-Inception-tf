import cv2
import os
import argparse
from skimage.measure import compare_ssim

parser = argparse.ArgumentParser()
parser.add_argument("--file")
parser.add_argument("--method", default="SSIM")
parser.add_argument("--debug", default="Y")
parser.add_argument("--tolerance", default=0.4)
args = parser.parse_args()

folder_name = "images_" + args.file

# tolerance defines to save or not
tolerance = args.tolerance

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

    if args.debug == "Y":
        print("Filename: ", args.file)
        print("Video size: " + str(width) + "x" + str(height))
        print("frame size: ", length)
        print("fps: ", fps)
        print("method: ", args.method)
        print("tolerance: ", tolerance)

    ret, image = video.read()
    grayOrigin = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    os.makedirs(os.path.join(folder_name))

def SSIM(img1, img2):
    (ssim, diff) = compare_ssim(img1, img2, full=True)
    if args.debug == "Y":
        print("SSIM: {}".format(ssim))
    return ssim

while(video.isOpened()):
    if ret != False:
        count += 1
        aaa = os.path.join("./", "temp", "frame" + str(count) + ".jpg")
        compare_ret, compare_image = video.read()
        grayCompare = cv2.cvtColor(compare_image, cv2.COLOR_BGR2GRAY)

        if args.method == "SSIM":
            score = SSIM(grayOrigin, grayCompare)
            if score <= float(args.tolerance):
                cv2.imwrite(os.path.join(folder_name, "frame" + str(count) + ".jpg"), image)
                if args.debug == "Y":
                    print("The origin is changed to frame " + str(count) + "/" + str(length));
                image = compare_image
                grayOrigin = grayCompare
        elif args.method == "ORB":
            print("")
    else:
        break

video.release()

