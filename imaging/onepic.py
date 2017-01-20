from skimage import measure

from csxdata.utilities.highlevel import image_to_array

from SciProjects.imaging.misc import preprocess
from SciProjects.imaging.algorithm import algo_fitpolynom

img = "D:/dohany_kepanalizis/SNAP-133827-0001.jpg"

pic = image_to_array(img)
lpic = preprocess(pic, show=True)
measurement = algo_fitpolynom(sorted([prp for prp in measure.regionprops(lpic)
                                      if prp.area > 10000 and prp.image.shape[0] > 1000],
                                     key=lambda p: p.bbox[0]),
                              show=True, lpic=lpic, deg=5, labeltup=(None, "SNAP-133827-0001.jpg"))
print("MEASURED:", measurement)
