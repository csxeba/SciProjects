import socket as sck

import numpy as np
import cv2

REMOTE = "192.168.1.2", 1234
LOCAL = "127.0.0.1", 1234


def generate_frames(remote):
    sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    sock.bind(remote)
    sock.listen(1)

    conn, addr = sock.accept()
    print("Connection from {}".format(addr))

    while 1:
        data = b""
        while 1:
            d = conn.recv(1024)
            if d[-4:] == b"NULL":
                data += d[:-4]
                break
            data += d
        data = np.fromstring(data).reshape(640, 480, 3)
        print("SERVER: Got frame of shape:", data.shape)
        cv2.imshow("RECEIVED!", cv2.cvtColor(data, cv2.COLOR_BGR2GRAY))
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            break

    print("RunDone!")

if __name__ == '__main__':
    generate_frames(LOCAL)
