# bayer2rgb
=========
bayer2rgb with python


usage
------------
  python .\raw2rgb.py -h
  usage: raw2rgb.py [-h] [--path PATH] [--rawfile RAWFILE] --width WIDTH
                    --height HEIGHT --pattern PATTERN --depth DEPTH
                    [--gray GRAY] [--split SPLIT]

  optional arguments:
    -h, --help         show this help message and exit
    --path PATH        input raw path
    --rawfile RAWFILE  input raw file name
    --width WIDTH      raw image width
    --height HEIGHT    raw image height
    --pattern PATTERN  raw image bayer pattern: [rggb/RGGB, grbg/GRBG,
                       gbrg/GBRG, bggr/BGGR]
    --depth DEPTH      raw image depth [8, 10, 12, 14, 16]
    --gray GRAY        show gray raw image
    --split SPLIT      split bayer channel
  

eg.
------------
(1)single python .\raw2rgb.py --rawfile raw8_1600x1200_RGGB.raw --width 1600 --height 1200 --pattern rggb --depth 8 [--gray 1] [--split 1]
(2)batch python .\raw2rgb.py --path D:\bayer2rgb --width 1600 --height 1200 --pattern rggb --depth 8 [--gray 1] [--split 1]
