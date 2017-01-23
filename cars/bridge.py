import socket as sck
import pickle

import numpy as np

from matplotlib import pyplot as plt


REMOTE = "127.0.0.1", 1234


def generate_frames(socket):
    data = b""
    while 1:
        d = socket.recv(1024)

        if d[:6] == b"cnumpy" and data:
            frame = pickle.loads(data)
            yield frame
            data = b""

        data += d

if __name__ == '__main__':
    sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    sock.connect(REMOTE)

    print("CLIENT: Connection established!")

    plt.ion()
    obj = plt.matshow(np.eye(640, 480, dtype=int) * 255)

    for pic in generate_frames(sock):
        print("CLIENT: Got pic of shape", pic.shape)
        obj.set_data(pic)
        plt.pause(1)

    plt.close()
