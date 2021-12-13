import numpy as np
import cv2
import argparse


class bayerFormat:
    BayerRGGB = 1
    BayerGRBG = 2
    BayerGBRG = 3
    BayerBGGR = 4


def showColorImg(imgName, img):
    cv2.namedWindow(imgName, cv2.WINDOW_NORMAL)
    cv2.imshow(imgName, img)


def closeWindows():
    cv2.waitKey(0)
    # 释放窗口
    cv2.destroyAllWindows()


def convertBayer2RGB(bayerFile, imgWidth, imgHeight, bitDeepth, bayerPattern):
    if bitDeepth == 8:
        bayerIMG_data = np.fromfile(bayerFile, dtype='uint8')
    else:
        bayerIMG_data = np.fromfile(bayerFile, dtype='uint16')
    print("raw file size:", bayerIMG_data.size)

    bayerIMG = bayerIMG_data.reshape(imgHeight, imgWidth, 1)

    if bayerPattern == bayerFormat.BayerRGGB:
        rgbIMG = cv2.cvtColor(bayerIMG, cv2.COLOR_BayerRG2RGB)
    elif bayerPattern == bayerFormat.BayerGRBG:
        rgbIMG = cv2.cvtColor(bayerIMG, cv2.COLOR_BayerGR2RGB)
    elif bayerPattern == bayerFormat.BayerGBRG:
        rgbIMG = cv2.cvtColor(bayerIMG, cv2.COLOR_BayerGB2RGB)
    elif bayerPattern == bayerFormat.BayerBGGR:
        rgbIMG = cv2.cvtColor(bayerIMG, cv2.COLOR_BayerBG2RGB)
    else:
        print("unsupport bayer format:", bayerPattern)

    if bitDeepth == 8:
        rgbIMG = np.uint8(rgbIMG)  # raw8
    elif bitDeepth == 10:
        rgbIMG = np.uint16(rgbIMG*64)  # raw10
    elif bitDeepth == 12:
        rgbIMG = np.uint16(rgbIMG*16)  # raw12
    elif bitDeepth == 14:
        rgbIMG = np.uint16(rgbIMG*4)  # raw14
    elif bitDeepth == 16:
        rgbIMG = np.uint16(rgbIMG)  # raw16
    else:
        print("unsupport bayer bitDeepth:", bitDeepth)

    cv2.imwrite(bayerFile[:-4]+'.png', rgbIMG)

    showColorImg(bayerFile, rgbIMG)
    closeWindows()


def convertBayer2GRAY(bayerFile, imgWidth, imgHeight, bitDeepth, bayerPattern):
    if bitDeepth == 8:
        bayerIMG_data = np.fromfile(bayerFile, dtype='uint8')
    else:
        bayerIMG_data = np.fromfile(bayerFile, dtype='uint16')
    print("raw file size:", bayerIMG_data.size)

    bayerIMG = bayerIMG_data.reshape(imgHeight, imgWidth, 1)

    rgbIMG = np.zeros([imgHeight, imgWidth, 3])

    for i in range(0, imgHeight, 1):
        for j in range(0, imgWidth, 1):
            rgbIMG[i][j][0] = rgbIMG[i][j][1] = rgbIMG[i][j][2] = bayerIMG[i][j]

    if bitDeepth == 8:
        rgbIMG = np.uint8(rgbIMG)  # raw8
    elif bitDeepth == 10:
        rgbIMG = np.uint16(rgbIMG*64)  # raw10
    elif bitDeepth == 12:
        rgbIMG = np.uint16(rgbIMG*16)  # raw12
    elif bitDeepth == 14:
        rgbIMG = np.uint16(rgbIMG*4)  # raw14
    elif bitDeepth == 16:
        rgbIMG = np.uint16(rgbIMG)  # raw16
    else:
        print("unsupport bayer bitDeepth:", bitDeepth)

    cv2.imwrite(bayerFile[:-4]+'_GRAY.png', rgbIMG)

    showColorImg(bayerFile, rgbIMG)
    closeWindows()


if "__main__" == __name__:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--rawfile", help="input raw file name", required=True, type=str)
    parser.add_argument("--width", help="raw image width",
                        required=True, type=int)
    parser.add_argument("--height", help="raw image height",
                        required=True, type=int)
    parser.add_argument(
        "--pattern", help="raw image bayer pattern: [1:RGGB, 2:GRBG, 3:GBRG, 4:BGGR]", required=True, type=int)
    parser.add_argument(
        "--depth", help="raw image depth [8, 10, 12, 14, 16]", required=True, type=int)
    parser.add_argument(
        "--gray", help="show gray raw image", required=False, type=int)

    args = parser.parse_args()

    rawFile = args.rawfile
    img_width = args.width
    img_height = args.height
    bayerPattern = args.pattern
    rawDepth = args.depth
    if args.gray == 1:
        convertBayer2GRAY(rawFile, img_width, img_height,
                          rawDepth, bayerPattern)
    else:
        convertBayer2RGB(rawFile, img_width, img_height,
                         rawDepth, bayerPattern)
