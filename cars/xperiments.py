import time
import pickle
import socket as sck

import numpy as np


LOCAL = "127.0.0.1", 1234


def read_capture_device():
    while 1:
        yield (np.random.randn(640, 480) * 255).astype(int)


def stream_data():
    sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    sock.bind(LOCAL)
    print("SERVER: Waiting for connection...")
    sock.listen(1)
    sock, addr = sock.accept()
    print("SERVER: Received connection from", addr)
    for frame in read_capture_device():
        print("SERVER: Frame shape:", frame.shape)
        strdata = bytes(pickle.dumps(frame, protocol=0))
        slices = (strdata[start:start+1024] for start in
                  range(0, len(strdata), 1024))
        for slc in slices:
            sock.send(slc)
        sock.send(b"\0")
        time.sleep(1)
    sock.close()

if __name__ == '__main__':
    stream_data()
