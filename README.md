# bayer2rgb
bayer2rgb with python


python .\raw2rgb.py -h
usage: raw2rgb.py [-h] --rawfile RAWFILE --width WIDTH --height HEIGHT
                  --pattern PATTERN --depth DEPTH [--gray GRAY]
                  [--split SPLIT]

optional arguments:
  -h, --help         show this help message and exit
  --rawfile RAWFILE  input raw file name
  --width WIDTH      raw image width
  --height HEIGHT    raw image height
  --pattern PATTERN  raw image bayer pattern: [1:RGGB, 2:GRBG, 3:GBRG, 4:BGGR]
  --depth DEPTH      raw image depth [8, 10, 12, 14, 16]
  --gray GRAY        show gray raw image
  --split SPLIT      split bayer channel
  

eg.
python .\raw2rgb.py --rawfile raw8_1600x1200_RGGB.raw --width 1600 --height 1200 --pattern 1 --depth 8 [--gray 1] [--split 1]