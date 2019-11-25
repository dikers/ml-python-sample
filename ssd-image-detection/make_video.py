
"""
ffmpeg -ss 00:05 -i /Users/mac/PycharmProjects/ml-python-sample/ssd-image-detection/dataset/output.mp4 -f image2  -s 1280x768 -r 6 -t 02:00 %4d.jpg
sudo killall VDCAssistant
"""


import numpy as np
import cv2


cap = cv2.VideoCapture(0)

## some videowriter props
sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
      int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

fps = 30
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# fourcc = cv2.VideoWriter_fourcc('m', 'p', 'e', 'g')
# fourcc = cv2.VideoWriter_fourcc(*'mpeg')

## open and set props
out = cv2.VideoWriter()
out.open('./dataset/output.mp4', fourcc, fps, sz, True)

while (True):
    ret, frame = cap.read()
    out.write(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()