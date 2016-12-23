import socket as sck

import numpy as np
import cv2


REMOTE = "192.168.1.2", 1234
LOCAL = "127.0.0.1", 1234
END = bytes("NULL", encoding="utf8")


def read_capture_device():
    feed = cv2.VideoCapture(0)
    for _ in range(10):
        yield feed.read()


def stream_data():
    sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    sock.connect(LOCAL)
    for ret, frame in read_capture_device():
        print("CLIENT: Frame shape:", frame.shape)
        strdata = frame.tobytes() + END
        sock.sendall(strdata)
    sock.close()

if __name__ == '__main__':
    stream_data()
