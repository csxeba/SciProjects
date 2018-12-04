import cv2
import nibabel as nib


data_root = "/data/Megosztott/Dokumentumok/SciProjects/Project_Hippocrates/ISBI2015_Challenge_atlases/atlas_with_mask1/"
data_file = data_root + "atlas1_T1.nii.gz"

img = nib.load(data_file)
data = img.get_fdata()

data = data / data.max()
print("Data shape:", data.shape)
print("Iterating over axis 1")
for array in data.transpose(1, 0, 2):
    cv2.imshow("Array", array)
    cv2.waitKey(100)
