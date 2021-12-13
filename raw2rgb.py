import os
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
    #print("raw file size:", bayerIMG_data.size)

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

    #showColorImg(bayerFile, rgbIMG)
    # closeWindows()


def convertBayer2GRAY(bayerFile, imgWidth, imgHeight, bitDeepth, bayerPattern, splitChannel):
    if bitDeepth == 8:
        bayerIMG_data = np.fromfile(bayerFile, dtype='uint8')
        grayIMG = np.zeros([imgHeight, imgWidth, 3], dtype='uint8')
    else:
        bayerIMG_data = np.fromfile(bayerFile, dtype='uint16')
        grayIMG = np.zeros([imgHeight, imgWidth, 3], dtype='uint16')
    #print("raw file size:", bayerIMG_data.size)

    bayerIMG = bayerIMG_data.reshape(imgHeight, imgWidth, 1)

    for i in range(0, imgHeight, 1):
        for j in range(0, imgWidth, 1):
            grayIMG[i][j][0] = grayIMG[i][j][1] = grayIMG[i][j][2] = bayerIMG[i][j]

    if bitDeepth == 8:
        grayIMG = np.uint8(grayIMG)  # raw8
    elif bitDeepth == 10:
        grayIMG = np.uint16(grayIMG*64)  # raw10
    elif bitDeepth == 12:
        grayIMG = np.uint16(grayIMG*16)  # raw12
    elif bitDeepth == 14:
        grayIMG = np.uint16(grayIMG*4)  # raw14
    elif bitDeepth == 16:
        grayIMG = np.uint16(grayIMG)  # raw16
    else:
        print("unsupport bayer bitDeepth:", bitDeepth)

    if splitChannel == 1:
        splitWidth = imgWidth // 2
        splitHeight = imgHeight // 2
        if bitDeepth == 8:
            grayIMGch1 = np.zeros([splitHeight, splitWidth, 3], dtype='uint8')
            grayIMGch2 = np.zeros([splitHeight, splitWidth, 3], dtype='uint8')
            grayIMGch3 = np.zeros([splitHeight, splitWidth, 3], dtype='uint8')
            grayIMGch4 = np.zeros([splitHeight, splitWidth, 3], dtype='uint8')
        else:
            grayIMGch1 = np.zeros([splitHeight, splitWidth, 3], dtype='uint16')
            grayIMGch2 = np.zeros([splitHeight, splitWidth, 3], dtype='uint16')
            grayIMGch3 = np.zeros([splitHeight, splitWidth, 3], dtype='uint16')
            grayIMGch4 = np.zeros([splitHeight, splitWidth, 3], dtype='uint16')

        posX = 0
        posY = 0
        for i in range(0, (imgHeight-1), 2):  # first pixel
            posY = 0
            for j in range(0, (imgWidth-1), 2):
                grayIMGch1[posX][posY][0] = grayIMGch1[posX][posY][1] = grayIMGch1[posX][posY][2] = grayIMG[i][j][0]
                posY = posY + 1
            posX = posX + 1
        cv2.imwrite(bayerFile[:-4]+'_GRAY_ch1.png', grayIMGch1)
        posX = 0
        posY = 0
        for i in range(0, (imgHeight-1), 2):  # second pixel
            posY = 0
            for j in range(1, (imgWidth-1), 2):
                grayIMGch2[posX][posY][0] = grayIMGch2[posX][posY][1] = grayIMGch2[posX][posY][2] = grayIMG[i][j][0]
                posY = posY + 1
            posX = posX + 1
        cv2.imwrite(bayerFile[:-4]+'_GRAY_ch2.png', grayIMGch2)
        posX = 0
        posY = 0
        for i in range(1, (imgHeight-1), 2):  # third pixel
            posY = 0
            for j in range(0, (imgWidth-1), 2):
                grayIMGch3[posX][posY][0] = grayIMGch3[posX][posY][1] = grayIMGch3[posX][posY][2] = grayIMG[i][j][0]
                posY = posY + 1
            posX = posX + 1
        cv2.imwrite(bayerFile[:-4]+'_GRAY_ch3.png', grayIMGch3)
        posX = 0
        posY = 0
        for i in range(1, (imgHeight-1), 2):  # fourth pixel
            posY = 0
            for j in range(1, (imgWidth-1), 2):
                grayIMGch4[posX][posY][0] = grayIMGch4[posX][posY][1] = grayIMGch4[posX][posY][2] = grayIMG[i][j][0]
                posY = posY + 1
            posX = posX + 1
        cv2.imwrite(bayerFile[:-4]+'_GRAY_ch4.png', grayIMGch4)

    cv2.imwrite(bayerFile[:-4]+'_GRAY.png', grayIMG)

    #showColorImg(bayerFile, grayIMG)
    # closeWindows()


def ProcSingleFile(rawFile, img_width, img_height,
                   rawDepth, bayerPattern, splitFlag):
    #(path, rawFile) = os.path.split(raw_name)
    print("process ", rawFile, "...")
    if args.gray == 1:
        convertBayer2GRAY(rawFile, img_width, img_height,
                          rawDepth, bayerPattern, splitFlag)
    else:
        convertBayer2RGB(rawFile, img_width, img_height,
                         rawDepth, bayerPattern)


def ProcPath(path, img_width, img_height,
             rawDepth, bayerPattern, splitFlag):
    file_list = os.listdir(path)
    for f in file_list:
        f_lower = f.lower()
        if f_lower.endswith('.raw'):
            raw_name = '%s\%s' % (path, f)
            ProcSingleFile(raw_name, img_width, img_height,
                           rawDepth, bayerPattern, splitFlag)


if "__main__" == __name__:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--path", help="input raw path", required=False, type=str)
    parser.add_argument(
        "--rawfile", help="input raw file name", required=False, type=str)
    parser.add_argument("--width", help="raw image width",
                        required=True, type=int)
    parser.add_argument("--height", help="raw image height",
                        required=True, type=int)
    parser.add_argument(
        "--pattern", help="raw image bayer pattern: [1:RGGB, 2:GRBG, 3:GBRG, 4:BGGR]", required=True, type=int)
    parser.add_argument(
        "--depth", help="raw image depth [8, 10, 12, 14, 16]", required=True, type=int)
    parser.add_argument(
        "--gray", help="show gray raw image", required=False, type=bool)
    parser.add_argument(
        "--split", help="split bayer channel", required=False, type=bool)

    args = parser.parse_args()

    rawPath = args.path
    rawFile = args.rawfile
    img_width = args.width
    img_height = args.height
    bayerPattern = args.pattern
    rawDepth = args.depth
    splitFlag = args.split

    if rawPath is not None:
        ProcPath(rawPath, img_width, img_height,
                 rawDepth, bayerPattern, splitFlag)
    elif rawFile is not None:
        ProcSingleFile(rawFile, img_width, img_height,
                       rawDepth, bayerPattern, splitFlag)
    else:
        print("parameters wrong!!! no path or file")
