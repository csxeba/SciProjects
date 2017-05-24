from skimage import io


def get_image():
    return (1 - io.imread("/home/csa/Rizs/S1-1bin.png") / 255).astype(bool)
